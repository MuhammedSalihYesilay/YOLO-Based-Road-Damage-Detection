"""
Adım 5 — Modelin yerel donanımda (GTX 1650 ve CPU) saniyede kaç görüntü işlediğini ölçer.

Kameradaki gibi görüntüler tek tek (batch 1) işlenir. Görüntüler önceden belleğe okunur; böylece disk okuma
süresi ölçüme karışmaz, yalnızca model.predict süresi (ön işleme + çıkarım + son işleme) ölçülür.
Görüntüler val setinden ülke katmanlı seçilir (Norveç'in 1280x717 görüntüleri de girsin diye).
Ölçüm FP32 ile yapılır: GTX 1650'de FP16 bozuk sonuç veriyor (val mAP50 0,04; kararlar.md 2026-10-30).

Çalıştırma:
  python src/eval/measure_fps.py --weights runs/kaggle/baseline_v8s/weights/best.pt --name baseline_v8s
"""

import argparse
import shutil
import time
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
from ultralytics import YOLO

TARGET_FPS = 15  # proje hedefi: gerçek zamanlı kamerada GTX 1650'de ≥ 15 FPS


def sample_by_country(split_csv, n, seed):
    """Val görüntülerinden her ülkeden orantılı rastgele n görüntü seçer (make_smoke_lists.py ile aynı mantık)."""
    split = pd.read_csv(split_csv)
    val = split[(split.part == "val") & split.used]
    rng = np.random.default_rng(seed)
    frac = n / len(val)
    picked = []
    for _, group in sorted(val.groupby("country")):
        k = max(1, round(len(group) * frac))  # her ülkeden en az 1 görüntü
        picked.extend(rng.choice(np.asarray(group.index), size=k, replace=False))
    return val.loc[sorted(picked)]


def sync(device):
    """GPU işlemleri asenkron çalışır; süre ölçmeden önce GPU'nun işini bitirmesini bekler."""
    if device != "cpu":
        torch.cuda.synchronize()


def measure(model, images, device, imgsz, warmup):
    """Önce ısınma turu atar, sonra her görüntüyü tek tek işleyip süreleri ölçer; özet satırı döndürür."""
    # Isınma: ilk çağrılarda CUDA başlatma ve bellek ayırma olur, bunlar ölçüme girmemeli
    for img in images[:warmup]:
        model.predict(img, imgsz=imgsz, device=device, verbose=False)

    wall, pre, inf, post, n_boxes = [], [], [], [], []
    for img in images:
        sync(device)
        t0 = time.perf_counter()
        r = model.predict(img, imgsz=imgsz, device=device, verbose=False)[0]
        sync(device)
        wall.append((time.perf_counter() - t0) * 1000)  # ms
        pre.append(r.speed["preprocess"])  # Ultralytics'in kendi ölçtüğü aşama süreleri (ms)
        inf.append(r.speed["inference"])
        post.append(r.speed["postprocess"])
        n_boxes.append(len(r.boxes))  # kontrol amaçlı: model gerçekten kutu üretiyor mu

    wall = np.array(wall)
    return {
        "cihaz": "GPU" if device != "cpu" else "CPU",
        "imgsz": imgsz,
        "görüntü": len(images),
        "ms ort": wall.mean(),
        "ms medyan": np.median(wall),
        "ms p95": np.percentile(wall, 95),  # yavaş karelerin ne kadar yavaş olduğunu gösterir
        "FPS": 1000 / wall.mean(),
        "ön işleme ms": np.mean(pre),
        "çıkarım ms": np.mean(inf),
        "son işleme ms": np.mean(post),
        "kutu/görüntü": np.mean(n_boxes),
    }


def main():
    parser = argparse.ArgumentParser(description="GTX 1650 ve CPU'da görüntü başına süre ve FPS ölçümü")
    parser.add_argument("--weights", default="runs/kaggle/baseline_v8s/weights/best.pt")
    parser.add_argument("--split-csv", default="data/yolo/split.csv")
    parser.add_argument("--images", default="data/yolo/images/val")
    parser.add_argument("--name", default="baseline_v8s")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--n", type=int, default=200, help="GPU'da ölçülecek görüntü sayısı")
    parser.add_argument("--n-cpu", type=int, default=50, help="CPU'da ölçülecek görüntü sayısı (0 = CPU atlanır)")
    parser.add_argument("--warmup", type=int, default=20)
    parser.add_argument("--device", default="0")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="runs/eval")
    parser.add_argument("--docs-dir", default="docs/degerlendirme")
    args = parser.parse_args()

    rows = sample_by_country(args.split_csv, args.n, args.seed)
    images = [cv2.imread(str(Path(args.images) / f)) for f in rows.file]  # belleğe önceden okuma
    print(f"{len(images)} görüntü:", rows.country.value_counts().to_dict())
    print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "yok")

    model = YOLO(args.weights)
    results = [measure(model, images, args.device, args.imgsz, args.warmup)]
    if args.n_cpu > 0:
        results.append(measure(model, images[: args.n_cpu], "cpu", args.imgsz, min(args.warmup, 5)))

    df = pd.DataFrame(results)
    out_dir = Path(args.out) / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "fps.csv", index=False, float_format="%.2f")
    docs_dir = Path(args.docs_dir) / f"{args.name}_val"  # görüntüler val'den seçildiği için val klasörüne
    docs_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_dir / "fps.csv", docs_dir / "fps.csv")

    print(df.to_string(index=False, float_format=lambda v: f"{v:.2f}"))
    gpu_fps = results[0]["FPS"]
    print(f"\nGPU (FP32): {gpu_fps:.1f} FPS → hedef ≥ {TARGET_FPS}: {'tuttu' if gpu_fps >= TARGET_FPS else 'TUTMADI'}")


if __name__ == "__main__":
    main()
