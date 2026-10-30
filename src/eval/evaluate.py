"""
Adım 5 — Modeli val setinde ölçer: genel, sınıf bazında, ülke bazında ve özel alt kümeler.

Neden tek koşu: alt kümeler için ayrı liste/yaml yazıp her biri için model.val çalıştırılsaydı, Ultralytics
data/yolo/labels/ altına yeni .cache dosyaları yazardı (data/yolo/ değişirdi) ve val 10 kez koşardı.
Bunun yerine val bir kez koşar; Ultralytics'in her görüntü için hesapladığı eşleştirme sonuçları (tp, conf,
pred_cls, target_cls) saklanır ve alt kümeler bu sonuçlardan, yine Ultralytics'in ap_per_class fonksiyonuyla
hesaplanır. Böylece her alt küme resmî val ile birebir aynı yöntemle ölçülmüş olur.

Test seti yalnızca Adım 9'da, --final bayrağıyla kullanılabilir.

Çalıştırma:
  python src/eval/evaluate.py --weights runs/kaggle/baseline_v8s/weights/best.pt --name baseline_v8s
"""

import argparse
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from ultralytics.models.yolo.detect import DetectionValidator
from ultralytics.utils.metrics import ap_per_class

CLASS_NAMES = ["D00", "D10", "D20", "D40"]

# Raporlanan alt kümeler: ad → içerdiği ülkeler. None = tüm görüntüler.
SPECIAL_SUBSETS = {
    "Tümü": None,
    "Drone hariç": ["Japan", "India", "Czech", "United_States", "Norway", "China_MotorBike"],
    "Japonya+Hindistan": ["Japan", "India"],  # referans projenin eğitildiği ülkeler (0,547 ile ön karşılaştırma)
}

# docs/ altına (git'e) kopyalanacak Ultralytics grafikleri
PLOTS_TO_COPY = ["confusion_matrix.png", "confusion_matrix_normalized.png", "BoxPR_curve.png"]


class BreakdownValidator(DetectionValidator):
    """Ultralytics'in val sınıfı; ek olarak görüntü başına sonuçları ve dosya adlarını saklar."""

    def init_metrics(self, model):
        """Val başında çağrılır; dosya adı listesini sıfırlar."""
        super().init_metrics(model)
        self.im_names = []  # görüntü sırası; metrics.stats listeleriyle aynı sırada dolar
        self.per_image = None

    def update_metrics(self, preds, batch):
        """Her batch'te çağrılır. Asıl metot her görüntü için stats'a bir satır ekler; adları da aynı sırayla tutarız."""
        self.im_names.extend(Path(f).name for f in batch["im_file"][: len(preds)])
        super().update_metrics(preds, batch)

    def get_stats(self):
        """Val sonunda çağrılır. Asıl metot görüntü başına stats'ı siler (clear_stats); silinmeden önce kopyalarız."""
        self.per_image = {k: list(v) for k, v in self.metrics.stats.items()}
        return super().get_stats()


def compute_metrics(stats, idx):
    """Seçilen görüntülerin (idx) sonuçlarını birleştirip P, R, F1, mAP50, mAP50-95 ve sınıf başına AP50 hesaplar.

    Döndürür: (özet satırı, sınıf başına ayrıntılar). Etiket yoksa ayrıntılar None.
    """
    tp = np.concatenate([stats["tp"][i] for i in idx], 0)
    conf = np.concatenate([stats["conf"][i] for i in idx], 0)
    pred_cls = np.concatenate([stats["pred_cls"][i] for i in idx], 0)
    target_cls = np.concatenate([stats["target_cls"][i] for i in idx], 0)

    row = {"görüntü": len(idx), "kutu": len(target_cls)}
    if len(target_cls) == 0:  # alt kümede hiç etiket yoksa metrik tanımsız
        return row, None
    # ap_per_class: P ve R, sınıf ortalaması F1'i en yüksek yapan güven eşiğinde verilir (Ultralytics ile aynı)
    _, _, p, r, f1, ap, classes = ap_per_class(tp, conf, pred_cls, target_cls)[:7]
    mp, mr = p.mean(), r.mean()
    row.update(
        P=mp,
        R=mr,
        F1=2 * mp * mr / (mp + mr + 1e-16),  # ortalama P ve R'den F1 (tek sayı olarak raporlamak için)
        mAP50=ap[:, 0].mean(),  # ap sütunları IoU 0.50, 0.55, ..., 0.95
        **{"mAP50-95": ap.mean()},
    )
    # Alt kümede bulunmayan sınıf için AP boş kalır (ör. bir ülkede hiç D40 yoksa)
    for k, c in enumerate(classes):
        row[f"AP50 {CLASS_NAMES[int(c)]}"] = ap[k, 0]
    return row, (p, r, f1, ap, classes)


def per_class_table(stats, idx):
    """Tüm görüntülerde sınıf başına P, R, F1, AP50, AP50-95 ve etiket sayısı tablosu."""
    _, details = compute_metrics(stats, idx)
    p, r, f1, ap, classes = details
    target_cls = np.concatenate([stats["target_cls"][i] for i in idx], 0).astype(int)
    rows = []
    for k, c in enumerate(classes):
        c = int(c)
        rows.append({"sınıf": CLASS_NAMES[c], "etiket": int((target_cls == c).sum()), "P": p[k], "R": r[k],
                     "F1": f1[k], "AP50": ap[k, 0], "AP50-95": ap[k].mean()})
    return pd.DataFrame(rows)


