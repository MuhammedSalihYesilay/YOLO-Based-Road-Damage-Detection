# Deney sonuçları

> **Final model: e5 (YOLO26s, imgsz 1024)**, 2026-11-08: val mAP50 0,609 (e3'ten +2,0 puan). Neden:
> [model-secimi.md](model-secimi.md). Kayıt: [kararlar.md](kararlar.md) (2026-11-08, e7 ve final seçim)
> Mimari seçimi (2026-11-02): YOLO26s (e3); e5–e7 e3'e karşı karşılaştırıldı.
> **e6 (cls_pw 0.5) ve e7 (D40 ×2), 2026-11-08:** genel mAP50'de kazandırmıyor (e3'e göre +0,1 / +0,4 puan, 1 puan
> kuralının altında). e7 çukurda kazandırıyor (D40 AP50 +2,0, recall +8,2, precision −4,1). Birleşik model
> (1024 + D40 ×2) yapılmadı; zaman ve kota kalırsa final teslimden önce isteğe bağlı deney / gelecek çalışma.

Her eğitim bir satır. Rapordaki karşılaştırma tablosunun kaynağı bu dosya.

**Ölçüm kuralı (kararlar.md, 2026-10-30):** Sonuçlar `src/eval/evaluate.py` ile yerelde, FP32, **val** setinde
ölçülür (imgsz eğitimdekiyle aynı, batch 16, Ultralytics val varsayılanları: conf 0,001, IoU 0,7). Kaggle'ın eğitim
sonunda verdiği değer yalnızca not olarak "Ayarlar" tablosunda durur. FPS `src/eval/measure_fps.py` ile GTX 1650'de,
FP32, batch 1 (kameradaki gibi tek tek), val'den ülke katmanlı 201 görüntüyle ölçülür. Test seti yalnızca Adım 9'da.

## Ayarlar

| # | Tarih | Ad | Model | imgsz | Epoch | Batch | Augmentation | Ortam, süre | Kaggle eğitim sonu mAP50 | Ağırlık |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-29 | baseline_v8s | yolov8s.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, 4 sa 55 dk (eğitim döngüsü: 4 sa 34 dk, results.csv) | 0,589 | `runs/kaggle/baseline_v8s/weights/best.pt` |
| 2 | 2026-11-01 | e2_yolo11s | yolo11s.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, 7 sa 11 dk (eğitim döngüsü: 5 sa 55 dk, results.csv) | 0,597 | `runs/kaggle/e2_yolo11s/weights/best.pt` |
| 3 | 2026-11-01 | e3_yolo26s | yolo26s.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, 8 sa 22 dk (eğitim döngüsü: 7 sa 5 dk, results.csv) | 0,600 | `runs/kaggle/e3_yolo26s/weights/best.pt` |
| 4 | 2026-11-02 | e4_yolo26n | yolo26n.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, 5 sa 21 dk (eğitim döngüsü: 4 sa 33 dk, results.csv) | 0,578 | `runs/kaggle/e4_yolo26n/weights/best.pt` |
| 5 | 2026-11-07 | e5_yolo26s_1024 | yolo26s.pt (COCO) | **1024** | 50 / 50 | 16 | Ultralytics varsayılan | Kaggle T4, **iki oturum** (resume): V4 epoch 1–26 + V5 epoch 27–50 (eğitim döngüsü: 6 sa 5 dk + 6 sa 50 dk = **12 sa 55 dk**, results.csv; aşağıdaki nota bakın) | 0,631 | `runs/kaggle/e5_yolo26s_1024/weights/best.pt` |
| 6 | 2026-11-08 | e6_yolo26s_clspw | yolo26s.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan + **`cls_pw 0.5`** | Kaggle T4, tek oturum (V6) (eğitim döngüsü: 5 sa 5 dk, results.csv = log "5.085 hours") | 0,603 | `runs/kaggle/e6_yolo26s_clspw/weights/best.pt` |
| 7 | 2026-11-08 | e7_yolo26s_d40x2 | yolo26s.pt (COCO) | 640 | 50 / 50 | 16 | Ultralytics varsayılan + **D40 ×2 oversampling** (train listesi 24.202 satır) | Kaggle T4, tek oturum (V7) (eğitim döngüsü: 6 sa 7 dk, results.csv = log "6.120 hours") | 0,609 | `runs/kaggle/e7_yolo26s_d40x2/weights/best.pt` |

## Sonuçlar (val, yerel FP32)

