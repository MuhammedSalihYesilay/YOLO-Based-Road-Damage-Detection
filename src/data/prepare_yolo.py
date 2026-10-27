"""
Adım 3 — RDD2022 (Supervisely JSON) → YOLO formatı + %80/10/10 bölme.

Kararlar (docs/kararlar.md, 2026-10-27):
  - Sınıflar isimle eşlenir: longitudinal→0, transverse→1, alligator→2, pothole→3; diğerleri yazılmaz.
  - Bölme: ülke + boş/dolu katmanlı %80/10/10, seed 42 (Adım 1 önizlemesiyle aynı algoritma).
  - Boş görüntüler yalnızca train'de ~%10'a indirilir; kenara konanlar silinmez, sadece train.txt'e girmez.
  - Norveç uzun kenar 1280'e küçültülüp yeni dosya olarak yazılır (JPEG 95); diğerleri hardlink.
  - Genişliği/yüksekliği 0 olan kutu atılır (Japan_001265.jpg).

Güvenlik: data-root'a hiçbir şey yazılmaz; çıktı klasörü varsa script durur.

Çalıştırma:
  python src/data/prepare_yolo.py --data-root data/rdd2022 --out data/yolo --seed 42 --workers 4
"""

import argparse
import json
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

# Sıra = YOLO sınıf numarası. Model sınıf numarası döndürdüğü için bu sıra hiç değişmemeli.
CLASS_IDS = {"longitudinal crack": 0, "transverse crack": 1, "alligator crack": 2, "pothole": 3}
CLASS_NAMES = ["D00", "D10", "D20", "D40"]

PARTS = ["train", "val", "test"]
NORWAY_LONG_SIDE = 1280
JPEG_QUALITY = 95


# ---------------------------------------------------------------------------
# Okuma ve dönüştürme
# ---------------------------------------------------------------------------

def read_annotations(data_root):
    """train/ann/*.json dosyalarını okur; görüntü başına bir satırlık tablo döndürür.

    Her satırda: dosya adı, ülke, boyut ve hedef kutular [(sınıf, x1, y1, x2, y2), ...].
    other corruption kutuları ve sıfır boyutlu kutular listeye alınmaz.
    """
    rows, n_zero = [], 0
    for path in sorted((data_root / "train" / "ann").glob("*.json")):
        ann = json.loads(path.read_text(encoding="utf-8"))
        file = path.name[: -len(".json")]  # Japan_000001.jpg.json -> Japan_000001.jpg
        tags = [t["name"].replace(" ", "_") for t in ann["tags"]]  # "United States" -> "United_States"
        country = tags[0] if tags else file.rsplit("_", 1)[0]

        boxes = []
        for obj in ann["objects"]:
            if obj["classTitle"] not in CLASS_IDS:
                continue
            (xa, ya), (xb, yb) = obj["points"]["exterior"]  # dikdörtgenin iki köşesi
            x1, x2, y1, y2 = min(xa, xb), max(xa, xb), min(ya, yb), max(ya, yb)
            if x2 <= x1 or y2 <= y1:
                n_zero += 1
                continue
            boxes.append((CLASS_IDS[obj["classTitle"]], x1, y1, x2, y2))

        rows.append({
            "file": file, "country": country,
            "width": ann["size"]["width"], "height": ann["size"]["height"],
            "boxes": boxes, "is_empty": len(boxes) == 0,  # "empty" olmaz: df.empty pandas'ın kendi özelliği
        })
    print(f"Okunan görüntü: {len(rows)}, atılan sıfır boyutlu kutu: {n_zero}")
    return pd.DataFrame(rows)


def to_yolo_lines(boxes, width, height):
    """Köşe koordinatlarını YOLO satırına çevirir: 'sınıf cx cy w h' (0-1 arası, görüntüye göre oran).

    Oran olduğu için görüntü küçültülse de (Norveç) etiket değişmez.
    """
    lines = []
    for cls, x1, y1, x2, y2 in boxes:
        cx, cy = (x1 + x2) / 2 / width, (y1 + y2) / 2 / height
        w, h = (x2 - x1) / width, (y2 - y1) / height
        lines.append(f"{cls} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")
    return lines


