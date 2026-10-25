"""
Adım 1 — RDD2022 veri analizi.

Sadece etiket dosyalarını (ann/*.json, Supervisely formatı) okur; görüntü açmaz.
Görüntü boyutu JSON'daki "size" alanından alınır.

Çıktılar:
  --out      (docs/analysis/)  toplu tablolar (CSV), grafikler (PNG), summary.md  -> git'e girer
  --raw-out  (data/analysis/)  ham images.csv ve boxes.csv                         -> git dışı

Çalıştırma:
  python src/analysis/analyze_dataset.py --data-root data/rdd2022 --out docs/analysis --raw-out data/analysis --seed 42
"""

import argparse
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # pencere açmadan doğrudan dosyaya çiz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Eğitimde kullanılacak 4 sınıf. Veri setinde D kodları yok, sınıflar isimle geçiyor.
# Sıra (D00, D10, D20, D40) ileride YOLO sınıf numarası (0..3) olacak.
TARGET_CLASSES = {
    "longitudinal crack": "D00",
    "transverse crack": "D10",
    "alligator crack": "D20",
    "pothole": "D40",
}
CLASS_ORDER = ["D00", "D10", "D20", "D40"]

# Doğrulama için beklenen değerler (CLAUDE.md, plan.md A tablosu)
EXPECTED = {"images": 38385, "labels": 61082, "D00": 26196, "D10": 11875, "D20": 10617, "D40": 6544}
# datasetninja sitesinde yazan "bu sınıfı içeren görüntü sayısı"
SITE_IMAGES_PER_CLASS = {"D00": 13657, "D10": 7744, "D20": 8412, "D40": 3674}

IMGSZ = 640  # eğitimde modelin göreceği boyut (uzun kenar 640'a küçültülür)
FILE_RE = re.compile(r"^(?P<country>.+)_(?P<num>\d+)\.jpg\.json$")  # ör. Japan_001180.jpg.json


# ---------------------------------------------------------------------------
# Okuma
# ---------------------------------------------------------------------------

def load_annotations(data_root):
    """train ve test klasörlerindeki ann/*.json dosyalarını okuyup iki tablo kurar.

    images: görüntü başına bir satır (bölüm, dosya, ülke, boyut, etiket sayıları)
    boxes : kutu (etiket) başına bir satır (köşe koordinatları, sınıf)
    Ayrıca etiket dosyası olmayan görüntülerin sayısını döndürür (kalite kontrolü için).
    """
    image_rows, box_rows, orphan_images = [], [], {}
    for split in ["train", "test"]:
        ann_dir = data_root / split / "ann"
        # Görüntüler açılmaz; sadece klasördeki dosya adları listelenir.
        img_names = {p.name for p in (data_root / split / "img").iterdir()}
        ann_names = set()

        for path in sorted(ann_dir.glob("*.json")):
            ann = json.loads(path.read_text(encoding="utf-8"))
            img_name = path.name[: -len(".json")]
            ann_names.add(img_name)

            # Ülke iki yerden okunur: dosya adı ve görüntü etiketi (tag). İkisi tutmalı.
            m = FILE_RE.match(path.name)
            name_country = m["country"] if m else None
            tags = [t["name"].replace(" ", "_") for t in ann["tags"]]  # "United States" -> "United_States"
            country = tags[0] if tags else name_country

            width, height = ann["size"]["width"], ann["size"]["height"]
            n_target = 0
            for obj in ann["objects"]:
                cls_name = obj["classTitle"]
                is_target = cls_name in TARGET_CLASSES
                n_target += is_target
                # Dikdörtgen iki köşe noktasıyla saklanıyor: [[x1, y1], [x2, y2]]
                (xa, ya), (xb, yb) = obj["points"]["exterior"]
                box_rows.append({
                    "split": split, "file": img_name, "country": country,
                    "class": TARGET_CLASSES.get(cls_name, cls_name),  # hedef değilse ismi kalır
                    "is_target": is_target,
                    "x1": min(xa, xb), "y1": min(ya, yb), "x2": max(xa, xb), "y2": max(ya, yb),
                    "img_w": width, "img_h": height,
                })

            image_rows.append({
                "split": split, "file": img_name, "country": country, "name_country": name_country,
                "num": int(m["num"]) if m else -1,
                "width": width, "height": height,
                "n_all": len(ann["objects"]),  # tüm etiketler (other corruption dahil)
                "n_target": n_target,          # sadece 4 hedef sınıf
                "has_img": img_name in img_names,
            })

        orphan_images[split] = len(img_names - ann_names)

    return pd.DataFrame(image_rows), pd.DataFrame(box_rows), orphan_images