def subset_table(stats, im_names, split_csv):
    """Tümü, her ülke, Drone hariç ve Japonya+Hindistan için metrik tablosu."""
    country_of = pd.read_csv(split_csv).set_index("file")["country"]
    countries = country_of.reindex(im_names)
    if countries.isna().any():  # her val görüntüsünün ülkesi split.csv'de olmalı
        sys.exit(f"split.csv'de bulunamayan görüntü: {countries[countries.isna()].index[:5].tolist()}")
    countries = countries.to_numpy()

    subsets = dict(SPECIAL_SUBSETS)
    for c in sorted(set(countries)):
        subsets[c] = [c]

    rows = []
    for name, members in subsets.items():
        idx = np.arange(len(im_names)) if members is None else np.flatnonzero(np.isin(countries, members))
        row, _ = compute_metrics(stats, idx)
        rows.append({"alt küme": name, **row})
    return pd.DataFrame(rows)


def to_markdown(df):
    """DataFrame'i ondalıkları 3 basamaklı Markdown tabloya çevirir (tabulate paketi gerektirmez)."""
    def fmt(v):
        if isinstance(v, float):
            return "" if np.isnan(v) else f"{v:.3f}"
        return str(v)
    lines = ["| " + " | ".join(df.columns) + " |", "|" + "---|" * len(df.columns)]
    lines += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Val setinde genel, sınıf ve ülke bazında değerlendirme")
    parser.add_argument("--weights", default="runs/kaggle/baseline_v8s/weights/best.pt")
    parser.add_argument("--data", default="data/yolo/data.yaml")
    parser.add_argument("--split-csv", default="data/yolo/split.csv")
    parser.add_argument("--name", default="baseline_v8s", help="deney adı; çıktı klasörlerinin adı")
    parser.add_argument("--split", default="val", choices=["val", "test"])
    parser.add_argument("--final", action="store_true", help="test seti için zorunlu (yalnızca Adım 9)")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default="0")
    parser.add_argument("--out", default="runs/eval", help="ham çıktılar (git dışı)")
    parser.add_argument("--docs-dir", default="docs/degerlendirme", help="özet kopya (git'e girer)")
    args = parser.parse_args()

    # Test seti koruması: model seçimi val ile yapılır, test yalnızca en sonda bir kez kullanılır
    if args.split == "test" and not args.final:
        sys.exit("Test seti yalnızca Adım 9'da, --final bayrağıyla kullanılır.")

    out_dir = (Path(args.out) / args.name).resolve()  # mutlak yol: göreli olursa Ultralytics başına runs/detect ekler
    validator = BreakdownValidator(args=dict(
        model=args.weights, data=args.data, split=args.split, imgsz=args.imgsz, batch=args.batch,
        device=args.device, project=str(out_dir), name=args.split, exist_ok=True, plots=True,
    ))
    validator()  # val'i bir kez koşturur; grafikler out_dir/<split>/ altına yazılır
    save_dir = Path(validator.save_dir)
    stats, im_names = validator.per_image, validator.im_names
    if len(im_names) != len(stats["tp"]):  # dosya adları ile sonuç satırları aynı sırada ve aynı sayıda olmalı
        sys.exit(f"Görüntü adı ({len(im_names)}) ve sonuç ({len(stats['tp'])}) sayıları tutmuyor.")

    per_class = per_class_table(stats, np.arange(len(im_names)))
    subsets = subset_table(stats, im_names, args.split_csv)

    # Tutarlılık kontrolü: bizim hesapladığımız "Tümü" satırı Ultralytics'in kendi sonucuyla aynı olmalı
    box = validator.metrics.box
    total = subsets.iloc[0]
    if not (np.isclose(total["mAP50"], box.map50) and np.isclose(total["mAP50-95"], box.map)):
        sys.exit(f"Tutarsızlık: bizim mAP50 {total['mAP50']:.4f}, Ultralytics {box.map50:.4f}")

    per_class.to_csv(save_dir / "per_class.csv", index=False, float_format="%.4f")
    subsets.to_csv(save_dir / "per_subset.csv", index=False, float_format="%.4f")
    summary = (
        f"# Değerlendirme: {args.name} — {args.split}\n\n"
        f"- Ağırlık: `{args.weights}`\n- imgsz {args.imgsz}, batch {args.batch}, conf/iou Ultralytics val varsayılanı\n"
        f"- Görüntü: {len(im_names)}, kutu: {int(total['kutu'])}\n\n"
        f"## Sınıf bazında\n\n{to_markdown(per_class)}\n\n"
        f"## Alt kümeler (ülke ve özel)\n\n{to_markdown(subsets)}\n\n"
        "P ve R, sınıf ortalaması F1'i en yüksek yapan güven eşiğinde; F1 = 2PR/(P+R). "
        "Boş AP hücresi: o alt kümede o sınıftan etiket yok.\n"
    )
    (save_dir / "summary.md").write_text(summary, encoding="utf-8")

    # Özet sonuçların git'e giren kopyası
    docs_dir = Path(args.docs_dir) / f"{args.name}_{args.split}"
    docs_dir.mkdir(parents=True, exist_ok=True)
    for f in ["per_class.csv", "per_subset.csv", "summary.md", *PLOTS_TO_COPY]:
        if (save_dir / f).exists():
            shutil.copy2(save_dir / f, docs_dir / f)

    print(summary)
    print(f"Ham çıktılar: {save_dir}\nÖzet kopya: {docs_dir}")


if __name__ == "__main__":
    main()
