"""
Adım 3 smoke test — küçük, temsilî train/val listeleri ve data_smoke.yaml.

fraction kullanılmaz: train listesinin ilk %X'ini alır, sıralı olduğu için neredeyse hepsi China_Drone olur.
Burada her katmandan (ülke + boş/dolu) aynı oranda rastgele seçilir; Norveç mutlaka içinde olur.

Çalıştırma:
  python src/data/make_smoke_lists.py --yolo data/yolo --n-train 2000 --n-val 400 --seed 42
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

CLASS_NAMES = ["D00", "D10", "D20", "D40"]


def sample_stratified(rows, n, seed):
    """Her katmandan (ülke + boş/dolu) satır sayısıyla orantılı rastgele seçim."""
    rng = np.random.default_rng(seed)
    frac = n / len(rows)
    picked = []
    for _, group in sorted(rows.groupby(["country", "is_empty"])):
        k = max(1, round(len(group) * frac))
        picked.extend(rng.choice(np.asarray(group.index), size=k, replace=False))
    return rows.loc[sorted(picked)]


def write_list(rows, path):
    path.write_text("\n".join(f"./images/{r.part}/{r.file}" for r in rows.itertuples()) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Smoke test için küçük katmanlı listeler")
    parser.add_argument("--yolo", default="data/yolo")
    parser.add_argument("--n-train", type=int, default=2000)
    parser.add_argument("--n-val", type=int, default=400)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    yolo = Path(args.yolo)
    outputs = [yolo / "smoke_train.txt", yolo / "smoke_val.txt", yolo / "data_smoke.yaml"]
    if any(p.exists() for p in outputs):
        sys.exit("Smoke dosyaları zaten var; üzerine yazılmadı.")

    split = pd.read_csv(yolo / "split.csv")
    split = split[split.used]  # kenara konan boşlar smoke'a da girmez
    train = sample_stratified(split[split.part == "train"], args.n_train, args.seed)
    val = sample_stratified(split[split.part == "val"], args.n_val, args.seed)
    if not ((train.country == "Norway").any() and (val.country == "Norway").any()):
        sys.exit("Norveç görüntüsü seçilmedi; smoke test temsilî değil.")

    write_list(train, outputs[0])
    write_list(val, outputs[1])
    names = "\n".join(f"  {i}: {n}" for i, n in enumerate(CLASS_NAMES))
    outputs[2].write_text(f"train: smoke_train.txt\nval: smoke_val.txt\n\nnames:\n{names}\n", encoding="utf-8")

    for name, rows in [("train", train), ("val", val)]:
        print(f"{name}: {len(rows)} görüntü, boş %{100 * rows.is_empty.mean():.1f}")
        print(rows.country.value_counts().to_string(), "\n")


if __name__ == "__main__":
    main()