def add_geometry(boxes):
    """Her kutu için boyut ölçülerini ekler.

    norm_area : kutu alanı / görüntü alanı (0-1). Farklı boyuttaki görüntüleri karşılaştırmak için.
    aspect    : genişlik / yükseklik. >1 yatay (enine çatlak gibi), <1 dikey (boyuna çatlak gibi).
    short_640 : görüntü uzun kenarı 640 olacak şekilde küçültülünce kutunun kısa kenarı kaç piksel kalıyor.
                Çok küçük kalan kutuları model göremeyebilir (Norveç kararı için kritik).
    """
    b = boxes.copy()
    b["w"] = b.x2 - b.x1
    b["h"] = b.y2 - b.y1
    b["norm_area"] = (b.w * b.h) / (b.img_w * b.img_h)
    b["aspect"] = b.w / b.h.where(b.h > 0)
    scale = IMGSZ / np.maximum(b.img_w, b.img_h)
    b["short_640"] = np.minimum(b.w, b.h) * scale
    # Sekans kontrolü için 0-1 aralığına normalize köşeler
    b["nx1"], b["nx2"] = b.x1 / b.img_w, b.x2 / b.img_w
    b["ny1"], b["ny2"] = b.y1 / b.img_h, b.y2 / b.img_h
    return b


# ---------------------------------------------------------------------------
# Yardımcılar
# ---------------------------------------------------------------------------

def save_csv(df, out, name):
    df.to_csv(out / name, encoding="utf-8")


def save_fig(fig, out, name):
    fig.tight_layout()
    fig.savefig(out / name, dpi=120)
    plt.close(fig)


