# Yol Hasarı Tespit Sistemi — Bitirme Projesi

## Proje özeti
Yol görüntülerinden 4 tür hasarı (3 çatlak türü + çukur) tespit eden bir sistem.
**Ana kapsam = proje önerisi** (`docs/proje-onerisi.md`): YOLO modeli eğitimi,
standart metriklerle değerlendirme ve Streamlit web arayüzü (görüntü yükleme,
video yükleme, gerçek zamanlı kamera; kutu + sınıf + güven skoru).

**Ek özellikler (ana kapsam bitince, zaman kalırsa, öncelik sırasıyla):**
GPS eşleştirme → veritabanına kayıt → harita gösterimi → aynı hasarın zaman içinde takibi.

- Ekip: 2 kişi (ben + Ahmet Hakan Yıldırım, GitHub: hakan0363, repoda collaborator). Her hafta birbirimize yaptıklarımızı anlatırız;
  ikimiz de projenin tamamını sunabilmeliyiz.
- Teslim: ara rapor 23 Kas 2026 23:00, vize sunumu 24 Kas 2026; final Aralık sonu / Ocak başı (çizelge: `docs/plan.md` §8)
- Dil: Python 3.13 (Kaggle/Colab ile aynı; yedek 3.12)
- SDG: 11. Sürdürülebilir şehirler ve topluluklar
- Kategori: Construction / Architecture

