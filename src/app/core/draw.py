"""
Tespit kutularını görüntünün üzerine çizer.

Ultralytics'in hazır `result.plot()` fonksiyonu yerine kendi çizimimiz:
- Renkler bizim sabit paletimiz (classes.py); kutu, tablo ve lejant aynı renkte.
- Etiket kısa ve dilden bağımsız: "D40 0,82". Türkçe karakter (ç, ğ, ş) çizilmediği için yazı tipi sorunu yok;
  Ultralytics ASCII dışı etiket görünce internetten yazı tipi indirmeye çalışır, sunumda internet olmayabilir.
- Pillow'un içinde gelen yazı tipi kullanılır (ImageFont.load_default), dışarıdan dosya gerekmez.
"""

from PIL import Image, ImageDraw, ImageFont

from core.classes import CLASS_COLORS


def format_conf(conf, lang):
    """Güven skorunu 2 basamakla yazar; Türkçede ondalık ayıracı virgül (0,82), İngilizcede nokta (0.82)."""
    text = f"{conf:.2f}"
    return text.replace(".", ",") if lang == "tr" else text


def draw_detections(rgb, detections, lang):
    """RGB numpy görüntüye kutuları ve etiketleri çizer; yeni bir RGB PIL görüntüsü döndürür (orijinal değişmez)."""
    img = Image.fromarray(rgb).copy()
    draw = ImageDraw.Draw(img)
    long_side = max(img.size)
    width = max(2, round(long_side / 400))  # çizgi kalınlığı görüntü boyuyla orantılı (1280 px → 3 px)
    font = ImageFont.load_default(size=max(12, round(long_side / 50)))  # yazı boyu da orantılı

    # Düşük güvenli kutular önce çizilir; üst üste binenlerde yüksek güvenli olan üstte kalsın
    for d in sorted(detections, key=lambda d: d["conf"]):
        color = CLASS_COLORS[d["code"]]
        x1, y1, x2, y2 = d["box"]
        draw.rectangle((x1, y1, x2, y2), outline=color, width=width)

        label = f'{d["code"]} {format_conf(d["conf"], lang)}'
        left, top, right, bottom = draw.textbbox((0, 0), label, font=font)  # yazının kapladığı alan
        tw, th = right - left, bottom - top
        pad = max(2, width)
        # Etiket kutunun üstüne; görüntünün üst kenarına taşarsa kutunun içine yazılır
        ty = y1 - th - 2 * pad if y1 - th - 2 * pad >= 0 else y1
        draw.rectangle((x1, ty, x1 + tw + 2 * pad, ty + th + 2 * pad), fill=color)  # renkli etiket zemini
        draw.text((x1 + pad - left, ty + pad - top), label, fill=(255, 255, 255), font=font)  # beyaz yazı
    return img
