# Kararlar

Her kayıt: tarih — karar — gerekçe.

## 2026-10-14 — CLAUDE.md veri setine göre düzeltildi
- **Karar:** CLAUDE.md'deki veri seti bilgileri gerçek veriye göre düzeltildi (`docs/plan.md` A tablosu, madde 1-10 ve 12).
  Sınıflar isimle eşleniyor; format Supervisely JSON; kesin etiket sayıları yazıldı; `other corruption` atılacak;
  38.385 etiketli görüntü var, test klasörü etiketsiz; Japonya ve Norveç boyutları düzeltildi; boş görüntü oranı eklendi.
- **Gerekçe:** Tüm ann JSON'ları sayıldı, görüntü boyutları örneklemle doğrulandı; CLAUDE.md'deki bazı bilgiler tahmini ya da eksikti.

## 2026-10-14 — Isı haritası maddesi kaldırıldı
- **Karar:** "Isı haritası kullanılmayacak (Çin Drone görüntülerinin kullanılabilmesi için)" maddesi CLAUDE.md'den şimdilik kaldırıldı.
- **Gerekçe:** Veri setinde ya da referans projede ısı haritası ile Çin Drone arasında bağlantı bulunamadı; gerekçe belirsizdi.

## 2026-10-15 — A tablosu 13-16 onaylandı
- **Karar:** datasetninja sayfasıyla karşılaştırmadan çıkan maddeler CLAUDE.md'ye işlendi: Hindistan 960x720'den sıkıştırılmış;
  Norveç'in gerçek boyutları ve CVAT ile etiketlenmesi; Japonya'daki ek boyutlar; sitedeki ülke sayılarının train+test toplamı olması.
- **Gerekçe:** Site bazı konularda eksik ya da yanıltıcı; sayılar veriyle doğrulandı, çelişkide veriye güveniliyor.

## 2026-10-15 — Ana kapsam = proje önerisi
- **Karar:** Ana kapsam danışmana verilen öneri (`docs/proje-onerisi.md`): model, değerlendirme, Streamlit arayüzü (görüntü, video, gerçek zamanlı kamera).
  GPS, veritabanı, harita ve hasar takibi ek özellik oldu, zaman kalırsa yapılacak.
- **Gerekçe:** Öneride bu dört özellik yok; teslim süresi sınırlı. Önce taahhüt edilen kapsam bitirilecek.

## 2026-10-15 — Arayüz Streamlit web, backend tamamen Python
- **Karar:** Arayüz Streamlit ile web; backend tamamen Python, Spring Boot yok.
- **Gerekçe:** Öneride teknoloji olarak Streamlit ve Python yazılı. Tek dil öğrenme yükünü azaltıyor; referans proje de Streamlit kullanıyor.

## 2026-10-15 — Referansla karşılaştırma yöntemi
- **Karar:** Karşılaştırmada referansın raporladığı mAP50 = 0,547 kullanılacak. Bizim modelimiz, test setimizin Japonya+Hindistan alt kümesinde ölçülecek.
  Referansın hazır modeli bizim test setimizde ölçülmeyecek, sadece arayüz testi için kullanılacak.
- **Gerekçe:** Hazır model aynı havuzdaki Japonya+Hindistan train görüntüleriyle eğitildi. Bizim test görüntülerimizin bir kısmını görmüş olabilir (veri sızıntısı), bu da sonucu şişirir.
  0,547 farklı görüntülerde ölçüldüğü için karşılaştırma yaklaşık kabul edilecek.

## 2026-10-15 — Python 3.13 (yedek 3.12)
- **Gerekçe:** 3.10'un desteği bitti; Kaggle ve Colab 3.13 kullanıyor; güncel paketlerin hepsi destekliyor. Ayrıntı: [python-surumu.md](arastirma/python-surumu.md)

## 2026-10-15 — Modeller: YOLOv8s, YOLO11s, YOLO26s + kamera için YOLO26n
- **Gerekçe:** YOLOv8s referansla aynı mimari; diğer ikisi yeni nesiller; YOLO26n gerçek zamanlı hız için. Ayrıntı: [yolo-modelleri.md](arastirma/yolo-modelleri.md)

