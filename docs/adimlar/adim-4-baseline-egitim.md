# Adım 4: Baseline eğitim (YOLOv8s, imgsz 640)

## Ne yaptık, neden (2026-10-28)
Ağır eğitim Kaggle'da yapılacak ([kararlar.md → 2026-10-18 Kaggle veri ve notebook düzeni](../kararlar.md)).
Bu aşamada yalnızca yüklenecek zip ve Kaggle notebook'u hazırlandı; yükleme ve eğitim tarayıcıdan yapılacak.

## Tekrar üretme
```powershell
# data/yolo/ hazır olmalı (Adım 3). data/kaggle_upload varsa script durur.
.\venv\Scripts\python.exe src\kaggle\pack_dataset.py --yolo data/yolo --out data/kaggle_upload
```

## `src/kaggle/pack_dataset.py`
| Fonksiyon | Ne yapar |
|---|---|
| `to_relative` | Liste satırını `./images/<parça>/<dosya>` biçimine çevirir (ters bölü / mutlak yol gelirse düzeltir; bizim listeler zaten bu biçimde) |
| `read_list`, `label_for` | Listeyi okur; görüntüden etiket yolunu bulur (`images/train/X.jpg` → `labels/train/X.txt`) |
| `check_sources` | Zip yazmadan önce her görüntü ve etiket diskte var mı bakar |
| `write_zip` | Görüntü + etiket + 3 liste + yeni `data.yaml`. Sıkıştırmasız (JPEG zaten sıkışık) |
| `verify_zip` | Zip'teki listelerin her satırının görüntüsü ve etiketi zip içinde var mı |

`data/yolo/` sadece okunur. Zip'e girmeyenler: `train_dropped_empty.txt` (9.498 kenara konan boş), smoke dosyaları,
`split.csv`, `.cache`.

**Zip:** `data/kaggle_upload/rdd2022_yolo.zip` — 2,99 GB, 57.778 dosya (28.887 görüntü + 28.887 etiket +
3 liste + `data.yaml`). Parça sayıları Adım 3 ile aynı: train 21.211 / val 3.838 / test 3.838. `verify_zip` hatasız.

**Notebook mantığının yerel denemesi:** zip'ten parça başına 10 görüntü, Kaggle'daki klasör düzenini taklit eden geçici
bir klasöre açıldı; notebook'taki gibi `path:` içeren yaml yazılıp Ultralytics'e okutuldu → görüntüler ve kutular
doğru bulundu (train 10 görüntü / 18 kutu, val 10 / 14).

## `notebooks/train_baseline.ipynb`
| Bölüm | Ne yapar | Ne zaman |
|---|---|---|
| 1 | `nvidia-smi`, `pip install ultralytics==8.4.182` | Her oturumda |
| 2 | `/kaggle/input` içinde `data.yaml`'ı arar; liste/görüntü/etiket sayılarını 21.211 / 3.838 / 3.838 ile karşılaştırır | Her oturumda |
| 3 | `/kaggle/working/data.yaml` yazar (`path:` input klasörü; input salt okunur) | Her oturumda, resume'dan önce de |
| 4 | Ortak ayarlar + `RUN_TRIAL` / `RESUME` / `RUN_MAIN` bayrakları | Her oturumda |
| (a) | Deneme: v8s, 3 epoch, `name="deneme"` → 1. epoch'tan sonra bilerek durdurulur | İlk oturum |
| (b) | `last.pt` + `resume=True`; yeni oturumda önceki output aynı yola kopyalanır | Deneme durdurulunca / 12 saat dolunca |
| (c) | Asıl eğitim: v8s, 640, 50 epoch, `name="baseline_v8s"` | Deneme + resume başarılıysa, yeni oturumda "Save & Run All" |
| Son | `results.csv` son 5 epoch, en iyi val mAP50, `best.pt` yolu | Her koşudan sonra |

**Eğitim ayarları:** `yolov8s.pt`, imgsz 640, batch 16, workers 4, seed 42, cache kapalı,
`patience=10` (early stopping), `save_period=5`, `project=/kaggle/working/runs` (tam yol).