## Teknolojiler
- Python 3.13 (python.org) + venv; GPU: GTX 1650 (sürücü 617.42, torch CUDA 13.0 / cu130)
- PyTorch (Ultralytics'in altındaki derin öğrenme kütüphanesi)
- Ultralytics YOLO (eğitim, değerlendirme, tahmin)
- OpenCV (görüntü/video/kamera işleme)
- Streamlit + streamlit-webrtc (web arayüzü, gerçek zamanlı kamera)
- pandas, matplotlib (analiz ve grafikler)
- Git / GitHub (repo: github.com/MuhammedSalihYesilay/YOLO-Based-Road-Damage-Detection, Public, dal main)
- Eğitim: ağır eğitim Kaggle'da (yedek Colab); analiz, dönüştürme, küçük denemeler, değerlendirme,
  FPS ölçümü ve arayüz yerelde (ayrıntı: docs/kararlar.md)
- Model ağırlıkları (`best.pt`) git dışında, GitHub Releases'ta

## Kesinleşen kararlar
- Konu: yol hasarı (çatlak/çukur) tespiti
- Model yaklaşımı: YOLO tabanlı nesne tespiti
- Sınıflar: 4 hasar türü. Sıra eğitimdeki sınıf sırasıyla birebir aynı olmak zorunda,
  çünkü model sınıf numarası döndürüyor. Veri setinde D kodları yok, sınıflar isimle
  (`classTitle`) geçiyor; eşleme isimle yapılır:
  - 0: D00 — Longitudinal Crack (boyuna çatlak) — `longitudinal crack`, 26.196 etiket
  - 1: D10 — Transverse Crack (enine çatlak) — `transverse crack`, 11.875 etiket
  - 2: D20 — Alligator Crack (timsah çatlağı) — `alligator crack`, 10.617 etiket
  - 3: D40 — Pothole (çukur) — `pothole`, 6.544 etiket. Not: D40 yalnızca çukur değil,
    etiket detayı "rutting, bump, pothole, separation" (tekerlek izi oturması, tümsek,
    çukur, ayrışma)
  - Kullanılmayacaklar:
    - `other corruption` (5.850 etiket) atılacak. İki alt türü var: white line blur (D44, şerit
      çizgilerinin silinmesi) ve crosswalk blur (D43, yaya geçidi çizgilerinin silinmesi).
      Bunlar boya aşınması, asfalt hasarı değil; 4 sınıfımızın dışında.
    - `block crack` (blok çatlak) ve `repair` (yamalı/onarılmış bölge) meta.json'da tanımlı
      ama hiçbir görüntüde etiketi yok (0 etiket).
    - Görüntüler silinmez; sadece bu kutular YOLO etiketlerine yazılmaz. Tek etiketi
      `other corruption` olan görüntüler boş (arka plan) görüntüye dönüşür.
- Veri seti: datasetninja.com "road-damage-detector" (RDD2022, 47.420 görüntü, 12,86 GB)
  - Konum: `data/rdd2022/`
  - Web sitesi: https://datasetninja.com/road-damage-detector/
  - Format: Supervisely JSON — `train|test/{ann,img,meta}`, etiketler `ann/*.jpg.json`,
    hepsi dikdörtgen (bbox). Pascal VOC XML değil.
  - Etiketli görüntü: train'deki 38.385 (61.082 etiket). Test klasöründeki 9.035 görüntü
    etiketsiz; sadece görsel demo için kullanılabilir.
  - Etiketli verinin tamamı kullanılacak
  - Çin Drone görüntüleri de eğitime dahil edilecek (dikkatli ele alınacak)
  - Lisans: CC BY-SA 4.0. Kaynak/atıf: Arya, Maeda, Sekimoto vd., "RDD2022: A multi-national
    image dataset for automatic Road Damage Detection", 2022, arXiv:2209.08538
- Veri bölme: resmi test seti etiketsiz olduğu için etiketli train verisi
  %80 train / %10 val / %10 test olarak ayrılacak, seed 42, ülke + boş/dolu katmanlı;
  boş görüntüler yalnızca train'de ~%10'a indirilir
- Norveç uzun kenar 1280'e küçültülür; eğitim imgsz 640 (seçilen modelde 1024).
  Sınıf dengesizliği baseline'da ele alınmaz (Adım 6). Ayrıntı: docs/kararlar.md (2026-10-27)
- Referans proje: RoadDamageDetection-main
  - Konum: `reference/RoadDamageDetection-main/`
  - PyCharm'da sistem Python'u 3.10 ile CPU'da çalıştırıldı (README: Py 3.8, ultralytics 8.0.201)
  - Hazır modelin yeni ultralytics'te açılması Adım 0'da test edilecek (ayrıntı: docs/arastirma/python-surumu.md)
  - Sadece Japonya + Hindistan ile, YOLOv8s, imgsz 640, mosaic=0, 100 epoch eğitilmiş;
    kendi val bölmesinde mAP50 = 0,547
  - Dönüştürücüsü Pascal VOC XML bekliyor; bizim veri setinde doğrudan kullanılamaz
  - LICENSE dosyası yok: kodu kopyalanmaz, incelenip kendimiz yazarız, raporda atıf verilir
- Arayüz: Streamlit ile web (görüntü, video, gerçek zamanlı kamera)
- Backend: tamamen Python (Spring Boot yok)
- Sistem bileşenleri: ana kapsam = tespit modeli + değerlendirme + Streamlit arayüzü;
  ek özellik = GPS eşleştirme + veritabanı + harita + takip
- Farklı YOLO modelleri (YOLOv8s, YOLO11s, YOLO26s; kamera için YOLO26n) ve augmentation
  yöntemleri karşılaştırılacak (ayrıntı: docs/arastirma/yolo-modelleri.md)

## Değerlendirme
- Metrikler: Precision, Recall, F1, mAP50 (ana metrik), mAP50-95, sınıf başına AP,
  confusion matrix, PR eğrisi, çıkarım hızı (ms/görüntü, FPS) (açıklamalar: docs/ogrenme/metrikler.md)
- Kırılımlar: ülke bazında (özellikle Norveç, China_Drone) ve sınıf bazında
- Hedef: test setimizin Japonya+Hindistan alt kümesinde mAP50 ≥ 0,547 (referansın
  **raporladığı** değer; farklı görüntülerde ölçüldüğü için karşılaştırma yaklaşık).
  Gerçek zamanlı kamerada GTX 1650'de ≥ 15 FPS.
- Test parçası yalnızca en sonda, seçilen model için bir kez kullanılır; model seçimi val ile yapılır.
- Referansın hazır modeli (`YOLOv8_Small_RDD.pt`) bizim test setimizde **ölçülmez**:
  aynı havuzdaki Japonya+Hindistan train görüntüleriyle eğitildi (veri sızıntısı).
  Sadece arayüzün çalıştığını test etmek için kullanılır.

## Veri seti notları
Görüntü boyutları ülkeye göre farklı (train sayıları; datasetninja'daki ülke sayıları train+test toplamıdır):
- Japonya: 10.506 görüntü. Çoğu 600x600 (10.187), ayrıca 540x540 (124), 1024x1024 (147), 1080x1080 (48)
- Çek Cumhuriyeti: 2.829 görüntü, 600x600
- Hindistan: 7.706 görüntü, 720x720. Orijinali 960x720'den sıkıştırılmış, en-boy oranı bozuk; dokunulmuyor
- ABD: 4.805 görüntü, 640x640
- Çin: iki alt küme, ikisi de 512x512. China_Drone 2.401 (yukarıdan çekim; test klasöründe yok),
  China_MotorBike 1.977
- Norveç: 8.161 görüntü, üç boyut: 4040x2035 (4.342), 3643x2041 (2.896), 3650x2044 (923).
  Datasetninja "tipik 3650x2044" diyor ama veride en az görülen boyut bu. CVAT ile etiketlenmiş
  (diğerleri LabelImg).

Boş (etiketsiz) train görüntüleri: 12.658 (%33). Norveç %64, Çek %62, Hindistan %51, ABD %0.
`other corruption` atılınca 14.522 (%37,8).

## Henüz karar verilmeyenler
- (Ek özellik) Veritabanı ve harita teknolojisi (öneri: SQLite + folium)
- (Ek özellik) GPS verisi nereden gelecek (telefon, video metadata, vb.)

## Klasör yapısı
```
yol-hasari/
  CLAUDE.md        ← bu dosya
  README.md, .gitignore, requirements.txt
  docs/            ← plan.md, kararlar.md, proje-onerisi.md, arastirma/, ogrenme/
  docs/rapor/ozel/ ← (git dışı)
  data/            ← veri seti (git'e girmez)
  reference/       ← referans proje (sadece okunur, değiştirilmez)
  src/             ← bizim kodumuz (analysis/, data/)
  data/yolo/       ← YOLO formatlı veri + data.yaml (prepare_yolo.py çıktısı, git dışı)
  src/kaggle/      ← Kaggle'a yüklenecek zip'i hazırlayan script (pack_dataset.py)
  data/kaggle_upload/ ← Kaggle'a yüklenecek zip (pack_dataset.py çıktısı, git dışı)
  notebooks/       ← Kaggle eğitim notebook'ları (train_baseline.ipynb)
```

## Çalışma kuralları (Claude için)
- Benimle Türkçe konuş, kısa ve net ol.
- Kod yazmadan önce planı göster, onayımı al. Ne yaptığını ve neden yaptığını açıkla;
  projeyi anlamam ve sunabilmem gerekiyor.
- Her adımda bu adımda ne öğreneceğimi ve hocaya nasıl anlatacağımı açıkla.
- Önemli bir karar alındığında `docs/kararlar.md` dosyasına tarih, karar ve gerekçe olarak ekle,
  bu dosyadaki ilgili bölümü de güncelle.
- `reference/` içindeki dosyaları değiştirme, sadece incele.
- Veri setindeki görüntüleri tek tek açma; analiz için script yaz ve örneklem kullan.
- `data/`, `reference/`, `venv/`, `runs/`, `*.pt`, `*.onnx`, `__pycache__/`, `kaggle.json` git'e girmez (`.gitignore`).
  Commit mesajlarına Co-Authored-By / "Generated with Claude Code" satırı ekleme.
- Ortam: Windows, PowerShell, VS Code. Python sanal ortamı (venv) kullan.
- CLAUDE.md veya docs içindeki bilgilerle çelişen bir şey görürsen değiştirmeden önce bana göster ve onay al.
