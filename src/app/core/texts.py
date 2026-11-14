"""
Arayüzün tüm metinleri, iki dilde (Türkçe / İngilizce).

Sayfalar metni doğrudan yazmaz, buradan `t("anahtar")` ile alır. Böylece:
- dil değiştirmek tek bir ayarla olur (kenar çubuğundaki dil seçici),
- bir metni düzeltmek için tek dosyaya bakmak yeter,
- 7b'de eklenecek Video / Kamera sayfaları aynı sözlüğü kullanır.
Yeni bir metin eklerken anahtarı İKİ dile de ekleyin (check_keys() eksikleri bulur).
"""

import streamlit as st

DEFAULT_LANG = "tr"  # varsayılan dil Türkçe (kullanıcı kararı, 2026-11-14)
LANGS = {"tr": "Türkçe", "en": "English"}  # dil kodu → seçicide görünen ad

# Sınıf adları: model sınıf NUMARASI döndürür (0-3); numara → kod (D00...) eşlemesi classes.py'de.
# Burada kod → okunur ad. Görüntü üzerindeki etiketlerde dilden bağımsız kısa kod kullanılır.
CLASS_NAMES = {
    "tr": {
        "D00": "Boyuna çatlak",
        "D10": "Enine çatlak",
        "D20": "Timsah çatlağı",
        "D40": "Çukur",
    },
    "en": {
        "D00": "Longitudinal crack",
        "D10": "Transverse crack",
        "D20": "Alligator crack",
        "D40": "Pothole",
    },
}

# Ülke adları: örnek görüntülerin altında gösterilir. Anahtar, RDD2022 dosya adındaki ülke kısmı
# ("China_MotorBike_002019.jpg" → "China_MotorBike").
COUNTRY_NAMES = {
    "tr": {
        "China_MotorBike": "Çin",
        "China_Drone": "Çin (drone)",
        "Czech": "Çek Cumhuriyeti",
        "India": "Hindistan",
        "Japan": "Japonya",
        "Norway": "Norveç",
        "United_States": "ABD",
    },
    "en": {
        "China_MotorBike": "China",
        "China_Drone": "China (drone)",
        "Czech": "Czech Republic",
        "India": "India",
        "Japan": "Japan",
        "Norway": "Norway",
        "United_States": "United States",
    },
}