Kaynaktan doğrulananlar (ultralytics 8.4.182):
- `project` mutlak yolsa olduğu gibi kullanılır; göreliyse başına `runs/detect` eklenir (Adım 3'teki sürpriz bunun sonucuydu).
- Listedeki `./` ile başlayan satırlar, listenin bulunduğu klasöre göre çözülür → zip'teki listeler Kaggle'da değişmeden çalışır.

## Kaggle'da yapılanlar (2026-10-29, tarayıcıdan)

### Yükleme
- Zip private dataset olarak yüklendi; dataset adı **`rdd2022-yolo`** (tireli; notebook açıklamasında `rdd2022_yolo` yazıyor,
  kod `data.yaml`'ı aradığı için fark etmedi). Kaggle zip'i açtı: 57,8 bin dosya, klasör düzeni doğru.
- Notebook import edildi (Kaggle'daki adı `notebook8cccb874dd`). Accelerator **GPU T4 x2**, Internet açık.
  Kodda `device=0` olduğu için eğitim tek T4'te koştu.

### Deneme + resume testi (interaktif oturum)
- Veri kontrolü geçti: 21.211 / 3.838 / 3.838; liste, görüntü ve etiket sayıları tuttu.
- **"Slow image access":** ilk okumada 0,8 MB/s; etiket taraması ~20 dk, **1. epoch ~25 dk**. 2. epoch'tan itibaren dosyalar
  önbellekte: **~3 dk 53 sn eğitim + ~25 sn val ≈ 4,5 dk/epoch**. Yavaşlık sadece ilk okumada; veriyi yerel diske
  kopyalamaya gerek kalmadı.
- **Resume çalıştı:** 1. epoch sonrası durduruldu; `RESUME=True` ile log'da
  `Resuming training .../deneme/weights/last.pt from epoch 2 to 3 total epochs`.
- val mAP50: epoch 1 → 0,131, 2 → 0,203, 3 → 0,329. Oturum ~1 sa 15 dk kota harcadı.

### Asıl eğitim (baseline)
- `RUN_TRIAL=False`, `RESUME=False`, `RUN_MAIN=True` → Save & Run All (Commit), versiyon "baseline v8s".
- `args.yaml`: yolov8s.pt, imgsz 640, epochs 50, batch 16, patience 10, save_period 5, seed 42, cache false, workers 4, amp true.
- Süre **4 sa 55 dk** (T4). 50 epoch'un hepsi bitti, early stopping devreye girmedi; son 5 epoch'ta val mAP50
  0,588–0,590 arasında yatay → model doymuş.

### Sonuç (val seti, `best.pt`)
| Sınıf | P | R | mAP50 | mAP50-95 |
|---|---|---|---|---|
| Tümü | 0,629 | 0,555 | **0,589** | 0,304 |
| D00 boyuna | 0,624 | 0,566 | 0,592 | 0,329 |
| D10 enine | 0,613 | 0,569 | 0,589 | 0,299 |
| D20 timsah | 0,686 | 0,644 | 0,695 | 0,383 |
| D40 çukur | 0,594 | 0,442 | 0,482 | 0,205 |

- Çıkarım 4,2 ms/görüntü (T4; FPS hedefi GTX 1650'de ölçülür, Adım 5).
- **Bu değerler val setinde.** Test setine bakılmadı; referansın 0,547'siyle karşılaştırma Adım 5'te test setinin
  Japonya+Hindistan alt kümesinde yapılacak.
- D40 en zayıf sınıf (en az örnekli sınıf, beklenen) → Adım 6.

### İndirilen dosyalar (yerel, git dışı: `runs/kaggle/baseline_v8s/`)
`weights/best.pt` (22,5 MB), `args.yaml`, `results.csv`, `results.png`, `confusion_matrix*.png`, `Box{F1,P,PR,R}_curve.png`,
`val_batch0_pred.jpg`. İndirilmeyenler (`last.pt`, `epoch*.pt`, `train_batch*.jpg`, `labels.jpg`, `deneme/`) Kaggle'daki
Version 1 Output'unda duruyor.

### Kota
Bu hafta ≈ 6,3 saat (30 saatten). Ölçülen süre: ilk epoch ~25 dk + sonraki her epoch ~4,5 dk → v8s/640/50 epoch ≈ 5 saat.

## Açık işler
- Hakan dataset'e collaborator olarak eklenmedi.
- `best.pt` GitHub Releases'a yüklenmedi (karar 2026-10-18).
- Repodaki notebook'ta bayraklar deneme ayarında (`RUN_TRIAL=True`), Kaggle'daki kopyada `RUN_MAIN=True`; repoda hangisinin
  tutulacağına karar verilecek.
- **Sırada Adım 5:** test seti değerlendirmesi, Japonya+Hindistan alt kümesi, ülke/sınıf kırılımı, GTX 1650'de FPS.

## Karşılaşılan sorunlar
1. **`PurePosixPath` ve `./`:** `PurePosixPath("./images/train/X.jpg").parts` → `("images", "train", "X.jpg")`; baştaki `.`
   parçalara girmiyor. Etiket yolu yanlış kuruldu, `check_sources` 28.887 eksik dosya bulup zip yazmadan durdu. Düzeltildi.
   Ders: kaynak kontrolünü yazmadan önce yapmak hatayı ucuza yakaladı.

## Hocaya nasıl anlatırız
"Veriyi Kaggle'a ham değil, hazırladığımız YOLO formatında yükledik; zip'i oluşturan script listelerdeki her satırın
zip içinde karşılığı olduğunu kontrol ediyor. Kaggle oturumu 12 saatle sınırlı olduğu için eğitim her epoch'ta
checkpoint kaydediyor; bunu önce kısa bir denemede bilerek yarıda kesip kaldığı yerden devam ettirerek test ettik.
COCO'da ön-eğitimli YOLOv8s'i kendi verimize uyarladık (transfer learning): 50 epoch, T4'te ~5 saat, val mAP50 0,589.
Bu bizim baseline'ımız; sonraki her deney bununla karşılaştırılacak. En zayıf sınıf en az örneği olan çukur (0,48)."