def md_table(df):
    """DataFrame'i markdown tablosuna çevirir (summary.md için; ek paket gerektirmez)."""
    df = df.reset_index()
    lines = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    for row in df.itertuples(index=False):
        lines.append("| " + " | ".join(map(str, row)) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Ölçümler (plan.md Adım 1, madde 1-10)
# ---------------------------------------------------------------------------

def country_table(images, out):
    """1) Ülke başına görüntü sayısı, boyutlar ve boş (arka plan) görüntü oranı.

    Boş (önce): hiç etiketi yok.
    Boş (sonra): 4 hedef sınıftan etiketi yok; yani tek etiketi 'other corruption' olanlar da boşa dönüşür.
    """
    train = images[images.split == "train"]
    t = train.groupby("country").agg(
        train_images=("file", "size"),
        empty_before=("n_all", lambda s: int((s == 0).sum())),
        empty_after=("n_target", lambda s: int((s == 0).sum())),
    )
    t["test_images"] = images[images.split == "test"].groupby("country").size()
    t = t.fillna(0).astype(int)
    t.loc["TOPLAM"] = t.sum()
    t["empty_before_pct"] = (100 * t.empty_before / t.train_images).round(1)
    t["empty_after_pct"] = (100 * t.empty_after / t.train_images).round(1)
    save_csv(t, out, "countries.csv")

    sizes = images.groupby(["split", "country", "width", "height"]).size().rename("images")
    save_csv(sizes.to_frame(), out, "image_sizes.csv")

    fig, ax = plt.subplots(figsize=(9, 4))
    t.drop("TOPLAM")[["empty_before_pct", "empty_after_pct"]].plot.bar(ax=ax)
    ax.set_ylabel("Boş görüntü (%)")
    ax.set_title("Ülke başına boş görüntü oranı (train)")
    ax.legend(["Önce (hiç etiket yok)", "Sonra (4 hedef sınıftan etiket yok)"])
    save_fig(fig, out, "empty_ratio.png")
    return t


def class_by_country(boxes, out):
    """2) Sınıf × ülke etiket sayısı tablosu (hedef sınıflar + atılacak sınıflar)."""
    train = boxes[boxes.split == "train"]
    t = train.pivot_table(index="country", columns="class", aggfunc="size", fill_value=0)
    others = [c for c in t.columns if c not in CLASS_ORDER]
    t = t[CLASS_ORDER + others]
    t.loc["TOPLAM"] = t.sum()
    t["TOPLAM"] = t.sum(axis=1)
    save_csv(t, out, "class_by_country.csv")

    fig, ax = plt.subplots(figsize=(9, 4))
    t.drop("TOPLAM")[CLASS_ORDER].plot.bar(stacked=True, ax=ax)
    ax.set_ylabel("Etiket sayısı")
    ax.set_title("Ülke başına hedef sınıf etiketleri (train)")
    save_fig(fig, out, "class_by_country.png")
    return t


def labels_per_image(images, out):
    """3) Görüntü başına hedef etiket sayısı dağılımı (10 ve üstü tek grupta)."""
    train = images[images.split == "train"].copy()
    train["n"] = train.n_target.clip(upper=10).astype(str).replace("10", "10+")
    order = [str(i) for i in range(10)] + ["10+"]
    t = pd.crosstab(train.country, train.n).reindex(columns=order, fill_value=0)
    t.loc["TOPLAM"] = t.sum()
    save_csv(t, out, "labels_per_image.csv")

    fig, ax = plt.subplots(figsize=(8, 4))
    t.loc["TOPLAM"].plot.bar(ax=ax)
    ax.set_xlabel("Görüntüdeki hedef etiket sayısı")
    ax.set_ylabel("Görüntü sayısı")
    ax.set_title("Görüntü başına etiket sayısı (train)")
    save_fig(fig, out, "labels_per_image.png")
    return t


def box_geometry(boxes, out):
    """4) Kutu geometrisi: sınıf ve ülke başına medyan boyutlar; 640'ta küçük kalan kutular."""
    tb = boxes[(boxes.split == "train") & boxes.is_target]

    stats = tb.groupby(["country", "class"]).agg(
        boxes=("file", "size"),
        median_area_pct=("norm_area", lambda s: round(100 * s.median(), 2)),
        median_w_px=("w", "median"),
        median_h_px=("h", "median"),
        median_aspect=("aspect", lambda s: round(s.median(), 2)),
    )
    save_csv(stats, out, "box_stats.csv")

    # Kısa kenarı 8 / 16 pikselin altına düşen kutuların oranı
    def small(group):
        return pd.Series({
            "boxes": len(group),
            "median_short_640": round(group.short_640.median(), 1),
            "pct_under_8px": round(100 * (group.short_640 < 8).mean(), 1),
            "pct_under_16px": round(100 * (group.short_640 < 16).mean(), 1),
        })

    small_t = tb.groupby("country")[["short_640"]].apply(small)
    small_t.loc["TOPLAM"] = small(tb)
    small_t["boxes"] = small_t["boxes"].astype(int)
    save_csv(small_t, out, "small_boxes_640.csv")

    countries = sorted(tb.country.unique())
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.boxplot([100 * tb.norm_area[tb.country == c] for c in countries], showfliers=False)
    ax.set_xticks(range(1, len(countries) + 1), countries, rotation=45)
    ax.set_yscale("log")
    ax.set_ylabel("Kutu alanı / görüntü alanı (%)")
    ax.set_title("Ülke başına kutu büyüklüğü (hedef sınıflar)")
    save_fig(fig, out, "box_area.png")
    return stats, small_t


def quality_checks(images, boxes, orphans, out):
    """5) Kalite kontrolü: hatalı kutular ve eşleşmeyen dosyalar."""
    w, h = boxes.x2 - boxes.x1, boxes.y2 - boxes.y1
    rows = [
        ("Görüntü dışına taşan kutu", int(((boxes.x1 < 0) | (boxes.y1 < 0) |
                                           (boxes.x2 > boxes.img_w) | (boxes.y2 > boxes.img_h)).sum())),
        ("Sıfır genişlik/yükseklikli kutu", int(((w <= 0) | (h <= 0)).sum())),
        ("Görüntüsü olmayan etiket dosyası", int((~images.has_img).sum())),
        ("Etiket dosyası olmayan görüntü", sum(orphans.values())),
        ("Dosya adı ile ülke etiketi farklı", int((images.country != images.name_country).sum())),
    ]
    t = pd.DataFrame(rows, columns=["check", "count"]).set_index("check")
    save_csv(t, out, "quality.csv")
    return t


def images_per_class(boxes, out):
    """6) Her sınıfın kaç farklı görüntüde geçtiği; datasetninja değerleriyle karşılaştırma."""
    tb = boxes[(boxes.split == "train") & boxes.is_target]
    t = tb.groupby("class").file.nunique().reindex(CLASS_ORDER).rename("images").to_frame()
    t["site"] = pd.Series(SITE_IMAGES_PER_CLASS)
    t["diff"] = t.images - t.site
    save_csv(t, out, "images_per_class.csv")
    return t


def box_style_by_country(boxes, out):
    """7) Norveç (CVAT ile etiketlenmiş) kutu stili diğer ülkelerden farklı mı?

    Kutuların en-boy oranı ve görüntü genişliğine göre genişliği ülke ülke yan yana çizilir.
    Sayısal değerler box_stats.csv'de.
    """
    tb = boxes[(boxes.split == "train") & boxes.is_target]
    countries = sorted(tb.country.unique())
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].boxplot([tb.aspect[tb.country == c].dropna() for c in countries], showfliers=False)
    axes[0].set_yscale("log")
    axes[0].set_ylabel("Genişlik / yükseklik")
    axes[0].set_title("Kutu en-boy oranı")
    axes[1].boxplot([(tb.w / tb.img_w)[tb.country == c] for c in countries], showfliers=False)
    axes[1].set_ylabel("Kutu genişliği / görüntü genişliği")
    axes[1].set_title("Kutu göreli genişliği")
    for ax in axes:
        ax.set_xticks(range(1, len(countries) + 1), countries, rotation=45)
    save_fig(fig, out, "box_style_by_country.png")