| # | P | R | F1 | mAP50 | mAP50-95 | AP50 D00 | AP50 D10 | AP50 D20 | AP50 D40 | mAP50 Norveç | mAP50 China_Drone | mAP50 Drone hariç | mAP50 Japonya+Hindistan | FPS GTX 1650 | FPS CPU |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,621 | 0,541 | 0,578 | **0,571** | 0,286 | 0,569 | 0,574 | 0,679 | 0,464 | 0,295 | 0,593 | 0,568 | 0,522 | 53,2 | 9,5 |
| 2 | 0,638 | 0,542 | 0,586 | **0,582** | 0,294 | 0,572 | 0,591 | 0,690 | 0,477 | 0,265 | 0,666 | 0,577 | 0,522 | 53,4 | 10,6 |
| 3 | 0,641 | 0,547 | 0,591 | **0,589** | 0,294 | 0,578 | 0,588 | 0,691 | 0,500 | 0,280 | 0,666 | 0,584 | 0,537 | 50,5 | 9,9 |
| 4 | 0,610 | 0,534 | 0,570 | **0,560** | 0,281 | 0,543 | 0,569 | 0,670 | 0,458 | 0,239 | 0,658 | 0,554 | 0,509 | 61,2 | 23,4 |
| 5 | 0,633 | 0,578 | 0,605 | **0,609** | 0,309 | 0,604 | 0,620 | 0,697 | 0,516 | 0,380 | 0,688 | 0,605 | 0,544 | 25,0 | 4,2 |
| 6 | 0,635 | 0,554 | 0,592 | **0,590** | 0,296 | 0,580 | 0,585 | 0,693 | 0,503 | 0,308 | 0,670 | 0,584 | 0,534 | 51,9 | 11,0 |
| 7 | 0,646 | 0,554 | 0,596 | **0,593** | 0,294 | 0,573 | 0,583 | 0,696 | 0,520 | 0,316 | 0,680 | 0,587 | 0,531 | 51,8 | 10,9 |

- **Japonya+Hindistan** sütunu referansın raporladığı 0,547 ile yalnızca **ön karşılaştırma**: val'de ölçüldü ve
  referansın 0,547'si farklı görüntülerde ölçülmüştü. Kesin karşılaştırma Adım 9'da test setinde.
- P ve R, sınıf ortalaması F1'i en yüksek yapan güven eşiğinde; F1 = 2PR/(P+R).
- Ayrıntılı tablolar: `docs/degerlendirme/<ad>_val/` (ör. [baseline_v8s_val](degerlendirme/baseline_v8s_val/summary.md),
  [e2_yolo11s_val](degerlendirme/e2_yolo11s_val/summary.md), [e3_yolo26s_val](degerlendirme/e3_yolo26s_val/summary.md),
  [e4_yolo26n_val](degerlendirme/e4_yolo26n_val/summary.md), [e5_yolo26s_1024_val](degerlendirme/e5_yolo26s_1024_val/summary.md),
  [e6_yolo26s_clspw_val](degerlendirme/e6_yolo26s_clspw_val/summary.md),
  [e7_yolo26s_d40x2_val](degerlendirme/e7_yolo26s_d40x2_val/summary.md)).
- Tüm koşularda `optimizer=auto` → Ultralytics 8.4.182 uzun eğitimde (>10.000 adım) **MuSGD** seçti (checkpoint'lerden
  doğrulandı: baseline, e2, e3, e4, e5, e6, e7). YOLO26 (e3, e4, e5, e6, e7) Ultralytics varsayılanıyla **NMS'li** ölçüldü (`nms=None`; NMS'siz baş yalnızca `nms=False` ile açılır).
