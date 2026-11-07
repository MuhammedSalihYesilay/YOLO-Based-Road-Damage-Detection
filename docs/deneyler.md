# Deney sonuçları

> **Seçilen model: YOLO26s (e3)**, 2026-11-02. Neden: [model-secimi.md](model-secimi.md)
> **Şu anki en iyi aday: e5 (YOLO26s, imgsz 1024)**, 2026-11-07: val mAP50 0,609 (e3'ten +2,0 puan). Nihai model
> seçimi e6 ve e7 bitince yapılacak (1024 + e6/e7'den kazanan ayar birleştirilebilir). Kayıt: [kararlar.md](kararlar.md) (2026-11-07)

Her eğitim bir satır. Rapordaki karşılaştırma tablosunun kaynağı bu dosya.

**Ölçüm kuralı (kararlar.md, 2026-10-30):** Sonuçlar `src/eval/evaluate.py` ile yerelde, FP32, **val** setinde
ölçülür (imgsz eğitimdekiyle aynı, batch 16, Ultralytics val varsayılanları: conf 0,001, IoU 0,7). Kaggle'ın eğitim
sonunda verdiği değer yalnızca not olarak "Ayarlar" tablosunda durur. FPS `src/eval/measure_fps.py` ile GTX 1650'de,
FP32, batch 1 (kameradaki gibi tek tek), val'den ülke katmanlı 201 görüntüyle ölçülür. Test seti yalnızca Adım 9'da.

## Ayarlar

| # | Tarih | Ad | Model | imgsz | Epoch | Batch | Augmentation | Ortam, süre | Kaggle eğitim sonu mAP50 | Ağırlık |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-29 | baseline_v8s | yolov8s.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, 4 sa 55 dk | 0,589 | `runs/kaggle/baseline_v8s/weights/best.pt` |
| 2 | 2026-11-01 | e2_yolo11s | yolo11s.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, 7 sa 11 dk | 0,597 | `runs/kaggle/e2_yolo11s/weights/best.pt` |
| 3 | 2026-11-01 | e3_yolo26s | yolo26s.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, 8 sa 22 dk | 0,600 | `runs/kaggle/e3_yolo26s/weights/best.pt` |
| 4 | 2026-11-02 | e4_yolo26n | yolo26n.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, 5 sa 21 dk | 0,578 | `runs/kaggle/e4_yolo26n/weights/best.pt` |
| 5 | 2026-11-07 | e5_yolo26s_1024 | yolo26s.pt (COCO) | **1024** | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, **iki oturum** (resume): V4 epoch 1–26 + V5 epoch 27–50, toplam **≈ 13 sa** (aşağıdaki nota bakın) | 0,631 | `runs/kaggle/e5_yolo26s_1024/weights/best.pt` |

## Sonuçlar (val, yerel FP32)

| # | P | R | F1 | mAP50 | mAP50-95 | AP50 D00 | AP50 D10 | AP50 D20 | AP50 D40 | mAP50 Norveç | mAP50 China_Drone | mAP50 Drone hariç | mAP50 Japonya+Hindistan | FPS GTX 1650 | FPS CPU |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,621 | 0,541 | 0,578 | **0,571** | 0,286 | 0,569 | 0,574 | 0,679 | 0,464 | 0,295 | 0,593 | 0,568 | 0,522 | 53,2 | 9,5 |
| 2 | 0,638 | 0,542 | 0,586 | **0,582** | 0,294 | 0,572 | 0,591 | 0,690 | 0,477 | 0,265 | 0,666 | 0,577 | 0,522 | 53,4 | 10,6 |
| 3 | 0,641 | 0,547 | 0,591 | **0,589** | 0,294 | 0,578 | 0,588 | 0,691 | 0,500 | 0,280 | 0,666 | 0,584 | 0,537 | 50,5 | 9,9 |
| 4 | 0,610 | 0,534 | 0,570 | **0,560** | 0,281 | 0,543 | 0,569 | 0,670 | 0,458 | 0,239 | 0,658 | 0,554 | 0,509 | 61,2 | 23,4 |
| 5 | 0,633 | 0,578 | 0,605 | **0,609** | 0,309 | 0,604 | 0,620 | 0,697 | 0,516 | 0,380 | 0,688 | 0,605 | 0,544 | 25,0 | 4,2 |

- **Japonya+Hindistan** sütunu referansın raporladığı 0,547 ile yalnızca **ön karşılaştırma**: val'de ölçüldü ve
  referansın 0,547'si farklı görüntülerde ölçülmüştü. Kesin karşılaştırma Adım 9'da test setinde.
- P ve R, sınıf ortalaması F1'i en yüksek yapan güven eşiğinde; F1 = 2PR/(P+R).
- Ayrıntılı tablolar: `docs/degerlendirme/<ad>_val/` (ör. [baseline_v8s_val](degerlendirme/baseline_v8s_val/summary.md),
  [e2_yolo11s_val](degerlendirme/e2_yolo11s_val/summary.md), [e3_yolo26s_val](degerlendirme/e3_yolo26s_val/summary.md),
  [e4_yolo26n_val](degerlendirme/e4_yolo26n_val/summary.md), [e5_yolo26s_1024_val](degerlendirme/e5_yolo26s_1024_val/summary.md)).
- Tüm koşularda `optimizer=auto` → Ultralytics 8.4.182 uzun eğitimde (>10.000 adım) **MuSGD** seçti (checkpoint'lerden
  doğrulandı: baseline, e2, e3, e4, e5). YOLO26 (e3, e4, e5) Ultralytics varsayılanıyla **NMS'li** ölçüldü (`nms=None`; NMS'siz baş yalnızca `nms=False` ile açılır).
- **"Kaggle eğitim sonu" sütunu:** eğitim bitince `best.pt` ile yapılan son doğrulama (FP16). Önceki koşularda bu değer
  results.csv'deki en iyi epoch'la aynıydı (ör. baseline epoch 46: P 0,629, R 0,555, mAP50 0,589). e5'te ikisi ilk kez
  ayrışıyor: `best.pt` doğrulaması **0,631** (V5 log'u: P 0,645, R 0,597, mAP50-95 0,33); notebook'un özet satırındaki
  "en iyi val mAP50 0,633" results.csv'deki epoch 44 değeri.
- **e5 (iki oturum):** V4 epoch 1–26, Kaggle'ın 12 saat sınırı yüzünden `MAX_HOURS` ile durduruldu; V5 `MODE="devam"` ile
  `last.pt`'den resume, epoch 27–50, 50 epoch normal bitti. Süre: V4 ~6 sa 5 dk (results.csv `time` sütunu; devir notunda
  6,30 sa; süre sınırıyla durduğu için log'da "epochs completed" satırı yok) + V5 6 sa 50 dk (log: "24 epochs completed
  in 6.837 hours") ≈ **13 sa**. args.yaml'daki `optimizer: MuSGD` ve `warmup_bias_lr: 0.0` resume'dan geliyor (e3'ün
  checkpoint'inde de aynı); gerçek fark yalnızca imgsz.
- **e5 ölçümü:** `evaluate.py --imgsz 1024`, batch 16 (GTX 1650'de bellek yetti); modele giren tensörün 1024x1024
  olduğu çıktıda doğrulandı (2026-11-07'de evaluate.py ve measure_fps.py'ye eklenen kontrol).
- Yorumlar: [adim-6-karsilastirma.md](adimlar/adim-6-karsilastirma.md).
