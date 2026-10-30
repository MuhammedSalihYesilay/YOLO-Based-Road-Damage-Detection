# Deney sonuçları

Her eğitim bir satır. Rapordaki karşılaştırma tablosunun kaynağı bu dosya.

**Ölçüm kuralı (kararlar.md, 2026-10-30):** Sonuçlar `src/eval/evaluate.py` ile yerelde, FP32, **val** setinde
ölçülür (imgsz eğitimdekiyle aynı, batch 16, Ultralytics val varsayılanları: conf 0,001, IoU 0,7). Kaggle'ın eğitim
sonunda verdiği değer yalnızca not olarak "Ayarlar" tablosunda durur. FPS `src/eval/measure_fps.py` ile GTX 1650'de,
FP32, batch 1 (kameradaki gibi tek tek), val'den ülke katmanlı 201 görüntüyle ölçülür. Test seti yalnızca Adım 9'da.

## Ayarlar

| # | Tarih | Ad | Model | imgsz | Epoch | Batch | Augmentation | Ortam, süre | Kaggle eğitim sonu mAP50 | Ağırlık |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-29 | baseline_v8s | yolov8s.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, 4 sa 55 dk | 0,589 | `runs/kaggle/baseline_v8s/weights/best.pt` |

## Sonuçlar (val, yerel FP32)

| # | P | R | F1 | mAP50 | mAP50-95 | AP50 D00 | AP50 D10 | AP50 D20 | AP50 D40 | mAP50 Norveç | mAP50 China_Drone | mAP50 Drone hariç | mAP50 Japonya+Hindistan | FPS GTX 1650 | FPS CPU |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,621 | 0,541 | 0,578 | **0,571** | 0,286 | 0,569 | 0,574 | 0,679 | 0,464 | 0,295 | 0,593 | 0,568 | 0,522 | 53,2 | 9,5 |

- **Japonya+Hindistan** sütunu referansın raporladığı 0,547 ile yalnızca **ön karşılaştırma**: val'de ölçüldü ve
  referansın 0,547'si farklı görüntülerde ölçülmüştü. Kesin karşılaştırma Adım 9'da test setinde.
- P ve R, sınıf ortalaması F1'i en yüksek yapan güven eşiğinde; F1 = 2PR/(P+R).
- Ayrıntılı tablolar: `docs/degerlendirme/<ad>_val/` (ör. [baseline_v8s_val](degerlendirme/baseline_v8s_val/summary.md)).
