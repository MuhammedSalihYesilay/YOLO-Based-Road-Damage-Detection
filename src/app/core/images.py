"""
Görüntü okuma ve hazırlama: yüklenen dosyayı modele ve ekrana uygun hale getirir.

Kurallar:
- Telefon fotoğrafları çoğu zaman yan kaydedilir; doğru yön EXIF bilgisindedir → exif_transpose ile düzeltilir.
- Uzun kenar 1280'den büyükse 1280'e küçültülür. Norveç görüntüleri (4040 px) eğitimden önce de aynı şekilde
  1280'e küçültülmüştü (kararlar.md 2026-10-27); model zaten 1024'e indirdiği için doğruluk kaybı yok,
  çizim ve gösterim hızlanır.
- Bu modül RGB numpy dizisi döndürür. Ultralytics numpy girdiyi BGR beklediği için çevirme model.py'de yapılır.
"""

import io

import numpy as np
from PIL import Image, ImageOps

MAX_SIDE = 1280  # uzun kenar sınırı (Norveç eğitim ön işlemesiyle aynı)


def load_image(data):
    """Dosya baytlarını okur; yönü düzeltilmiş, gerekirse küçültülmüş RGB numpy dizisi döndürür.

    Okunamayan dosyada None döndürür (sayfa hata mesajı gösterir, çökmez).
    """
    try:
        img = Image.open(io.BytesIO(data))
        img = ImageOps.exif_transpose(img)  # EXIF yön bilgisine göre döndür
        img = img.convert("RGB")  # PNG'deki saydamlık (RGBA) veya gri tonlu görüntüler de 3 kanala çevrilir
    except Exception:
        return None
    return np.asarray(limit_size(img))


def limit_size(img, max_side=MAX_SIDE):
    """Uzun kenar max_side'dan büyükse en-boy oranını koruyarak küçültür (PIL görüntüsü alır/döndürür)."""
    w, h = img.size
    scale = max_side / max(w, h)
    if scale >= 1:
        return img  # zaten küçük, dokunma
    return img.resize((round(w * scale), round(h * scale)), Image.Resampling.LANCZOS)