def china_drone_summary(images, boxes, out):
    """8) China_Drone (yukarıdan çekim) ile diğer görüntülerin karşılaştırması."""
    def summarize(imgs, bxs):
        nonempty = imgs[imgs.n_target > 0]
        row = {
            "images": len(imgs),
            "empty_after_pct": round(100 * (imgs.n_target == 0).mean(), 1),
            "boxes_per_nonempty_image": round(nonempty.n_target.mean(), 2),
            "median_area_pct": round(100 * bxs.norm_area.median(), 2),
            "median_aspect": round(bxs.aspect.median(), 2),
        }
        share = bxs["class"].value_counts(normalize=True)
        for c in CLASS_ORDER:
            row[f"{c}_pct"] = round(100 * share.get(c, 0), 1)
        return row

    ti = images[images.split == "train"]
    tb = boxes[(boxes.split == "train") & boxes.is_target]
    drone = ti.country == "China_Drone"
    t = pd.DataFrame({
        "China_Drone": summarize(ti[drone], tb[tb.country == "China_Drone"]),
        "Diğer (Drone hariç)": summarize(ti[~drone], tb[tb.country != "China_Drone"]),
    })
    save_csv(t, out, "china_drone.csv")
    return t


def split_preview(images, boxes, seed, out):
    """9) Katmanlı %80/10/10 bölme önizlemesi (dosya kopyalanmaz, liste kaydedilmez).

    Katman = ülke + boş/dolu. Her katman ayrı karıştırılıp bölünür; böylece her parçada
    ülke ve boş görüntü oranı aynı kalır. Burada sadece sınıf dağılımının dengeli olup olmadığına bakılır.
    """
    train = images[images.split == "train"].copy()
    train["stratum"] = train.country + "_" + np.where(train.n_target > 0, "dolu", "bos")
    rng = np.random.default_rng(seed)
    train["part"] = ""
    for _, idx in sorted(train.groupby("stratum").groups.items()):
        idx = rng.permutation(np.asarray(idx))
        n_train, n_val = round(len(idx) * 0.8), round(len(idx) * 0.1)
        train.loc[idx[:n_train], "part"] = "train"
        train.loc[idx[n_train:n_train + n_val], "part"] = "val"
        train.loc[idx[n_train + n_val:], "part"] = "test"

    tb = boxes[(boxes.split == "train") & boxes.is_target].merge(train[["file", "part"]], on="file")
    t = tb.pivot_table(index="part", columns="class", aggfunc="size", fill_value=0)[CLASS_ORDER]
    share = (100 * t.div(t.sum(axis=1), axis=0)).round(1).add_suffix("_pct")
    t = t.join(share)
    t["images"] = train.groupby("part").size()
    t["empty_pct"] = train.groupby("part").n_target.apply(lambda s: round(100 * (s == 0).mean(), 1))
    t = t.reindex(["train", "val", "test"])
    save_csv(t, out, "split_preview.csv")
    return t


