"""
Adım 7a — Arayüzün "Örnek görüntüler" sekmesi için demo adaylarını üretir.

Ne yapar:
1. RDD2022'nin etiketsiz resmî test klasöründen (data/rdd2022/test/img) her ülkeden rastgele N aday seçer (seed 42).
   Bu klasör eğitimde hiç kullanılmadı; kendi test bölmemize (data/yolo test) dokunulmaz.
2. Her adayda e5 modeliyle tahmin yapar. Ayarlar arayüzle birebir aynı olsun diye arayüzün kendi modülleri
   kullanılır: okuma/küçültme core/images.py, tahmin core/model.py (imgsz 1024, quantize=32 yani FP32,
   eşik 0,25), çizim core/draw.py (aynı sınıf renkleri).
3. Çıktılar (git dışı, runs/demo_secim/):
   - adaylar.csv + temas_sayfasi.png: genel adaylar; her ülke bir satır, her küçük resmin üstünde büyük numara,
     ülke ve tespit özeti. Görüntüler tek tek açılmadan bu sayfadan numarayla seçim yapılır.
   - (--cukur) adaylar_cukur.csv + temas_sayfasi_cukur.png: çukur (D40) adayları. Daha geniş örneklem (ülke başına
     ~100, ABD hariç) taranır, D40 bulunanlar en yüksek D40 güveni ve kutu boyutuna göre sıralanır, en iyi 8'i
     gösterilir. Numaralar genel adaylardan sonra devam eder (#49...). Genel adaylarda zaten olan görüntüler atlanır.

ABD neden hariç (çukur modunda): ABD görüntülerinde Google filigranı var; public repodaki demo setine ABD görüntüsü
konmuyor (kararlar.md 2026-11-14).

Çalıştırma (repo kökünden):
  venv\\Scripts\\python.exe src/data/select_demo_images.py           # genel adaylar (48)
  venv\\Scripts\\python.exe src/data/select_demo_images.py --cukur   # çukur adayları (8)
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]  # repo kökü (src/data/select_demo_images.py → 2 üst klasör)
sys.path.insert(0, str(ROOT / "src" / "app"))  # arayüzün core/ modüllerini içe aktarabilmek için

from ultralytics import YOLO  # noqa: E402  (sys.path ayarından sonra içe aktarılmalı)

from core.classes import CLASS_CODES  # noqa: E402
from core.draw import draw_detections, format_conf  # noqa: E402
from core.images import load_image  # noqa: E402
from core.model import DEFAULT_CONF, WEIGHTS, filter_detections, predict  # noqa: E402

CELL = 420  # temas sayfasında bir küçük resmin kare alanı (piksel)
HEADER = 74  # küçük resmin üstündeki yazı şeridinin yüksekliği
GAP = 12  # hücreler arası boşluk
POTHOLE = "D40"  # çukur sınıfının kodu


def country_of(path):
    """Dosya adından ülkeyi çıkarır: "China_MotorBike_001977.jpg" → "China_MotorBike"."""
    return path.stem.rsplit("_", 1)[0]


def sample_candidates(test_dir, per_country, seed, exclude_countries=()):
    """Her ülkeden per_country kadar rastgele görüntü seçer; ülke adına göre sıralı liste döndürür."""
    by_country = {}
    for p in sorted(test_dir.glob("*.jpg")):  # sıralı liste: aynı seed her bilgisayarda aynı seçimi verir
        if country_of(p) not in exclude_countries:
            by_country.setdefault(country_of(p), []).append(p)
    rng = np.random.default_rng(seed)
    picked = []
    for country in sorted(by_country):
        files = by_country[country]
        idx = rng.choice(len(files), size=min(per_country, len(files)), replace=False)
        picked.extend(files[i] for i in sorted(idx))
    return picked


def summary_text(dets):
    """Tespit özetini kısa metin yapar: "D00 2 · D40 1" (tespit yoksa "tespit yok")."""
    parts = [f"{c} {n}" for c in CLASS_CODES if (n := sum(d["code"] == c for d in dets))]
    return " · ".join(parts) if parts else "tespit yok"


def box_area_frac(d, shape):
    """Kutunun görüntü alanına oranı (0-1): kutu boyutu görüntü boyundan bağımsız karşılaştırılsın diye."""
    x1, y1, x2, y2 = d["box"]
    return (x2 - x1) * (y2 - y1) / (shape[0] * shape[1])


def run_on(model, path):
    """Bir görüntüyü arayüzle aynı şekilde okur ve tahmin eder; (rgb, eşikten geçen tespitler) döndürür."""
    rgb = load_image(path.read_bytes())  # arayüzle aynı okuma (EXIF + uzun kenar ≤ 1280)
    dets, _ = predict(model, rgb)  # arayüzle aynı tahmin (imgsz 1024, FP32, ham eşik 0,05)
    return rgb, filter_detections(dets, DEFAULT_CONF, CLASS_CODES)  # arayüzün varsayılan eşiği 0,25


def make_row(no, path, dets):
    """CSV'nin bir satırı: no, dosya, ülke, sınıf başına sayı, toplam, en yüksek güven."""
    row = {"no": no, "dosya": path.name, "ulke": country_of(path)}
    row.update({c: sum(d["code"] == c for d in dets) for c in CLASS_CODES})
    row["toplam"] = len(dets)
    row["en_yuksek_guven"] = format_conf(max(d["conf"] for d in dets), "tr") if dets else ""
    return row


