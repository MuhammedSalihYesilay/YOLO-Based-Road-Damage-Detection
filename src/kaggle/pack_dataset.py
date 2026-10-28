"""
Adım 4 — Kaggle'a yüklenecek zip'i hazırlar.

Sadece train.txt / val.txt / test.txt'deki görüntüler ve etiketleri girer. Kenara konan boşlar
(train_dropped_empty.txt), smoke dosyaları, split.csv ve .cache dosyaları girmez.
data/yolo/ içindeki hiçbir dosya değiştirilmez; listeler ve data.yaml zip'e yeniden yazılır.

JPEG zaten sıkıştırılmış olduğu için zip sıkıştırmasız (ZIP_STORED): hızlı, boyut aynı.

Çalıştırma:
  python src/kaggle/pack_dataset.py --yolo data/yolo --out data/kaggle_upload
"""

import argparse
import sys
import zipfile
from pathlib import Path, PurePosixPath

CLASS_NAMES = ["D00", "D10", "D20", "D40"]
PARTS = ["train", "val", "test"]
ZIP_NAME = "rdd2022_yolo.zip"


def to_relative(line):
    """Liste satırını ./images/<parça>/<dosya> biçimine çevirir (ters bölü ve mutlak yol düzeltilir)."""
    parts = line.strip().replace("\\", "/").split("/")
    if "images" not in parts:
        sys.exit(f"Satırda 'images' klasörü yok: {line!r}")
    i = len(parts) - 1 - parts[::-1].index("images")  # son 'images'
    return "./" + "/".join(parts[i:])


def read_list(path):
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return [to_relative(ln) for ln in lines]


def label_for(image_rel):
    """./images/train/X.jpg → ./labels/train/X.txt"""
    p = PurePosixPath(image_rel)  # parts: ("images", "train", "X.jpg"); "./" parçalara girmez
    return "./" + str(PurePosixPath("labels", *p.parts[1:-1], p.stem + ".txt"))


def data_yaml_text():
    names = "\n".join(f"  {i}: {n}" for i, n in enumerate(CLASS_NAMES))
    return "train: train.txt\nval: val.txt\ntest: test.txt\n\nnames:\n" + names + "\n"


def check_sources(yolo, lists):
    """Listelerdeki her görüntü ve etiket diskte var mı; yoksa zip yazmadan durur."""
    missing = [rel for images in lists.values() for img in images
               for rel in (img, label_for(img)) if not (yolo / rel).exists()]
    if missing:
        sys.exit(f"{len(missing)} kaynak dosya eksik, ilk 5: {missing[:5]}")


def write_zip(yolo, out_zip, lists):
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_STORED) as zf:
        zf.writestr("data.yaml", data_yaml_text())
        for part, images in lists.items():
            zf.writestr(f"{part}.txt", "\n".join(images) + "\n")
            for img in images:
                for rel in (img, label_for(img)):
                    zf.write(yolo / rel, arcname=rel[2:])  # "./" atılır


def verify_zip(out_zip):
    """Zip'teki listelerin her satırının görüntüsü ve etiketi zip içinde var mı."""
    with zipfile.ZipFile(out_zip) as zf:
        names = set(zf.namelist())
        counts = {}
        for part in PARTS:
            images = zf.read(f"{part}.txt").decode("utf-8").splitlines()
            missing = [rel for img in images for rel in (img, label_for(img)) if rel[2:] not in names]
            if missing:
                sys.exit(f"Zip'te {part} için {len(missing)} dosya eksik, ilk 5: {missing[:5]}")
            counts[part] = len(images)
        return counts, len(names)


def main():
    parser = argparse.ArgumentParser(description="Kaggle'a yüklenecek YOLO veri seti zip'i")
    parser.add_argument("--yolo", default="data/yolo")
    parser.add_argument("--out", default="data/kaggle_upload")
    args = parser.parse_args()

    yolo, out = Path(args.yolo), Path(args.out)
    if out.exists():
        sys.exit(f"{out} zaten var; üzerine yazılmadı. Silmek ya da başka --out vermek için karar senin.")

    lists = {part: read_list(yolo / f"{part}.txt") for part in PARTS}
    check_sources(yolo, lists)

    out.mkdir(parents=True)
    out_zip = out / ZIP_NAME
    write_zip(yolo, out_zip, lists)
    counts, n_files = verify_zip(out_zip)

    for part in PARTS:
        print(f"{part}: {counts[part]} görüntü + {counts[part]} etiket")
    print(f"Zip'te toplam {n_files} dosya (görüntü + etiket + 3 liste + data.yaml)")
    print(f"{out_zip}: {out_zip.stat().st_size / 1024**3:.2f} GB")
    print("Kontrol: listelerdeki her satırın görüntüsü ve etiketi zip içinde var.")


if __name__ == "__main__":
    main()