## 2026-10-15 — Eğitim düzeni: aynı ayarlarla 50 epoch + early stopping; seçilen modelde imgsz 640 ve 960/1024 karşılaştırması
- **Gerekçe:** Kaggle kotası sınırlı; Norveç'teki küçük nesneler 640'ta kaybolabiliyor. Ayrıntı: [yolo-modelleri.md](arastirma/yolo-modelleri.md)

## 2026-10-15 — Git/GitHub: repo, .gitignore, commit'ler yalnızca kendi adımızla
- **Karar:** Repo https://github.com/MuhammedSalihYesilay/YOLO-Based-Road-Damage-Detection (Public, `main`). data/, reference/, venv/, runs/, *.pt, *.onnx, __pycache__/, kaggle.json git dışında. Commit'lere Claude satırı eklenmez.
  Ahmet Hakan Yıldırım (GitHub: hakan0363) collaborator olarak davet edildi ve kabul etti (2026-10-18).
- **Gerekçe:** Veri seti 12,9 GB ve lisanslı, referansın lisansı yok, ağırlıklar büyük (nereden indirilecekleri README'de); repo herkese açık olduğu için Kaggle API anahtarı asla girmemeli. Commit geçmişi proje sahiplerini göstermeli.

## 2026-10-18 — Çalışma düzeni: yerel / Kaggle ayrımı
- **Karar:** Ağır eğitim Kaggle'da. Veri analizi, JSON→YOLO dönüştürme, bölme, küçük deneme eğitimi, final test,
  değerlendirme, FPS ölçümü ve Streamlit arayüzü yerel bilgisayarda. FPS yalnızca yerelde (GTX 1650) ölçülür.
- **Gerekçe:** Kaggle'ın haftalık 30 saatlik GPU kotası yalnızca eğitime harcanır. FPS hedefi (≥ 15) GTX 1650 için
  tanımlı; bulut GPU'sunda ölçülen hız arayüzün çalışacağı donanımı göstermez.

## 2026-10-18 — Kaggle veri ve notebook düzeni
- **Karar:** Veri Kaggle'a ham haliyle değil, Adım 3'te YOLO formatına çevrilip Norveç küçültüldükten sonra
  private dataset olarak yüklenir; Hakan dataset'e collaborator olarak eklenir ve kendi hesabıyla da eğitim yapabilir.
  Notebook'ta cache kapalı; veri `/kaggle/input`'tan okunur, çıktılar `/kaggle/working`'e yazılır.
- **Gerekçe:** 12,9 GB ham veri yerine küçültülmüş kopya yükleme süresini ve disk kullanımını azaltır.
  Kota hesap başına olduğu için iki hesap iki kat GPU süresi demek. Kaggle hesabı hazır (telefon doğrulandı;
  private dataset 214,75 GB, GPU 30 saat/hafta).

## 2026-10-18 — Model ağırlıkları GitHub Releases'ta
- **Karar:** `best.pt` gibi ağırlıklar git'e girmez; GitHub Releases'a eklenir, README'de bağlantısı verilir.
- **Gerekçe:** `*.pt` dosyaları büyük ve git geçmişini kalıcı olarak şişirir; Releases dosya başına 2 GB'a kadar izin veriyor
  ve repo Public olduğu için hocalar/jüri modeli indirebilir.

## 2026-10-18 — Yerel ortam: python.org Python 3.13 + venv + torch cu130
- **Karar:** venv `venv/` klasöründe, python.org Python 3.13.16 ile (Anaconda'nın 3.13'ü değil). NVIDIA sürücüsü 617.42 olduğu için
  torch'un CUDA 13.0 derlemesi: torch 2.14.1+cu130, torchvision 0.29.1+cu130, ultralytics 8.4.182, opencv-python 5.0.0.93,
  pandas 3.0.6, matplotlib 3.11.2. Sürümler `requirements.txt`'te sabit; dosya cu130 deposunu da içerdiği için CUDA derlemesi
  bu dosyadan kurulunca da geliyor. `torch.cuda.is_available()` → True (GTX 1650, sm_75).
- **Gerekçe:** Anaconda kendi kütüphaneleriyle ayrı bir dağıtım; üzerine kurulan venv'lerde DLL/SSL sorunları çıkabiliyor.
  Sürücü ≥ 580 olduğundan 12.6 yerine güncel 13.0 derlemesi seçildi. Sabit sürümler tekrarlanabilirlik için.

## 2026-10-18 — Referansın hazır modeli yeni ultralytics'te açılıyor
- **Karar:** `YOLOv8_Small_RDD.pt` ultralytics 8.4.182'de doğrudan kullanılacak; ONNX yedek yoluna gerek yok.
- **Gerekçe:** Bir test görüntüsünde (China_MotorBike_001977) GPU'da tahmin üretti (~20 ms çıkarım). Sınıf sırası
  (0 Longitudinal, 1 Transverse, 2 Alligator, 3 Potholes) bizim sıramızla aynı; arayüz testinde eşleme sorunu yok.

## 2026-10-25 — Rapor dosyaları git dışında
- **Karar:** Rapor dosyaları (duyuru, şablon, taslaklar) `docs/rapor/ozel/`'de, `.gitignore`'da. **Gerekçe:** Repo public; Turnitin taslağı kaynak olarak bulup benzerliği şişirebilir.

## 2026-10-27 — Adım 2 veri kararları
- **Norveç:** uzun kenar 1280'e küçültülür (JPEG 95); baseline imgsz 640, seçilen modelde 1024. Gerekçe: kutuların
  %23,5'i 640'ta 8 px altına düşüyor (1024'te %9,9, 1280'de %5,8); 1024 tüm eğitimi ~2,5 kat yavaşlatır.
  Görsel: [arastirma/norvec_cozunurluk_kucultme.html](arastirma/norvec_cozunurluk_kucultme.html)
- **Boş görüntü:** yalnızca train'de ~%10'a indirilir (~2.400, ülke oranlı, seed 42); val/test doğal (%37,8). Gerekçe:
  14.522 boş görüntü var, Ultralytics %0–10 öneriyor; epoch ~%30 kısalır, precision gerçekçi ölçülür.
- **Sınıf dengesizliği:** baseline'da işlem yok; sınıf başına AP ölçülünce Adım 6'da ağırlık/oversampling denenir.
  Gerekçe: D00:D40 ≈ 4:1, orta düzey; önce sorun ölçülür.
- **Bölme:** ülke + boş/dolu katmanlı %80/10/10, seed 42; önce bölünür, boş azaltma sonra yalnızca train'de. Gerekçe:
  sekans sızıntısı işareti yok (ardışık IoU 0,040, rastgele 0,041); önizlemede sınıf oranları en fazla 1 puan farklı.
- **Küçükler:** `Japan_001265.jpg`'daki sıfır boyutlu kutu atılır; China_Drone ayrı ve "Drone hariç" raporlanır;
  Hindistan en-boy oranına dokunulmaz (train/test aynı bozuk, etiketler normalize; raporda sınırlılık).

## 2026-10-27 — Adım 3 uygulama notları
- **Boş azaltma liste ile:** kenara konan 9.498 boş train görüntüsünün dosyaları `data/yolo`'da duruyor, sadece `train.txt`'e
  girmiyor (`train_dropped_empty.txt`). Gerekçe: Adım 6'da "tüm boşlar" denemesi yeniden dönüştürmeden yapılabilir.
- **Kullanılan boş sayısı 2.121** (kararda ~2.400 yazıyordu). Gerekçe: %10 train'in son hâline göre hesaplandı; 2.400 tüm veriden kaba tahmindi.

## 2026-10-29 — Baseline ve ortak eğitim ayarları
- **Karar:** Baseline = YOLOv8s, imgsz 640, 50 epoch (val mAP50 0,589). Adım 6'daki "aynı ayarlar" bu koşunun ayarlarıdır:
  batch 16, patience 10, save_period 5, seed 42, cache kapalı, workers 4, Ultralytics varsayılan augmentation.
- **Gerekçe:** Karşılaştırmada tek değişken değişmeli. Ayarlar T4'te sorunsuz çalıştı (~4,5 dk/epoch, ilk epoch ~25 dk).
  Ayrıntı: [adim-4-baseline-egitim.md](adimlar/adim-4-baseline-egitim.md)

## 2026-10-30 — Adım 5 yalnızca val; test Adım 9'da
- **Karar:** Adım 5'te yalnızca val seti ölçülür. Japonya+Hindistan alt kümesinin val değeri referansın 0,547'siyle
  yalnızca **ön karşılaştırma**; kesin karşılaştırma Adım 9'da, seçilen modelle test setinde bir kez yapılır.
  `evaluate.py` test setini yalnızca `--final` bayrağıyla açar.
- **Gerekçe:** Test seti model seçiminden önce görülürse sonuç iyimser olur ("kopya"). Plan'da Adım 5 için yazılan
  "val/test" bu kararla Adım 9'a kaydı.

## 2026-10-30 — Resmî değer: yerel FP32 ölçüm (evaluate.py)
- **Karar:** Tüm modeller bizim `src/eval/evaluate.py` ile **yerelde, FP32** ölçülür; raporda ve `deneyler.md`'de bu
  değer esas alınır. Baseline val mAP50 = **0,571** (mAP50-95 0,286). Kaggle'ın eğitim sonunda verdiği 0,589 yalnızca
  "eğitim sonu değeri" olarak not edilir.
- **Gerekçe:** Aynı `best.pt` ve aynı val etiketleriyle (sınıf başına etiket sayıları birebir aynı) yerelde 0,571 çıktı.
  Batch 32 ve CPU'da da 0,571 → yerel ölçüm kararlı. Kaggle'ın son ölçümü FP16 ile yapılıyor (eğitimdeki AMP ayarı
  `quantize=16` olarak validator'da kalıyor); fark araştırması burada kapatıldı. Tek, tekrar üretilebilir ölçüm yolu
  deneyleri birbiriyle adil karşılaştırır.
- **FP16:** GTX 1650'de FP16 bozuk sonuç veriyor (val mAP50 **0,04**). FPS ölçümü ve arayüz **FP32** ile yapılır.

## 2026-10-31 — Adım 6 deney sırası ve model seçim kuralı
- **Karar:** Sıra: YOLO11s → YOLO26s → YOLO26n → model seçimi → seçilen modelle imgsz 1024 → D40 sınıf ağırlığı →
  D40 oversampling → (koşullu) birleşik model; zaman kalırsa mosaic kapalı. **Seçim:** baseline dahil s modelleri
  içinden val mAP50'si (yerel FP32) en yüksek olan; fark 1 puandan azsa GTX 1650 FPS'i yüksek olan. YOLO26n ayrıca kamera adayı.
  Birleşik model yalnızca 1024 ve bir D40 yöntemi val'de ayrı ayrı kazandırırsa eğitilir.
- **Gerekçe:** Önce mimari seçilir ki sonraki deneyler tek bir modelde, tek değişkenle yapılsın. Model karşılaştırması
  ara rapora (23 Kas) yetişmesi gereken asıl iş. 1 puandan küçük farklar seed/oturum oynaklığı içinde kalabilir; o
  durumda kamera hedefi için hız belirleyici.
  Ayrıntı: [adim-6-karsilastirma.md](adimlar/adim-6-karsilastirma.md)

## 2026-10-31 — D40 dengeleme: cls_pw 0.5 ve 2× oversampling
- **Karar:** İki ayrı deney. (1) Ultralytics `cls_pw=0.5`: sınıf kaybı ters frekansın karekökü ile ağırlıklandırılır.
  (2) D40 içeren train görüntüleri (2.991 / 21.211) train listesinde 2 kez yazılır (24.202 satır); görüntü kopyalanmaz,
  val/test değişmez.
- **Gerekçe:** D40 en zayıf sınıf (val AP50 0,464, recall 0,43). D00:D40 ≈ 4:1; tam ters frekans (`cls_pw=1`) D40'a
  ~4 kat ağırlık verip D00'ı cezalandırabilir, 0,5 ~2 kat ile daha yumuşak. Ağırlık ve oversampling sorunu farklı
  yollardan çözer (kayıp hesabı / veri sıklığı); ikisini ayrı denemek hangisinin işe yaradığını gösterir.

## 2026-10-31 — Uzun eğitimler: süre sınırıyla düzgün durdurma (MAX_HOURS)
- **Karar:** `train_experiment.ipynb`'de `on_fit_epoch_end` callback'i, bir sonraki epoch `MAX_HOURS`'u aşacaksa
  eğitimi `last.pt` kaydedildikten sonra durdurur; yeni oturumda `MODE="devam"` ile sürdürülür. Varsayılan 11 sa;
  1024 gibi uzun deneyler bilerek daha küçük değerle iki oturuma bölünür. Yeni model/imgsz önce `MODE="deneme"` ile
  (train'in %10'u, 2 epoch, otomatik dur + devam) test edilir.
- **Gerekçe:** Kaggle 12 saatte oturumu zorla keser. Ultralytics normal bitişte `last.pt`'den optimizer'ı silip devamı
  kapatıyor; bizim durdurma bu adımdan önce olduğu için checkpoint devam ettirilebilir kalıyor (trainer.py'de kayıt →
  callback sırası doğrulandı). Ultralytics'in kendi `time` ayarı eğitimi "bitmiş" sayıp devamı engellediği için kullanılmadı.

## 2026-11-02 — Seçilen model: YOLO26s (seçim kuralından bilinçli sapma)
- **Karar:** 1024 ve D40 deneyleri (e5, e6, e7) **YOLO26s** (e3) ile yapılır ve e3'e karşı karşılaştırılır.
  YOLO26n (e4) yedek kamera modeli olarak kalır; üzerinde 1024 / D40 deneyi yapılmaz. Baseline (YOLOv8s) raporda
  referansla aynı mimarideki karşılaştırma noktası olarak kalır.
- **Kuraldan sapma:** 2026-10-31 kuralı harfiyen uygulanınca **YOLO11s (e2)** çıkıyordu: en yüksek val mAP50 e3'te
  (0,589), e2 ile farkı 0,7 puan (< 1) → kural GTX 1650 FPS'i yüksek olanı seçer (e2 53,4 / e3 50,5).
- **Gerekçe:** Kuralın FPS'e bakmasının amacı kamera hedefiydi; iki model de 15 FPS hedefinin üç katından hızlı, aradaki
  fark pratikte önemsiz. Sonraki deneylerin hedeflediği üç noktada e3 önde: D40 AP50 0,500 / 0,477 (+2,3),
  Japonya+Hindistan 0,537 / 0,522 (+1,5; referansın 0,547'sine fark 1,0 puana iniyor), Norveç 0,280 / 0,265 (+1,5).
  Bilinen maliyet ve sınırlar: e3'ün eğitimi ~%16 daha uzun (8 sa 22 dk / 7 sa 11 dk); farklar tek seed ile ölçüldü;
  D40 ve Japonya+Hindistan genel val'den küçük alt kümeler. YOLO26n CPU'da 15 FPS'i geçen tek model (23,4 FPS),
  doğrulukta s modellerinin ~3 puan altında (0,560).
- Ayrıntı: [model-secimi.md](model-secimi.md), [adim-6-karsilastirma.md §6.4](adimlar/adim-6-karsilastirma.md)

## 2026-11-05 — Ara rapor: literatür taraması taslağı, kaynak stili IEEE
- **Karar:** Literatür taraması taslağı hazırlandı; 19 kaynak elle doğrulandı (her biri birincil kaynakta açıldı, birebir
  alıntılı kontrol tablosu, tüm satırlar "Doğru"). Kaynak stili **IEEE** (numaralı [1], [2] …). Hakemsiz/ikincil kaynaklar
  (HF model kartı, bloglar) ve açılamayan sayfalar metne alınmadı.
- **Gerekçe:** Şablon "proper in-text citations" istiyor ama stil belirtmiyor; IEEE mühendislikte standart ve numaralı
  atıf metni kısa tutuyor. Uydurma kaynak riskine karşı her iddia bir alıntıyla bağlandı.
- Ayrıntı: [rapor/literatur-taramasi.md](rapor/literatur-taramasi.md) (git dışı kopyası `rapor/ozel/` altında, ikisi aynı)

## 2026-11-07 — e5 (imgsz 1024): 1024 val'de kazandırıyor, şu anki en iyi aday
- **Karar:** e5 (YOLO26s, imgsz 1024) **şu anki en iyi aday**. Nihai model seçimi e6 ve e7 bitince yapılacak; 1024 ile
  e6/e7'den kazanan ayar birleştirilebilir (birleşik model koşulunun 1024 yarısı sağlandı). `model-secimi.md` ve
  CLAUDE.md'deki "seçilen model" (YOLO26s, e3) nihai seçime kadar değişmez.
- **Gerekçe:** Yerel FP32 val mAP50 **0,609**, e3'ten **+2,0 puan** (1 puan kuralının açıkça üstünde); artış recall'dan
  (+3,1) ve 4 sınıfın hepsinde. Norveç 0,280 → 0,380 (+10,0), D40 0,500 → 0,516 (+1,6), Japonya+Hindistan 0,537 → 0,544
  (+0,7; referansın 0,547'sine 0,3 puan). Bedeli: GTX 1650 FPS 50,5 → 25,0 (15 hedefi tutuyor), CPU 4,2; eğitim ≈ 13 sa
  (e3: 8 sa 22 dk). Tek seed.
- **Eğitim iki oturumda:** V4 epoch 1–26 (`MAX_HOURS` ile durdu, ~6 sa 5 dk results.csv'den) + V5 `MODE="devam"` ile
  resume, epoch 27–50 (6,837 sa, log). args.yaml'daki optimizer/warmup_bias_lr farkı resume kaynaklı (e3 checkpoint'iyle aynı).
- **Kaggle sütunu:** deneyler.md'nin "Kaggle eğitim sonu" sütununa `best.pt` doğrulaması (0,631) yazılır; önceki
  deneylerde de bu değer yazılmıştı (en iyi epoch'la aynıydı). Özet satırındaki 0,633 (epoch 44) not olarak durur.
- **Ölçüm eki:** `evaluate.py` modele giren tensör boyutunu, `measure_fps.py` Ultralytics'in kullandığı imgsz'yi kontrol
  edip çıktıya yazar; istenen imgsz ile tutmazsa durur. Gerekçe: Ultralytics `.pt` modelde giriş boyutunu loglamıyor;
  önceki özetler yalnızca verilen argümanı tekrarlıyordu. Varsayılanlar değişmedi.
- Ayrıntı: [adim-6-karsilastirma.md §6.5](adimlar/adim-6-karsilastirma.md), [deneyler.md](deneyler.md)

## 2026-11-08 — e6 (cls_pw 0.5): val'de kazandırmıyor; birleştirme için tek aday e7
- **Karar:** cls_pw 0.5 val'de **kazandırmıyor** (e6 − e3 = **+0,1 puan**, D40 **+0,3**). 1024 ile birleştirme için tek
  aday **e7** (D40 ×2). **e5** (YOLO26s, imgsz 1024) şu anki en iyi aday olmaya devam ediyor.
- **Gerekçe:** Yerel FP32 val mAP50 0,590 (e3 0,589), 1 puan kuralının çok altında. D40'ta recall 0,430 → 0,464 arttı ama
  precision 0,631 → 0,615 düştü; AP50 0,500 → 0,503. Japonya+Hindistan 0,537 → 0,534. Tek belirgin değişim Norveç
  0,280 → 0,308 (+2,8); ABD'de D40 düşüşüyle −2,3. FPS aynı (GTX 1650 51,9, CPU 11,0). Tek seed.
- **Kontroller:** args.yaml'da e3'ten tek gerçek fark `cls_pw`; checkpoint'teki sınıf ağırlıkları D00 0,66 / D40 1,32
  (oran 2,0, karekök ters frekans), yani ayar gerçekten uygulandı. Kaggle `best.pt` doğrulaması 0,603 deneyler.md'ye
  yazıldı; results.csv'deki en yüksek 0,605 (epoch 37) not.
- **Süre ölçüsü düzeltmesi:** baseline–e4 için yazılan süreler (ör. e3 8 sa 22 dk) Kaggle versiyonunun toplam çalışma
  süresi; e6'nın log'u (5,085 sa) yalnızca eğitim döngüsü. Eski değerler korunur, yanlarına results.csv `time`
  sütunundan "eğitim döngüsü" eklenir (baseline 4 sa 34 dk, e2 5 sa 55 dk, e3 7 sa 5 dk, e4 4 sa 33 dk, e5 6 sa 5 dk +
  6 sa 50 dk = 12 sa 55 dk, e6 5 sa 5 dk); karşılaştırmada bu kullanılır. Bu ölçüyle e3/e2 ~%20 (önce %16), e5/e3 ~1,8 kat
  (önce ~1,5). Önceki kararlar bu oranlara dayanmadığı için değişmez; eski kayıtlar olduğu gibi bırakıldı.
- **e3 ↔ e6 süre farkı (7 sa 5 dk ↔ 5 sa 5 dk):** ~1,6 sa'i 1. epoch'tan (6.658 s ↔ 942 s; muhtemelen Kaggle'da ilk veri
  okuması, doğrulanmadı), kalanı epoch başına ~%8 (oturum/donanım farkı; cls_pw hesap yükünü değiştirmez).
- Ayrıntı: [adim-6-karsilastirma.md §6.6](adimlar/adim-6-karsilastirma.md), [deneyler.md](deneyler.md)

## 2026-11-08 — e7 (D40 ×2): genelde kazandırmıyor; birleşik model yok; final model e5 (YOLO26s, imgsz 1024)
- **Karar:** D40 oversampling (×2) val'de **kazandırmıyor** (e7 − e3 = **+0,4 puan** < 1; e6'ya da aynı kural uygulandı).
  Birleşik model (1024 + D40 ×2) **yapılmaz**. **Final model: e5 (YOLO26s, imgsz 1024).** YOLO26n (e4) GPU'suz
  bilgisayarlar için yedek kamera modeli. `model-secimi.md` ve CLAUDE.md'deki "seçilen model" e5 olarak güncellendi.
- **Gerekçe:** Yerel FP32 val mAP50 0,593 (e3 0,589). Birleşik model koşulu (1024 ve bir D40 yöntemi ayrı ayrı
  kazandırmalı, 2026-10-31) sağlanmadı. e5 yedi deneyin en yükseği (0,609, e3'ten +2,0); GTX 1650'de 25,0 FPS (15 hedefi
  tutuyor), CPU 4,2 FPS. Tek seed.
- **Raporda yer alacak bulgu:** e7 çukurda kazandırıyor: D40 AP50 0,500 → 0,520 (+2,0), recall 0,430 → 0,512 (+8,2),
  precision 0,631 → 0,590 (−4,1). ABD +3,6 (ABD D40 0,348 → 0,458), Norveç +3,6; Japonya+Hindistan 0,531 (−0,6). Diğer
  sınıflarda yan etki küçük (D00, D10 −0,5).
- **Birleşik model:** zaman ve kota kalırsa final teslimden önce isteğe bağlı deney / gelecek çalışma. Tahmini eğitim
  döngüsü ≈ 14,7 sa (e5 12 sa 55 dk × 24.202/21.211), iki Kaggle oturumu; 2026-11-08 itibarıyla kalan kota 10 sa 22 dk.
  1024 ve oversampling'in D40 kazançlarının üst üste eklenip eklenmediği bilinmiyor.
- **Kontroller:** args.yaml'da e3'ten tek gerçek fark `data_d40x2.yaml`; yerel veride 2.991 D40'lı görüntü → 24.202 satır
  → 1.513 adım/epoch, Kaggle `train_batch60520` = 40 × 1.513 ile tutuyor. Kaggle `best.pt` doğrulaması 0,609
  deneyler.md'ye yazıldı (özet satırıyla aynı).
- Ayrıntı: [adim-6-karsilastirma.md §6.7](adimlar/adim-6-karsilastirma.md), [model-secimi.md](model-secimi.md),
  [deneyler.md](deneyler.md)