def make_cell(drawn, no, line1, line2):
    """Bir hücre çizer: üstte büyük numara + iki satır bilgi, altta kutulu görüntü (kareye sığdırılmış)."""
    cell = Image.new("RGB", (CELL, HEADER + CELL), "white")
    d = ImageDraw.Draw(cell)
    big = ImageFont.load_default(size=40)  # numara: uzaktan okunacak kadar büyük
    small = ImageFont.load_default(size=19)
    d.text((6, 4), f"#{no}", fill=(20, 20, 20), font=big)
    d.text((100, 8), line1, fill=(60, 60, 60), font=small)
    d.text((100, 38), line2, fill=(20, 20, 20), font=small)

    thumb = drawn.copy()
    thumb.thumbnail((CELL, CELL))  # en-boy oranı korunarak küçültülür (Norveç geniş, diğerleri kare)
    cell.paste(thumb, ((CELL - thumb.width) // 2, HEADER + (CELL - thumb.height) // 2))
    return cell


def save_sheet(cells, row_keys, path):
    """Hücreleri temas sayfasına dizer: aynı row_key'e sahip hücreler aynı satıra (ör. her ülke bir satır)."""
    keys = list(dict.fromkeys(row_keys))  # sırayı koruyarak tekil satır anahtarları
    ncols = max(row_keys.count(k) for k in keys)
    sheet = Image.new("RGB", (GAP + ncols * (CELL + GAP), GAP + len(keys) * (HEADER + CELL + GAP)),
                      (225, 225, 225))  # açık gri zemin: hücreler birbirinden ayrılsın
    col_of = {}
    for cell, k in zip(cells, row_keys):
        r, c = keys.index(k), col_of.get(k, 0)
        col_of[k] = c + 1
        sheet.paste(cell, (GAP + c * (CELL + GAP), GAP + r * (HEADER + CELL + GAP)))
    sheet.save(path)


def general(model, args, out):
    """Genel adaylar: ülke başına per_country görüntü, hepsi gösterilir (her ülke bir satır)."""
    candidates = sample_candidates(Path(args.test_dir), args.per_country, args.seed)
    print(f"{len(candidates)} aday, eşik {DEFAULT_CONF}")
    rows, cells = [], []
    for no, path in enumerate(candidates, start=1):
        rgb, dets = run_on(model, path)
        rows.append(make_row(no, path, dets))
        cells.append(make_cell(draw_detections(rgb, dets, "tr"), no, country_of(path), summary_text(dets)))
        print(f"#{no:>2} {path.name:<28} {summary_text(dets)}")
    pd.DataFrame(rows).to_csv(out / "adaylar.csv", index=False, encoding="utf-8-sig")  # utf-8-sig: Excel uyumu
    save_sheet(cells, [r["ulke"] for r in rows], out / "temas_sayfasi.png")
    print(f"Çıktılar: {out / 'adaylar.csv'}, {out / 'temas_sayfasi.png'}")


def pothole(model, args, out):
    """Çukur adayları: geniş örneklemde D40 bulunanları sıralar, en iyi top_n'i gösterir (tek satır)."""
    general_csv = out / "adaylar.csv"
    already = set(pd.read_csv(general_csv).dosya) if general_csv.exists() else set()  # genelde gösterilenler
    start_no = (len(already) + 1) if already else 1  # numaralar genel adaylardan sonra devam eder (#49...)

    candidates = [p for p in sample_candidates(Path(args.test_dir), args.wide_per_country, args.seed,
                                               exclude_countries=args.exclude)
                  if p.name not in already]
    print(f"{len(candidates)} görüntü taranıyor (ülke başına {args.wide_per_country}, hariç: {args.exclude})")

    found = []  # D40 bulunan görüntüler
    for i, path in enumerate(candidates, start=1):
        rgb, dets = run_on(model, path)
        pots = [d for d in dets if d["code"] == POTHOLE]
        if pots:
            found.append({
                "path": path, "dets": dets,
                "d40_conf": max(d["conf"] for d in pots),  # en güvenli çukur tespiti
                "d40_area": max(box_area_frac(d, rgb.shape) for d in pots),  # en büyük çukur kutusu (alan oranı)
            })
        if i % 100 == 0:
            print(f"  {i}/{len(candidates)} tarandı, D40 bulunan: {len(found)}")

    # Sıralama: önce en yüksek D40 güveni (2 basamağa yuvarlanmış: 0,841 ile 0,839 "eşit" sayılsın),
    # güven eşitse daha büyük kutu önde (küçük resimde de görünen, sunumda anlaşılır çukur).
    found.sort(key=lambda f: (round(f["d40_conf"], 2), f["d40_area"]), reverse=True)
    best = found[:args.top]
    print(f"D40 bulunan {len(found)} görüntü; en iyi {len(best)} gösteriliyor")

    rows, cells = [], []
    for no, f in enumerate(best, start=start_no):
        path, dets = f["path"], f["dets"]
        rgb = load_image(path.read_bytes())  # çizim için yeniden oku (bellekte 500 görüntü tutmamak için)
        row = make_row(no, path, dets)
        row["d40_guven"] = format_conf(f["d40_conf"], "tr")
        row["d40_kutu_alani_yuzde"] = round(f["d40_area"] * 100, 1)  # en büyük çukur kutusu, görüntünün %'si
        rows.append(row)
        # Satır 1: ülke + en güvenli çukur; satır 2: en büyük çukur kutusunun alanı + tüm tespitler
        # (tek satıra sığmıyor, hücre genişliği sınırlı). Yüzde Türkçe biçimde: %2,9
        line1 = f'{country_of(path)} · D40 {format_conf(f["d40_conf"], "tr")}'
        area = str(row["d40_kutu_alani_yuzde"]).replace(".", ",")
        line2 = f"kutu %{area} · {summary_text(dets)}"
        cells.append(make_cell(draw_detections(rgb, dets, "tr"), no, line1, line2))
        print(f"#{no:>2} {path.name:<28} {line1} · {line2}")
    pd.DataFrame(rows).to_csv(out / "adaylar_cukur.csv", index=False, encoding="utf-8-sig")
    save_sheet(cells, ["hepsi"] * len(cells), out / "temas_sayfasi_cukur.png")  # hepsi tek satırda
    print(f"Çıktılar: {out / 'adaylar_cukur.csv'}, {out / 'temas_sayfasi_cukur.png'}")


def main():
    parser = argparse.ArgumentParser(description="Demo görüntüsü adaylarını seçer ve temas sayfası üretir")
    parser.add_argument("--test-dir", default=str(ROOT / "data/rdd2022/test/img"), help="resmî (etiketsiz) test")
    parser.add_argument("--per-country", type=int, default=8, help="genel adaylar: ülke başına")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default=str(ROOT / "runs/demo_secim"), help="çıktı klasörü (git dışı)")
    parser.add_argument("--cukur", action="store_true", help="çukur (D40) adaylarını üret")
    parser.add_argument("--wide-per-country", type=int, default=100, help="çukur modu: ülke başına taranan")
    parser.add_argument("--top", type=int, default=8, help="çukur modu: gösterilecek aday sayısı")
    parser.add_argument("--exclude", nargs="*", default=["United_States"], help="çukur modu: hariç ülkeler")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    model = YOLO(str(WEIGHTS))
    pothole(model, args, out) if args.cukur else general(model, args, out)


if __name__ == "__main__":
    main()