def box_iou(a, b):
    """İki kutunun örtüşme oranı (IoU) = kesişim alanı / birleşim alanı. 0: hiç örtüşmüyor, 1: aynı kutu."""
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def pair_score(boxes_a, boxes_b):
    """İki görüntünün kutu benzerliği (0-1).

    A'daki her kutu için B'de aynı sınıftan en çok örtüşen kutunun IoU'su alınır, ortalaması hesaplanır;
    aynısı B'den A'ya da yapılır, ikisinin ortalaması skor olur.
    """
    def one_way(src, dst):
        return np.mean([max((box_iou(s[1:], d[1:]) for d in dst if d[0] == s[0]), default=0.0) for s in src])
    return (one_way(boxes_a, boxes_b) + one_way(boxes_b, boxes_a)) / 2


def sequence_check(images, boxes, seed, out, threshold=0.5):
    """10) Sekans (ardışık kare) kontrolü.

    Dosya adlarında çekim bilgisi yok. Görüntüler bir videodan art arda alınmış karelerse,
    numarası ardışık iki görüntünün (n, n+1) kutuları rastgele iki görüntüye göre çok daha benzer olur.
    Ardışık çiftlerin ve aynı sayıda rastgele çiftin benzerlik skoru karşılaştırılır.
    Bu bir kanıt değil, göstergedir. Fark büyükse bölme ardışık numara blokları halinde yapılmalı (Adım 3).
    """
    tb = boxes[(boxes.split == "train") & boxes.is_target]
    by_file = defaultdict(list)
    for f, cls, x1, y1, x2, y2 in zip(tb.file, tb["class"], tb.nx1, tb.ny1, tb.nx2, tb.ny2):
        by_file[f].append((cls, x1, y1, x2, y2))

    rnd = random.Random(seed)
    train = images[(images.split == "train") & (images.n_target > 0)]
    rows, all_consec, all_random = [], [], []
    for country, g in train.groupby("country"):
        num_to_file = dict(zip(g.num, g.file))
        files = list(num_to_file.values())
        consec = [pair_score(by_file[num_to_file[n]], by_file[num_to_file[n + 1]])
                  for n in num_to_file if n + 1 in num_to_file]
        random_pairs = [rnd.sample(files, 2) for _ in range(len(consec))]
        rand = [pair_score(by_file[a], by_file[b]) for a, b in random_pairs]
        all_consec += consec
        all_random += rand
        rows.append((country, consec, rand))
    rows.append(("TOPLAM", all_consec, all_random))

    t = pd.DataFrame([{
        "country": c, "pairs": len(cs),
        "consec_mean": round(np.mean(cs), 3), "random_mean": round(np.mean(rs), 3),
        f"consec_pct_ge_{threshold}": round(100 * np.mean(np.array(cs) >= threshold), 1),
        f"random_pct_ge_{threshold}": round(100 * np.mean(np.array(rs) >= threshold), 1),
    } for c, cs, rs in rows]).set_index("country")
    save_csv(t, out, "sequence_check.csv")
    return t