# ---------------------------------------------------------------------------
# Bölme ve boş görüntü azaltma
# ---------------------------------------------------------------------------

def split_images(images, seed):
    """Katmanlı %80/10/10 bölme. Katman = ülke + boş/dolu.

    Her katman ayrı karıştırılıp bölünür; böylece her parçada ülke ve boş oranı aynı kalır.
    Algoritma Adım 1'deki split_preview ile aynı, sonuç önizlemeyle birebir aynı çıkar.
    """
    images = images.copy()
    images["stratum"] = images.country + "_" + np.where(images.is_empty, "bos", "dolu")
    rng = np.random.default_rng(seed)
    images["part"] = ""
    for _, idx in sorted(images.groupby("stratum").groups.items()):
        idx = rng.permutation(np.asarray(idx))
        n_train, n_val = round(len(idx) * 0.8), round(len(idx) * 0.1)
        images.loc[idx[:n_train], "part"] = "train"
        images.loc[idx[n_train:n_train + n_val], "part"] = "val"
        images.loc[idx[n_train + n_val:], "part"] = "test"
    return images.drop(columns="stratum")


def reduce_empty(images, seed, ratio=0.10):
    """Train'deki boş görüntülerden yalnızca bir kısmını kullanır; val/test'e dokunmaz.

    Hedef: train'in ~%10'u boş. Tutulacak boş sayısı ülkelere, ülkenin boş görüntü
    sayısıyla orantılı dağıtılır. Kenara konanlar silinmez; 'used' sütunu False olur.
    """
    images = images.copy()
    images["used"] = True
    train_empty = images[(images.part == "train") & images.is_empty]
    n_full = ((images.part == "train") & ~images.is_empty).sum()
    n_keep_total = round(n_full * ratio / (1 - ratio))  # boş / (dolu + boş) = ratio

    rng = np.random.default_rng(seed)
    for country, group in sorted(train_empty.groupby("country")):
        n_keep = round(n_keep_total * len(group) / len(train_empty))
        keep = rng.choice(np.asarray(group.index), size=n_keep, replace=False)
        images.loc[group.index.difference(keep), "used"] = False
    return images


# ---------------------------------------------------------------------------
# Yazma
# ---------------------------------------------------------------------------

