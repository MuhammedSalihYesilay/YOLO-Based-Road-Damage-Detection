"""
Görüntü sayfası (Adım 7a): fotoğraf yükle veya örnek seç → e5 modeli hasarları bulur →
kutu + sınıf + güven skoru gösterilir. Güven eşiği ve sınıf filtresi kenar çubuğunda.

Akış:
1. Girdi iki yoldan gelir: "Görüntü yükle" sekmesi veya "Örnek görüntüler" sekmesi.
   En son yapılan seçim geçerlidir (st.session_state["source"]).
2. Model görüntüde bir kez, düşük eşikle (0,05) çalışır; sonuç dosya içeriğine göre önbelleğe alınır.
3. Eşik ve sınıf filtresi yalnızca kutuları süzer → kaydırıcı oynatılınca model yeniden çalışmaz.
"""

from pathlib import Path

import pandas as pd
import streamlit as st
import torch

from core.classes import CLASS_CODES, hex_color
from core.draw import draw_detections, format_conf
from core.images import load_image
from core.model import (DEFAULT_CONF, IMGSZ, MIN_CONF, MODEL_NAME, WEIGHTS, filter_detections, load_model,
                        pick_device, predict)
from core.texts import class_name, country_name, get_lang, t

DEMO_DIR = Path(__file__).resolve().parents[1] / "assets" / "demo"  # src/app/assets/demo
THUMB_COLS = 5  # örnek ızgarasında bir satırdaki küçük resim sayısı (10 örnek → 2 satır)


# ---------------------------------------------------------------- önbellekli yardımcılar

@st.cache_data(show_spinner=False, max_entries=20)
def run_detection(_model, data):
    """Dosya baytlarından görüntüyü okur ve modeli çalıştırır; (rgb, tespitler, ms) döndürür.

    st.cache_data sonucu `data` (dosya içeriği) için saklar: aynı görüntü yeniden seçilince model çalışmaz.
    `_model` başındaki alt çizgi: Streamlit bu parametreyi önbellek anahtarına katmaz (model hash'lenemez).
    """
    rgb = load_image(data)
    if rgb is None:
        return None, [], 0.0
    detections, ms = predict(_model, rgb)
    return rgb, detections, ms


@st.cache_data(show_spinner=False)
def demo_thumbnail(path):
    """Örnek görüntünün kare küçük kopyasını döndürür (ızgarada hızlı ve hizalı gösterim için).

    Ortadan kare kırpılır: Norveç (geniş, 16:9) ve diğerleri (kare) aynı boyda görünür, altlarındaki düğmeler
    aynı hizada kalır. Yalnız küçük resim kırpılır; modele giden görüntü dosyanın tamamıdır (pick_example).
    """
    from PIL import Image, ImageOps  # yalnız burada gerekli
    img = Image.open(path).convert("RGB")
    return ImageOps.fit(img, (360, 360), method=Image.Resampling.LANCZOS)  # ortadan kare kırp + küçült


def demo_country(path):
    """Demo dosya adından ülkeyi çıkarır: "01_China_MotorBike_002019.jpg" → "China_MotorBike".

    Baştaki "01_" sıra numarası, sondaki "_002019" RDD2022 görüntü numarası atılır.
    """
    return path.stem.split("_", 1)[1].rsplit("_", 1)[0]