# ---------------------------------------------------------------------------
# Doğrulama ve özet
# ---------------------------------------------------------------------------

def verify_totals(images, boxes):
    """Toplamların CLAUDE.md'deki değerlerle tutup tutmadığını kontrol eder."""
    train_boxes = boxes[boxes.split == "train"]
    found = {
        "images": int((images.split == "train").sum()),
        "labels": len(train_boxes),
        **{c: int((train_boxes["class"] == c).sum()) for c in CLASS_ORDER},
    }
    t = pd.DataFrame({"expected": EXPECTED, "found": found})
    t["ok"] = np.where(t.expected == t.found, "OK", "UYARI")
    return t


def key_findings(countries, small, sequence, drone, split, boxes):
    """Öne çıkan bulgular: sayılar tablolardan alınır, yorum metni sabittir (Adım 2 kararlarına girdi)."""
    others_8 = small.drop(["Norway", "TOPLAM"]).pct_under_8px.max()
    seq = sequence.loc["TOPLAM"]
    pct_cols = [f"{c}_pct" for c in CLASS_ORDER]
    split_gap = (split[pct_cols].max() - split[pct_cols].min()).max()
    zero = boxes[(boxes.x2 - boxes.x1 <= 0) | (boxes.y2 - boxes.y1 <= 0)]
    zero_list = ", ".join(f"`{f}` ({c})" for f, c in zip(zero.file, zero["class"]))
    d, o = drone["China_Drone"], drone["Diğer (Drone hariç)"]
    c = countries
    return [
        f"1. **Norveç'te küçük nesne sorunu:** {IMGSZ}'a küçültülünce kısa kenarı 8 px altına düşen kutu oranı "
        f"%{small.loc['Norway', 'pct_under_8px']}, 16 px altına düşen %{small.loc['Norway', 'pct_under_16px']} "
        f"(diğer ülkelerde 8 px altı en fazla %{others_8}). Norveç boyut kararının dayanağı.",
        f"2. **Sekans sızıntısı işareti yok:** ardışık çiftlerin ortalama benzerliği {seq.consec_mean}, "
        f"rastgele çiftlerin {seq.random_mean}. Rastgele katmanlı bölme yeterli görünüyor. "
        "Sınır: araç hareketiyle kutular kayıyorsa IoU bunu yakalayamayabilir; bu bir göstergedir, kanıt değil.",
        f"3. **`other corruption` atılınca boş oran artıyor:** Japonya %{c.loc['Japan', 'empty_before_pct']} → "
        f"%{c.loc['Japan', 'empty_after_pct']}, Hindistan %{c.loc['India', 'empty_before_pct']} → "
        f"%{c.loc['India', 'empty_after_pct']}, toplam %{c.loc['TOPLAM', 'empty_before_pct']} → "
        f"%{c.loc['TOPLAM', 'empty_after_pct']}.",
        f"4. **China_Drone farklı:** D10 payı %{d['D10_pct']} (diğerlerinde %{o['D10_pct']}), "
        f"D40 payı %{d['D40_pct']} (diğerlerinde %{o['D40_pct']}).",
        f"5. **Bölme önizlemesi dengeli:** train/val/test sınıf oranları en fazla {split_gap:.1f} puan farklı.",
        f"6. **Hatalı kutu:** {len(zero)} adet sıfır boyutlu kutu ({zero_list}); Adım 3'te atılacak.",
    ]