def link_or_copy(src, dst):
    """Hardlink (yer kaplamaz); olmazsa kopya. Hardlink'e sonradan hiçbir şey yazılmaz."""
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def resize_norway(src, dst, width, height):
    """Norveç görüntüsünü uzun kenar 1280 olacak şekilde küçültüp yeni dosya olarak yazar.

    EXIF döndürmesi uygulanmaz (IGNORE_ORIENTATION): pikseller JSON koordinatlarıyla aynı yönde kalır.
    Okunan boyut JSON'dakiyle aynı değilse dosya yazılmaz, adı döndürülür (hata listesi için).
    """
    img = cv2.imread(str(src), cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION)
    if img is None or img.shape[:2] != (height, width):
        found = "okunamadı" if img is None else f"{img.shape[1]}x{img.shape[0]}"
        return f"{src.name}: JSON {width}x{height}, dosya {found}"
    scale = NORWAY_LONG_SIDE / max(width, height)
    small = cv2.resize(img, (round(width * scale), round(height * scale)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(dst), small, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
    return None


def write_dataset(images, data_root, out, workers):
    """Etiket txt'lerini yazar, görüntüleri hardlink'ler, Norveç'i küçültür.

    Boyutu JSON ile uyuşmayan Norveç görüntülerinin listesini döndürür (boşsa sorun yok).
    """
    for part in PARTS:
        (out / "images" / part).mkdir(parents=True)
        (out / "labels" / part).mkdir(parents=True)

    src_dir = data_root / "train" / "img"
    norway = []
    for row in images.itertuples():
        label = out / "labels" / row.part / (Path(row.file).stem + ".txt")
        label.write_text("\n".join(to_yolo_lines(row.boxes, row.width, row.height)), encoding="utf-8")
        dst = out / "images" / row.part / row.file
        if row.country == "Norway":
            norway.append((src_dir / row.file, dst, row.width, row.height))
        else:
            link_or_copy(src_dir / row.file, dst)

    print(f"Norveç küçültülüyor: {len(norway)} görüntü ({workers} iş parçacığı)...")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = pool.map(lambda args: resize_norway(*args), norway)
        return [r for r in results if r is not None]


def write_lists_and_yaml(images, out):
    """train/val/test.txt (data.yaml bunları gösterir), kenara konan boşlar, split.csv ve data.yaml."""
    def line(row):
        return f"./images/{row.part}/{row.file}"  # './' ile başlayan yol txt'nin klasörüne göre çözülür

    for part in PARTS:
        rows = images[(images.part == part) & images.used]
        (out / f"{part}.txt").write_text("\n".join(line(r) for r in rows.itertuples()) + "\n", encoding="utf-8")
    dropped = images[~images.used]
    (out / "train_dropped_empty.txt").write_text("\n".join(line(r) for r in dropped.itertuples()) + "\n",
                                                 encoding="utf-8")

    images[["file", "country", "part", "is_empty", "used"]].to_csv(out / "split.csv", index=False, encoding="utf-8")

    # path yazılmaz: Ultralytics yaml'ın bulunduğu klasörü kullanır (Kaggle'a taşınınca da çalışır)
    names = "\n".join(f"  {i}: {n}" for i, n in enumerate(CLASS_NAMES))
    (out / "data.yaml").write_text(f"train: train.txt\nval: val.txt\ntest: test.txt\n\nnames:\n{names}\n",
                                   encoding="utf-8")


# ---------------------------------------------------------------------------
# Özet
# ---------------------------------------------------------------------------

def print_summary(images):
    """Parça başına (yalnızca kullanılan görüntüler): görüntü, etiket, sınıf dağılımı, boş oranı."""
    used = images[images.used]
    rows = []
    for part in PARTS:
        p = used[used.part == part]
        classes = [cls for boxes in p.boxes for cls, *_ in boxes]
        counts = np.bincount(classes, minlength=len(CLASS_NAMES))
        row = {"part": part, "images": len(p), "labels": len(classes)}
        for name, n in zip(CLASS_NAMES, counts):
            row[name] = n
            row[f"{name}_%"] = round(100 * n / max(len(classes), 1), 1)
        row["empty_%"] = round(100 * p.is_empty.mean(), 1)
        rows.append(row)
    table = pd.DataFrame(rows).set_index("part")
    table.loc["toplam"] = table.sum(numeric_only=True)
    table.loc["toplam", [c for c in table.columns if c.endswith("%")]] = np.nan
    print("\n" + table.to_string())
    print(f"\nKenara konan boş train görüntüsü: {(~images.used).sum()} (dosyaları duruyor, train.txt'te yok)")


def main():
    parser = argparse.ArgumentParser(description="RDD2022 → YOLO formatı + katmanlı bölme")
    parser.add_argument("--data-root", default="data/rdd2022", help="train/ klasörünü içeren orijinal veri (salt okunur)")
    parser.add_argument("--out", default="data/yolo", help="çıktı klasörü (var olmamalı)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--workers", type=int, default=4, help="Norveç küçültmesi için iş parçacığı sayısı")
    args = parser.parse_args()

    data_root, out = Path(args.data_root).resolve(), Path(args.out).resolve()
    if out.exists():
        sys.exit(f"Çıktı klasörü zaten var: {out}\nÜzerine yazılmadı. Silmek ya da başka --out vermek size kalmış.")
    if out.is_relative_to(data_root):
        sys.exit(f"Çıktı orijinal veri klasörünün içinde olamaz: {out}")

    images = read_annotations(data_root)
    images = split_images(images, args.seed)
    images = reduce_empty(images, args.seed)

    mismatched = write_dataset(images, data_root, out, args.workers)
    if mismatched:
        print("\nHATA: boyutu JSON ile uyuşmayan Norveç görüntüleri:")
        print("\n".join(mismatched))
        sys.exit(f"{len(mismatched)} görüntü hatalı; listeler ve data.yaml yazılmadı.")

    write_lists_and_yaml(images, out)
    print_summary(images)
    print(f"\nTamam: {out}")


if __name__ == "__main__":
    main()
