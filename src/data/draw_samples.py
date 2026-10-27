"""
Adım 3 doğrulama — YOLO etiketlerinden rastgele görüntüleri kutularıyla çizer (gözle kontrol için).

Kutular orijinal JSON'dan değil, yazılan YOLO txt'lerinden çizilir: dönüştürme hatası varsa burada görünür.

Çalıştırma:
  python src/data/draw_samples.py --yolo data/yolo --out data/yolo_check --n 20 --n-norway 4 --seed 42
"""

import argparse
import sys
from pathlib import Path

import cv2
import pandas as pd

CLASS_NAMES = ["D00", "D10", "D20", "D40"]
COLORS = [(0, 0, 255), (0, 200, 0), (255, 0, 0), (0, 200, 255)]  # BGR: kırmızı, yeşil, mavi, sarı


def pick_samples(split, n, n_norway, seed):
    """Dolu görüntülerden n tane seçer; en az n_norway tanesi Norveç'ten."""
    full = split[~split.is_empty & split.used]
    norway = full[full.country == "Norway"].sample(n_norway, random_state=seed)
    others = full.drop(norway.index).sample(n - n_norway, random_state=seed)
    return pd.concat([norway, others])


def draw_boxes(img, label_path):
    """YOLO satırlarını (sınıf cx cy w h, 0-1 arası) piksele çevirip çizer."""
    h, w = img.shape[:2]
    thickness = max(2, round(max(h, w) / 400))
    for line in label_path.read_text(encoding="utf-8").splitlines():
        cls, cx, cy, bw, bh = line.split()
        cls, cx, cy, bw, bh = int(cls), float(cx) * w, float(cy) * h, float(bw) * w, float(bh) * h
        p1 = (round(cx - bw / 2), round(cy - bh / 2))
        p2 = (round(cx + bw / 2), round(cy + bh / 2))
        cv2.rectangle(img, p1, p2, COLORS[cls], thickness)
        cv2.putText(img, CLASS_NAMES[cls], (p1[0], max(p1[1] - 5, 15)), cv2.FONT_HERSHEY_SIMPLEX,
                    thickness / 3, COLORS[cls], thickness)
    return img


def main():
    parser = argparse.ArgumentParser(description="YOLO etiketlerini görüntü üzerine çizer")
    parser.add_argument("--yolo", default="data/yolo", help="prepare_yolo.py çıktısı")
    parser.add_argument("--out", default="data/yolo_check", help="çizimlerin kaydedileceği klasör (var olmamalı)")
    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--n-norway", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    yolo, out = Path(args.yolo), Path(args.out)
    if out.exists():
        sys.exit(f"Çıktı klasörü zaten var: {out}")
    out.mkdir(parents=True)

    split = pd.read_csv(yolo / "split.csv")
    for row in pick_samples(split, args.n, args.n_norway, args.seed).itertuples():
        img = cv2.imread(str(yolo / "images" / row.part / row.file))  # okunur, üzerine yazılmaz
        img = draw_boxes(img, yolo / "labels" / row.part / (Path(row.file).stem + ".txt"))
        cv2.imwrite(str(out / f"{row.part}_{row.file}"), img)  # yeni dosya, çıktı klasörüne
        print(f"{row.part}_{row.file}  {img.shape[1]}x{img.shape[0]}")
    print(f"\n{args.n} görüntü kaydedildi: {out.resolve()}")


if __name__ == "__main__":
    main()