def main():
    parser = argparse.ArgumentParser(description="RDD2022 etiket analizi (görüntü açmaz)")
    parser.add_argument("--data-root", default="data/rdd2022", help="train/ ve test/ klasörlerini içeren klasör")
    parser.add_argument("--out", default="docs/analysis", help="toplu tablolar, grafikler, summary.md (git'e girer)")
    parser.add_argument("--raw-out", default="data/analysis", help="ham images.csv ve boxes.csv (git dışı)")
    parser.add_argument("--seed", type=int, default=42, help="bölme önizlemesi ve rastgele çiftler için")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")  # Windows terminalinde Türkçe karakterler için
    out, raw_out = Path(args.out), Path(args.raw_out)
    out.mkdir(parents=True, exist_ok=True)
    raw_out.mkdir(parents=True, exist_ok=True)

    print("Etiket dosyaları okunuyor...")
    images, boxes, orphans = load_annotations(Path(args.data_root))
    boxes = add_geometry(boxes)
    images.to_csv(raw_out / "images.csv", index=False, encoding="utf-8")
    boxes.to_csv(raw_out / "boxes.csv", index=False, encoding="utf-8")

    print("Ölçümler hesaplanıyor...")
    checks = verify_totals(images, boxes)
    countries = country_table(images, out)
    class_by_country(boxes, out)
    labels_per_image(images, out)
    _, small = box_geometry(boxes, out)
    quality = quality_checks(images, boxes, orphans, out)
    per_class = images_per_class(boxes, out)
    box_style_by_country(boxes, out)
    drone = china_drone_summary(images, boxes, out)
    split = split_preview(images, boxes, args.seed, out)
    sequence = sequence_check(images, boxes, args.seed, out)

    # Terminal özeti ve summary.md aynı bölümlerden oluşur
    sections = [
        ("Doğrulama (beklenen = CLAUDE.md)", checks),
        ("Ülkeler: görüntü sayısı ve boş oranı", countries[["train_images", "test_images",
                                                           "empty_before_pct", "empty_after_pct"]]),
        (f"{IMGSZ}'a küçültülünce küçük kalan kutular", small),
        ("Sınıf başına görüntü (site ile)", per_class),
        ("Kalite kontrolü", quality),
        ("China_Drone karşılaştırması", drone),
        ("Bölme önizlemesi (seed %d)" % args.seed, split),
        ("Sekans kontrolü (ardışık vs rastgele çift)", sequence),
    ]
    md = ["# Veri analizi özeti (Adım 1)", "",
          "`src/analysis/analyze_dataset.py` ile üretildi. Sadece `train|test/ann/*.json` okundu.", ""]
    for title, df in sections:
        print(f"\n=== {title} ===")
        print(df.to_string())
        md += [f"## {title}", "", md_table(df), ""]
    md += ["## Öne çıkan bulgular", ""] + key_findings(countries, small, sequence, drone, split, boxes) + [""]
    (out / "summary.md").write_text("\n".join(md), encoding="utf-8")

    if (checks.ok != "OK").any():
        print("\nUYARI: bazı toplamlar beklenenle tutmuyor, yukarıdaki doğrulama tablosuna bakın.")
    print(f"\nÇıktılar: {out}/ (git'e girer), {raw_out}/ (git dışı)")


if __name__ == "__main__":
    main()
