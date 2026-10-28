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

## Sırada
1. Zip'i Kaggle'a private dataset olarak yükle (Hakan'ı collaborator ekle).
2. Notebook'u Kaggle'a import et, GPU T4 + Internet aç, dataset'i input olarak ekle.
3. Deneme koşusu → 1. epoch'tan sonra durdur → resume ile devam ettir. Epoch süresini not al (plan.md açık konu 1: kota hesabı).
4. Asıl eğitim (Save & Run All).

## Karşılaşılan sorunlar
1. **`PurePosixPath` ve `./`:** `PurePosixPath("./images/train/X.jpg").parts` → `("images", "train", "X.jpg")`; baştaki `.`
   parçalara girmiyor. Etiket yolu yanlış kuruldu, `check_sources` 28.887 eksik dosya bulup zip yazmadan durdu. Düzeltildi.
   Ders: kaynak kontrolünü yazmadan önce yapmak hatayı ucuza yakaladı.

## Hocaya nasıl anlatırız
"Veriyi Kaggle'a ham değil, hazırladığımız YOLO formatında yükledik; zip'i oluşturan script listelerdeki her satırın
zip içinde karşılığı olduğunu kontrol ediyor. Kaggle oturumu 12 saatle sınırlı olduğu için eğitim her epoch'ta
checkpoint kaydediyor; bunu önce kısa bir denemede bilerek yarıda kesip kaldığı yerden devam ettirerek test ettik."