TEXTS = {
    "tr": {
        # Başlık ve açıklama (metin: kullanıcı, 2026-11-14)
        "page_title": "Yol Hasarı Tespiti",  # tarayıcı sekmesindeki başlık
        "title": "Yol Hasarı Tespiti",
        "intro": "Bir yol fotoğrafı yükleyin; model boyuna, enine ve timsah çatlaklarını ve çukurları işaretler. "
                 "Model, RDD2022 veri setindeki altı ülkenin görüntüleriyle eğitilmiş YOLO26s'tir "
                 "(doğrulama mAP50: 0,609).",
        "nav_image": "Görüntü",  # gezinme menüsündeki sayfa adı
        # Kenar çubuğu
        "lang_label": "Dil",
        "conf_label": "Güven eşiği",
        "conf_help": "Bu değerin altındaki tespitler gösterilmez. Düşük eşik daha çok hasar bulur ama yanlış "
                     "alarmı artırır; yüksek eşik tersini yapar.",
        "classes_label": "Gösterilecek sınıflar",
        "model_info": "Model: {model} · imgsz {imgsz} · {device}",
        # Girdi
        "tab_upload": "Görüntü yükle",
        "tab_examples": "Örnek görüntüler",
        "upload_label": "Yol fotoğrafı seçin (JPG veya PNG; birden fazla eklenebilir)",
        "upload_pick_label": "Gösterilecek fotoğraf",
        "examples_caption": "Örnekler RDD2022 veri setinin etiketsiz resmî test klasöründen alınmıştır; "
                            "eğitimde kullanılmadı.",
        "examples_empty": "Örnek görüntü bulunamadı.",
        "selected_example": "Seçili örnek: {country} ({i}/{n})",
        "selected_upload": "Yüklenen fotoğraf: {name}",
        "no_input": "Başlamak için bir görüntü yükleyin veya bir örnek seçin.",
        "read_error": "Görüntü okunamadı. Lütfen JPG veya PNG dosyası seçin.",
        "model_missing": "Model dosyası bulunamadı: {path}",
        "loading_model": "Model yükleniyor...",
        "running": "Görüntü işleniyor...",
        # Sonuç
        "original": "Orijinal",
        "detections": "Tespitler",
        "summary": "Toplam {n} · {ms:.0f} ms",
        "no_detections": "Bu eşikte hasar tespit edilmedi.",
        "col_class": "Sınıf",
        "col_code": "Kod",
        "col_conf": "Güven",
        "col_size": "Kutu boyutu (px)",
        # Alt not: 1. satır sorumluluk notu, 2. satır veri seti atfı (CC BY-SA 4.0 atıf istiyor)
        "footer": "Bu araç karar desteği içindir; son karar insandadır.",
        "footer_dataset": "Veri seti: RDD2022 (Arya vd., 2022), CC BY-SA 4.0.",
    },
    "en": {
        "page_title": "Road Damage Detection",
        "title": "Road Damage Detection",
        "intro": "Upload a road photo; the model marks longitudinal, transverse and alligator cracks and potholes. "
                 "The model is YOLO26s, trained on images from six countries in the RDD2022 dataset "
                 "(validation mAP50: 0.609).",
        "nav_image": "Image",
        "lang_label": "Language",
        "conf_label": "Confidence threshold",
        "conf_help": "Detections below this value are hidden. A lower threshold finds more damage but raises "
                     "false alarms; a higher threshold does the opposite.",
        "classes_label": "Classes to show",
        "model_info": "Model: {model} · imgsz {imgsz} · {device}",
        "tab_upload": "Upload image",
        "tab_examples": "Example images",
        "upload_label": "Choose a road photo (JPG or PNG; you can add more than one)",
        "upload_pick_label": "Photo to show",
        "examples_caption": "Examples are taken from the unlabeled official test folder of the RDD2022 dataset; "
                            "they were not used in training.",
        "examples_empty": "No example images found.",
        "selected_example": "Selected example: {country} ({i}/{n})",
        "selected_upload": "Uploaded photo: {name}",
        "no_input": "Upload an image or pick an example to start.",
        "read_error": "The image could not be read. Please choose a JPG or PNG file.",
        "model_missing": "Model file not found: {path}",
        "loading_model": "Loading model...",
        "running": "Processing image...",
        "original": "Original",
        "detections": "Detections",
        "summary": "Total {n} · {ms:.0f} ms",
        "no_detections": "No damage detected at this threshold.",
        "col_class": "Class",
        "col_code": "Code",
        "col_conf": "Confidence",
        "col_size": "Box size (px)",
        "footer": "This tool is for decision support; the final decision rests with a human.",
        "footer_dataset": "Dataset: RDD2022 (Arya et al., 2022), CC BY-SA 4.0.",
    },
}


def get_lang():
    """Seçili dil kodunu döndürür ("tr" / "en"); henüz seçilmediyse varsayılan dil."""
    return st.session_state.get("lang", DEFAULT_LANG)


def t(key, **kwargs):
    """Seçili dildeki metni döndürür; {yer tutucu}lar kwargs ile doldurulur.

    Anahtar eksikse hata vermek yerine anahtarın kendisini gösterir: sunumda sayfa çökmesin,
    eksik metin ekranda görünür kalsın.
    """
    text = TEXTS.get(get_lang(), {}).get(key, key)
    return text.format(**kwargs) if kwargs else text


def class_name(code):
    """Sınıf kodunun (ör. "D40") seçili dildeki okunur adını döndürür."""
    return CLASS_NAMES[get_lang()].get(code, code)


def country_name(code):
    """Ülke kodunun (ör. "China_MotorBike") seçili dildeki adını döndürür; bilinmeyen kodu olduğu gibi gösterir."""
    return COUNTRY_NAMES[get_lang()].get(code, code)


def check_keys():
    """İki dilin anahtar kümelerini karşılaştırır; bir dilde eksik olan anahtarları döndürür (test için)."""
    tr, en = set(TEXTS["tr"]), set(TEXTS["en"])
    return {"yalnız tr'de": sorted(tr - en), "yalnız en'de": sorted(en - tr)}