def demo_files():
    """Örnek görüntü dosyalarını ada göre sıralı döndürür (klasör yoksa boş liste).

    Dosya adları sıra numarasıyla başladığı için (01_, 02_ ...) ada göre sıralama = seçilen gösterim sırası.
    """
    if not DEMO_DIR.exists():
        return []
    return sorted(p for p in DEMO_DIR.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"})


# ---------------------------------------------------------------- girdi seçimi

# Geçerli girdinin nereden geldiği st.session_state'te tutulur:
#   "source_kind": "upload" (yüklenen dosyalardan biri) / "example" (örnek görüntü) / yok
#   "upload_pick": yüklenenlerden seçili olanın file_id'si (seçici bileşenin key'i)
#   "upload_ids":  bir önceki çalıştırmadaki yüklü dosyaların file_id listesi (yeni ekleneni bulmak için)
#   "example_path": seçili örnek görüntünün yolu
# Modelin yeniden çalışmaması dosya baytlarının önbelleğiyle sağlanır (run_detection, st.cache_data):
# seçimler arasında geçiş yalnızca hangi baytların gösterileceğini değiştirir.

def on_upload():
    """Yükleyicideki liste değişince çalışır: yeni eklenen dosyayı seçili yapar, silineni seçimden çıkarır."""
    files = st.session_state.get("uploader") or []
    ids = [f.file_id for f in files]  # file_id: aynı adlı iki dosyayı da ayırt eden benzersiz kimlik
    new = [i for i in ids if i not in st.session_state.get("upload_ids", [])]
    st.session_state["upload_ids"] = ids
    if new:
        st.session_state["upload_pick"] = new[-1]  # yeni eklenen fotoğraf hemen gösterilsin
        st.session_state["source_kind"] = "upload"
    elif st.session_state.get("upload_pick") not in ids:
        # Seçili dosya çarpıyla silindi: varsa ilk dosyaya geç, hiç dosya kalmadıysa girdiyi temizle
        if ids:
            st.session_state["upload_pick"] = ids[0]
        else:
            st.session_state.pop("upload_pick", None)
            if st.session_state.get("source_kind") == "upload":
                st.session_state.pop("source_kind", None)


def on_pick_upload():
    """Seçiciden başka bir yüklenmiş fotoğraf seçilince geçerli girdiyi yüklenenlere çevirir."""
    st.session_state["source_kind"] = "upload"


def pick_example(path):
    """Örnek görüntü seçilince onu geçerli girdi yapar."""
    st.session_state["source_kind"] = "example"
    st.session_state["example_path"] = path


def upload_tab():
    """Yükleme sekmesi: birden çok dosya kabul eder; birden fazla dosya varsa altında seçici gösterir.

    Seçili yüklenmiş dosyayı (UploadedFile; adı ve baytları içinde) veya None döndürür.
    """
    files = st.file_uploader(t("upload_label"), type=["jpg", "jpeg", "png"], accept_multiple_files=True,
                             key="uploader", on_change=on_upload) or []
    if not files:
        return None
    by_id = {f.file_id: f for f in files}
    if st.session_state.get("upload_pick") not in by_id:
        st.session_state["upload_pick"] = files[0].file_id  # güvenlik: seçim geçersizse ilk dosya
    if len(files) > 1:
        # Seçenekler file_id; ekranda dosya adı görünür (format_func)
        st.selectbox(t("upload_pick_label"), options=list(by_id), format_func=lambda i: by_id[i].name,
                     key="upload_pick", on_change=on_pick_upload)
    return by_id[st.session_state["upload_pick"]]


def md_escape(text):
    """Markdown'da özel anlamı olan karakterlerin önüne ters bölü koyar.

    Dosya adları ekranda olduğu gibi görünsün: ör. "yol_foto_1.jpg"deki alt çizgiler italik yazıya dönmesin.
    """
    for ch in "\\`*_[]#~":
        text = text.replace(ch, "\\" + ch)
    return text


def input_section():
    """İki sekmeli girdi alanını çizer; (baytlar, seçili girdiyi anlatan kısa satır, seçim kimliği) döndürür.

    Seçim kimliği ("upload:<file_id>" / "example:<dosya adı>") yalnızca seçim değişince sayfayı kaydırmak için
    kullanılır. Girdi yoksa (None, None, None).
    """
    tab_upload, tab_examples = st.tabs([t("tab_upload"), t("tab_examples")])

    with tab_upload:
        upload_file = upload_tab()

    with tab_examples:
        files = demo_files()
        if not files:
            st.caption(t("examples_empty"))
        else:
            st.caption(t("examples_caption"))
            cols = st.columns(THUMB_COLS)
            # Seçili örneğin adı (örnek seçili değilse None): onun düğmesi vurgulu (primary) çizilir
            chosen = (Path(st.session_state["example_path"]).name
                      if st.session_state.get("source_kind") == "example" and "example_path" in st.session_state
                      else None)
            for i, path in enumerate(files):
                with cols[i % THUMB_COLS]:
                    st.image(demo_thumbnail(str(path)), width="stretch")
                    # Küçük resmin altında yalnız ülke adı; aynı zamanda seçme düğmesi
                    st.button(country_name(demo_country(path)), key=f"demo_{path.name}", on_click=pick_example,
                              args=(str(path),), width="stretch",
                              type="primary" if path.name == chosen else "secondary")

    # En son yapılan seçim geçerli: yüklenen fotoğraf mı, örnek görüntü mü.
    # Kısa satır her çalıştırmada yeniden üretilir; dil değişince o da değişir.
    kind = st.session_state.get("source_kind")
    if kind == "upload" and upload_file is not None:
        return (upload_file.getvalue(), t("selected_upload", name=md_escape(upload_file.name)),
                f"upload:{upload_file.file_id}")
    example = Path(st.session_state.get("example_path", ""))
    if kind == "example" and example.is_file():
        names = [p.name for p in files]
        pos = names.index(example.name) + 1 if example.name in names else 0  # 1'den başlayan sıra
        label = t("selected_example", country=country_name(demo_country(example)), i=pos, n=len(files))
        return example.read_bytes(), label, f"example:{example.name}"
    return None, None, None


def scroll_to_results(selection_id):
    """Seçim değiştiyse sayfayı sonuç bölümüne kaydırır; eşik, sınıf filtresi veya dil değişince kaydırmaz.

    Streamlit 1.67'de kaydırma için resmî bir Python fonksiyonu yok. En sade yol: st.html ile küçük bir JavaScript.
    st.html iframe'siz çalışır (script ana sayfada), JavaScript yalnız unsafe_allow_javascript=True ile çalışır.
    Script içeriği sabit (kullanıcı girdisi içermez). Hedef: st.container(key="results") kabının CSS sınıfı
    "st-key-results". Hata olursa (öğe bulunamadı, tarayıcı izin vermedi) try/catch yutar: yalnız kaydırma olmaz.
    """
    if st.session_state.get("last_selection") == selection_id:
        return  # aynı görüntü: kaydırma yok (eşik/dil değişiminde sayfa zıplamasın)
    st.session_state["last_selection"] = selection_id
    # Sayaç script metnini her seferinde farklı yapar; aynı metin gelirse tarayıcı öğeyi yeniden çalıştırmayabilir
    n = st.session_state["scroll_count"] = st.session_state.get("scroll_count", 0) + 1
    st.html(
        f"""<script>
        // kaydirma {n}
        setTimeout(function () {{
          try {{
            var el = document.querySelector(".st-key-results");
            if (el) el.scrollIntoView({{behavior: "smooth", block: "start"}});
          }} catch (e) {{}}
        }}, 150);  // 150 ms: görüntüler yerleşsin, kaydırma doğru konuma gitsin
        </script>""",
        unsafe_allow_javascript=True,
    )


# ---------------------------------------------------------------- kenar çubuğu

def sidebar_controls():
    """Eşik kaydırıcısı ve sınıf filtresi; (eşik, seçili sınıf kodları) döndürür."""
    conf = st.sidebar.slider(t("conf_label"), min_value=MIN_CONF, max_value=0.95, value=DEFAULT_CONF,
                             step=0.05, format="%.2f", help=t("conf_help"), key="conf")
    st.sidebar.write(t("classes_label"))
    codes = [code for code in CLASS_CODES
             if st.sidebar.checkbox(f"{code} · {class_name(code)}", value=True, key=f"cls_{code}")]
    return conf, codes


def device_label():
    """Kenar çubuğunda gösterilecek donanım adı: GPU'nun adı ya da "CPU"."""
    return torch.cuda.get_device_name(0) if pick_device() != "cpu" else "CPU"


# ---------------------------------------------------------------- sonuç

def legend_line(detections, ms):
    """Sınıf başına tespit sayısını renkli kare işaretleriyle tek satırda gösterir (+ toplam ve süre)."""
    parts = []
    for code in CLASS_CODES:
        n = sum(d["code"] == code for d in detections)
        if n:
            # Renkli kare: kutu rengiyle aynı → kullanıcı görüntüdeki rengi satırla eşleştirebilir
            parts.append(f'<span style="color:{hex_color(code)}">&#9632;</span> {class_name(code)} {n}')
    parts.append(t("summary", n=len(detections), ms=ms))
    st.markdown(" &nbsp;·&nbsp; ".join(parts), unsafe_allow_html=True)


def detections_table(detections, lang):
    """Tespitleri güvene göre azalan sırada tablo olarak gösterir.

    st.dataframe yerine st.table: düz, etkileşimsiz tablo. st.dataframe'in İngilizce araç çubuğu (arama, indirme,
    sütun menüsü) çıkmaz, sayfa sade kalır. Güven metin olarak biçimlendirildiği için TR'de virgül, EN'de nokta.
    """
    rows = [{
        t("col_code"): d["code"],
        t("col_class"): class_name(d["code"]),
        t("col_conf"): format_conf(d["conf"], lang),
        t("col_size"): f'{d["box"][2] - d["box"][0]} × {d["box"][3] - d["box"][1]}',  # genişlik × yükseklik
    } for d in sorted(detections, key=lambda d: d["conf"], reverse=True)]
    st.table(pd.DataFrame(rows), hide_index=True)  # hide_index: soldaki 0, 1, 2... satır numaraları gizli


# ---------------------------------------------------------------- sayfa

def main():
    """Sayfanın akışı. Erken çıkışlar st.stop() yerine `return` ile yapılır: st.stop() tüm script'i durdurur ve
    app.py'deki alt not hiç çizilmez."""
    st.title(t("title"))
    st.markdown(t("intro"))

    conf, codes = sidebar_controls()

    # Model dosyası git dışında (runs/); yoksa açık bir mesajla çık
    if not WEIGHTS.exists():
        st.error(t("model_missing", path=WEIGHTS))
        return
    with st.spinner(t("loading_model")):
        model = load_model()

    st.sidebar.space("medium")
    st.sidebar.caption(t("model_info", model=MODEL_NAME, imgsz=IMGSZ, device=device_label()))

    data, selected_label, selection_id = input_section()
    if data is None:
        st.session_state.pop("last_selection", None)  # girdi temizlendi: sonraki seçim yine kaydırsın
        st.caption(t("no_input"))
        return

    with st.spinner(t("running")):
        rgb, detections, ms = run_detection(model, data)
    if rgb is None:
        st.error(t("read_error"))
        return

    lang = get_lang()
    shown = filter_detections(detections, conf, codes)  # eşik + sınıf filtresi (model yeniden çalışmaz)

    # Sonuç bölümü anahtarlı bir kapta: key="results" → CSS sınıfı "st-key-results" (kaydırmanın hedefi)
    with st.container(key="results"):
        st.markdown(selected_label)  # hangi görüntü gösteriliyor: "Seçili örnek: Çin (1/10)" / yüklenen dosya adı
        left, right = st.columns(2)
        with left:
            st.subheader(t("original"))
            st.image(rgb, width="stretch")
        with right:
            st.subheader(t("detections"))
            st.image(draw_detections(rgb, shown, lang), width="stretch")

        if shown:
            legend_line(shown, ms)
            detections_table(shown, lang)
        else:
            st.write(t("no_detections"))

    scroll_to_results(selection_id)  # yalnız seçim değiştiyse sonuç bölümüne kaydır


main()