- **"Kaggle eğitim sonu" sütunu:** eğitim bitince `best.pt` ile yapılan son doğrulama (FP16). Önceki koşularda bu değer
  results.csv'deki en iyi epoch'la aynıydı (ör. baseline epoch 46: P 0,629, R 0,555, mAP50 0,589). e5'te ikisi ilk kez
  ayrışıyor: `best.pt` doğrulaması **0,631** (V5 log'u: P 0,645, R 0,597, mAP50-95 0,33); notebook'un özet satırındaki
  "en iyi val mAP50 0,633" results.csv'deki epoch 44 değeri. e6'da da ayrışıyor: `best.pt` doğrulaması **0,603** (P 0,632,
  R 0,575, mAP50-95 0,316, D40 0,501); özet satırındaki "en iyi val mAP50 0,605" results.csv'deki epoch 37 değeri.
  e7'de ayrışma yok: `best.pt` doğrulaması **0,609** (P 0,653, R 0,569, mAP50-95 0,317, D40 0,522); özet satırı da
  0,609 (results.csv'de en yüksek epoch 38, 0,6088).
- **Süre ölçüsü (2026-11-08 notu):** "Ortam, süre" sütunundaki baseline–e4 süreleri (ör. e3 8 sa 22 dk) Kaggle
  versiyonunun **toplam çalışma süresi** (kurulum, eğitim sonu doğrulama, zip dahil). Parantezdeki "eğitim döngüsü" ise
  results.csv `time` sütununun son değeri (eğitim başından son epoch'a; log'daki "epochs completed in X hours" ile aynı
  ölçü, e5 V5, e6 ve e7'de birebir tuttuğu doğrulandı). Deneyleri karşılaştırırken **eğitim döngüsü** kullanılır; tüm
  koşular için elde var. Ör. e3 7 sa 5 dk ↔ e6 5 sa 5 dk. Farkın ~1,6 sa'i **1. epoch**'tan: e3'te 6.658 s, e6'da 942 s
  (e2 ve e4'te de 1. epoch 1–2 sa; büyük olasılıkla Kaggle'da verinin diskten ilk okunması, doğrulanmadı). Kalan fark
  epoch başına ~384 s ↔ ~354 s (%8); cls_pw hesap yükünü değiştirmediği için oturum/donanım farkı.
- **e5 (iki oturum):** V4 epoch 1–26, Kaggle'ın 12 saat sınırı yüzünden `MAX_HOURS` ile durduruldu; V5 `MODE="devam"` ile
  `last.pt`'den resume, epoch 27–50, 50 epoch normal bitti. Süre (eğitim döngüsü, results.csv `time`; resume'da sütun
  sıfırdan başlıyor): V4 21.915 s = 6 sa 5 dk (süre sınırıyla durduğu için log'da "epochs completed" satırı yok; devir
  notundaki 6,30 sa oturum süresi) + V5 24.612 s = 6 sa 50 dk (log'daki "24 epochs completed in 6.837 hours" ile aynı)
  = **12 sa 55 dk** (≈ 13 sa). args.yaml'daki `optimizer: MuSGD` ve `warmup_bias_lr: 0.0` resume'dan geliyor (e3'ün
  checkpoint'inde de aynı); gerçek fark yalnızca imgsz.
- **e5 ölçümü:** `evaluate.py --imgsz 1024`, batch 16 (GTX 1650'de bellek yetti); modele giren tensörün 1024x1024
  olduğu çıktıda doğrulandı (2026-11-07'de evaluate.py ve measure_fps.py'ye eklenen kontrol).
- **e6:** args.yaml'da e3'ten tek gerçek fark `cls_pw 0.0 → 0.5` (diğerleri `name`, `save_dir`). Checkpoint'te
  `cls_pw 0.5`, MuSGD, batch 16; modeldeki sınıf ağırlıkları D00 0,66 / D10 0,98 / D20 1,04 / D40 1,32 (D40/D00 = 2,0,
  karekök ters frekans). Ölçüm `evaluate.py` imgsz 640, batch 16; tensör 640x640 doğrulandı.
- **e7:** args.yaml'da e3'ten tek gerçek fark `data: data.yaml → data_d40x2.yaml` (diğerleri `name`, `save_dir`).
  Checkpoint'te MuSGD, batch 16, imgsz 640, `cls_pw 0.0`. Oversampling kanıtı: yerel veride D40 içeren train görüntüsü
  2.991 → liste 24.202 satır → ⌈24.202/16⌉ = 1.513 adım/epoch (e3: 1.326). Kaggle'ın `train_batch` numarası buna uyuyor:
  e3 53.040 = 40 × 1.326, e7 60.520 = 40 × 1.513 (numara 40 × adım, çünkü resim close_mosaic'in başladığı epoch 41'de
  çiziliyor). Süre: 1. epoch 863 s; epoch başına (2–50) ~432 s, e3 ~385 s → ×1,12 (liste ×1,14 uzun). Ölçüm
  `evaluate.py` imgsz 640, batch 16; tensör 640x640 doğrulandı.
- Yorumlar: [adim-6-karsilastirma.md](adimlar/adim-6-karsilastirma.md).
