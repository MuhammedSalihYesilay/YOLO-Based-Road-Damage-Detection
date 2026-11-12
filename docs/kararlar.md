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

## 2026-11-10 — Literatür taraması düzeltmeleri; raporda yalnızca hakemli / birincil kaynak
- **Karar (literatür metni, `docs/rapor/literatur-taramasi.md` + `ozel/` kopyası):**
  - [5] CRDDC'2022: "More than 60 teams" → **70**. Kaynakçada IEEE sürümü gösteriliyor; IEEE özeti 70, arXiv özeti 60 diyor.
  - [16] Pham vd.: kaynakça arXiv ön baskısından **IEEE Big Data 2022 sürümüne** çevrildi (pp. 6416–6423,
    doi 10.1109/BigData55660.2022.10020856, künye Crossref). "51 teams" → **54 teams** (IEEE gövdesi; arXiv gövdesi 51);
    Google Street View ile veri toplama önerisi eklendi.
  - [7] Faster R-CNN 5 fps'in VGG-16 modeline ait olduğu yazıldı; [9] YOLO'nun daha çok konum hatası / daha az yanlış
    alarm yaptığı eklendi; [14] YOLO26 Progressive Loss eklendi ve tüm ölçümlerin varsayılan one-to-many (NMS'li) başla
    yapıldığı belirtildi; [17] SEA-YOLO v8'in değişiklikleri (SBS, EMA, uyarlanabilir dikkat FPN, LSCD-Head) eklendi
    (SBS için kaynaktaki "optimize" ifadesi kullanıldı); [18] "five model scales" netleştirildi.
  - §5: dört sınıfın RDD benchmark'larından geldiği, `other corruption`'ın (white line blur, crosswalk blur) neden
    atıldığı netleştirildi; final model (YOLO26s, 1024, val mAP50 0,609, GTX 1650'de ~25 FPS) eklendi.
  - LIT bloğu 11.216 karakter (şablon ≥ 8000).
- **Gerekçe:** Her madde birincil kaynaktan (arXiv özeti, Crossref, Semantic Scholar'daki IEEE özeti, PLOS sayfası)
  bağımsız doğrulandı; [5] ve [16]'nın IEEE değerleri kullanıcı tarafından IEEE sayfasında elle doğrulandı. Kaynakçada
  hangi sürüm gösteriliyorsa sayılar o sürümden alınmalı. Doğrulanamayan iddialar (ör. YOLO26-RD'nin görüntü sayısı ve
  sınıfları) metne konmadı. SEA-YOLO'nun Data Availability kısmı "RDD2020" yazıyor ama RDD2022 sitesine bağlanıyor;
  metinde özete (RDD2022) uyuldu, not kontrol tablosunda.
- **Kural:** Raporda kaynak olarak yalnızca hakemli ya da birincil kaynaklar (makale, resmi belge, veri setinin kendi
  yayını) kullanılır. Hugging Face model kartı gibi topluluk sonuçları ve doğrulanamayan (403 veren) kaynaklar
  araştırma notlarında kalabilir ama açıkça işaretlenir: `model-secimi.md` §8 S4 ve `arastirma/yolo-modelleri.md`'deki
  "m'nin s'ye üstünlüğü ~0,6 puan" ifadesi "bir topluluk sonucu (Hugging Face model kartı, hakemsiz)" olarak düzeltildi;
  yolo-modelleri.md'deki MDPI Sensors 2026 sonucu "doğrulanamadı, raporda kaynak olarak kullanılmayacak" diye işaretlendi.
- Ayrıntı: [rapor/literatur-taramasi.md](rapor/literatur-taramasi.md) (Kaynak Kontrol Tablosu, "Dikkat edilecek" 3. madde)

## 2026-11-10 — Literatür taraması sadeleştirildi (son düzenleme)
- **Karar:** LIT metni (`docs/rapor/literatur-taramasi.md` + `ozel/` kopyası) sadeleştirildi:
  - Kaynak özetlerine çok yakın cümleler (özellikle §1 veri setleri, §2 R-CNN / Faster R-CNN / SSD / YOLO tanımları)
    kendi cümlelerimizle, farklı yapıyla yeniden yazıldı; anlam ve sayılar aynı. [17]'deki SBS ifadesi de kendi
    cümlemizle yazıldı ("reduces computational cost").
  - §2'deki gereksiz ayrıntılar çıkarıldı: YOLOv8/YOLO11 çıkış tarihleri, COCO mAP ve parametre sayıları, 45/155 FPS,
    VGG-16 5 fps, %43 CPU, COCO'nun örnek/görüntü sayısı ve YOLOv8'in "resmi makalesi yok" cümlesi. [10] COCO metinde kaldı.
  - Tüm "(this study)" ekleri kaldırıldı; kendi bilgilerimiz "this project" / "our experiments" ile ayrılıyor.
  - §4: 0,547'nin hakemsiz bir GitHub deposundaki PR eğrisi görselinden alındığı ve hangi bölmede ölçüldüğünün
    belirtilmediği yazıldı; değer yalnızca yaklaşık karşılaştırma noktası.
  - §1, §2, §3 sonuna önceki paragraflardan çıkan birer sentez cümlesi eklendi (yeni iddia yok).
  - §5 kısaltıldı: bölme sayıları ve ara sonuçlar (0,589 / 0,582 / 0,571, 15 FPS hedefi) çıktı; üç sürümün aynı
    koşullarda karşılaştırılması, hız ölçümü ve final model (YOLO26s, 1024, val mAP50 0,609, ~25 FPS) tek cümlede.
    "Diğer çalışmalar yalnızca doğruluk raporluyor" iddiası "karşılaştırmalar ağırlıklı olarak doğruluğa dayanıyor"
    diye yumuşatıldı.
  - LIT bloğu 11.220 → **10.012 karakter** (şablon ≥ 8000). Yeni kaynak yok; [1]–[19]'un hepsi metinde geçiyor.
- **Gerekçe:** (1) Özetlere yakın cümleler benzerlik/intihal denetiminde sorun çıkarabilir. (2) Literatür bölümünde
  model tanıtımının sayısal ayrıntısı gereksiz; bu bilgiler Kaynak Kontrol Tablosu'nda ve araştırma notlarında duruyor.
  (3) Referans değerin (0,547) zayıf kaynağını açıkça yazmak, hedefin "yaklaşık" olduğunu dürüstçe gösterir.
  (4) Sentez cümleleri literatürü yalnızca özetlemek yerine bizim çalışmamıza bağlıyor. (5) "Yalnızca doğruluk"
  iddiası tüm kaynaklar için kanıtlanmadığı için yumuşatıldı.
- Metinden çıkan alıntılar Kaynak Kontrol Tablosu'nda kayıt olarak duruyor (tablonun üstünde not var). Türkçe çeviri
  (`ozel/literatur-taramasi-turkce.md`, git dışı) yeni metne göre güncellendi.

## 2026-11-11 — Vize planı: ara rapor + yalnız görüntü prototipi
- **Karar:** Vizeye (ara rapor 23 Kas 23:00, sunum 24 Kas) kadar ara raporun midterm bölümleri bitirilir ve küçük bir
  Streamlit **görüntü** prototipi gösterilir (fotoğraf yükleme, e5 ile tespit, kutu + sınıf + güven skoru, güven eşiği
  kaydırıcısı). Video, kamera, testler, pHash veri sızıntısı kontrolü, test seti ölçümü (Adım 9) ve ek özellikler
  vizeden sonra. Kapsam değişmiyor, yalnız sıra. plan.md §8 ve yol haritası tarihsiz sıra listesine çevrildi.
- **Veri sızıntısı kontrolü (pHash):** val/test görüntülerinden train'deki bir görüntüye çok benzeyenlerin oranı ölçülür;
  yüksekse temiz alt kümede yeniden değerlendirme + raporda sınırlama. Adım 9'dan önce yapılır; Adım 1'deki sekans
  kontrolünden farklı.
- **Gerekçe:** Şablon ara raporda sonuç istemiyor (System Test, Discussion final'de); kalan sürenin çoğu rapor bölümlerine
  gerekiyor. Prototip, önerideki arayüzün çalıştığını vizede göstermek için yeterli. Şablon gövdesi esas alınır
  (duyurudaki liste ile bölüm sırası/numaraları tutmuyor).
- **Not:** Ağırlıklar henüz GitHub Releases'ta değil (`gh release list` boş); prototip e5'i yerelden
  (`runs/kaggle/e5_yolo26s_1024/weights/best.pt`) yükler, Releases'a yükleme vizeden sonra.

## 2026-11-11 — Ara rapor: Standards to be Used
- **Karar:** Standartlar: ISO/IEC/IEEE 29148:2018 (gereksinim), ISO/IEC 25010:2023 (kalite modeli), ISO/IEC/IEEE
  29119-1:2021 ve 29119-3:2021 (test), OMG UML 2.5.1, ASTM D6433-24 (yalnız alan bağlantısı), COCO değerlendirmesi
  (mAP50 = PASCAL VOC metriği, mAP50-95), PEP 8, IEEE kaynak stili. Gereksinimler (29148) şimdiki zaman: bu raporun
  Use Case bölümünde "The system shall ..." biçiminde yazılıyor; kalite (25010) ve test (29119) gelecek zaman.
  ASTM için: sınıflar RDD2022'nin etiketleme şemasını izliyor, kategoriler ilk olarak Japon kılavuzuna (JRA 2013) göre
  tanımlandı, ASTM'den alınmadı; ASTM D6433 de görsel denetimle gözlenen yüzey hasarına dayanıyor, modelin bulduğu da
  görünür yüzey hasarı (sınıf eşlemesi çıkarımı yok); PCI hesaplanmıyor. ISO/IEC 19505 ve ayrı PASCAL VOC kaynağı çıkarıldı. PEP 8 cümlesi yumuşatıldı ("is written
  following PEP 8 conventions"; kod bir stil denetleyicisiyle kontrol edilmedi). Metin 1.465 kr. (2026-11-12 kaynağa yakın ifade düzeltmesiyle 1.442)
  Yeni kaynaklar geçici olarak [20]–[28]; rapor birleştirilirken yeniden sıralanacak.
- **Gerekçe:** Her standart resmî sayfada doğrulandı (iso.org otomatik erişime 403 verdi: ortak standartlar IEEE SA'dan,
  25010 kullanıcı tarafından iso.org'da elle). RDD2022 PDF'inde ASTM/PCI hiç geçmiyor; ASTM'nin resmî sayfasında hasar
  türü listesi yok, bu yüzden adlarıyla eşleme yazılmadı. Testler final döneminde yapılacağı için şimdiki zaman kullanılmadı.
- Ayrıntı: [rapor/standartlar.md](rapor/standartlar.md) (Kaynak Kontrol Tablosu; git dışı kopyası ve Türkçe açıklaması `rapor/ozel/` altında)

## 2026-11-11 — Ara rapor: Legal Consequences; kodun lisansı AGPL-3.0 ile uyumlu seçilecek
- **Karar:** Legal metni dört konu: veri seti lisansı (CC BY 4.0 / CC BY-SA 4.0 çelişkisi, aşağıda), yazılım lisansları (Ultralytics AGPL-3.0, lisanssız
  referans proje), kişisel veri (KVKK 6698, GDPR), sorumluluk (karar destek aracı, son karar insanda: kaynaksız, kendi
  tasarım kararımız). Hukuki yorum yok; yalnız kaynağın dediği ve bizim yaptığımız / yapacağımız. AB Yapay Zekâ Yasası
  ve diğer kütüphane lisansları çıkarıldı. Metin 1.421 kr. (2026-11-12 düzeltmesiyle 1.449); kaynaklar geçici olarak [29]–[37].
- **Kodun lisansı:** Repoda LICENSE dosyası yok. Ultralytics AGPL-3.0 olduğu için kodumuzun lisansı **AGPL-3.0 ile uyumlu**
  seçilecek; dosya şimdi eklenmedi (ne zaman ve hangi lisans: ekip kararı).
- **Kaggle:** YOLO formatlı kopya private yüklendi, herkese açık değil; metinde yalnız bu olgu, hukuki yorum yok.
- **Bulanıklaştırma iddiası çıkarıldı:** "Yüz ve plakalar bulanıklaştırılmış" cümlesi yalnız sekilab README'sinin genel
  "Privacy matters" bölümünde (2018 veri seti bölümünden sonra); RDD2022 makalesinde yok, RDD2022'yi kapsadığı
  doğrulanamadı. GDPR cümlesi somut olguyla: "part of the images was collected in the Czech Republic".
- **Veri seti lisansı çelişkisi:** RDD2022'nin figshare kaydı (DOI 10.6084/m9.figshare.21431547; kullanıcı elle baktı,
  DataCite kaydı da "Creative Commons Attribution 4.0 International") **CC BY 4.0** diyor; veri setinin GitHub
  deposundaki README (sekilab/RoadDamageDetector, "# License", genel başlık) **CC BY-SA 4.0** diyor. Metinde ikisi de
  yazıldı; **daha katı koşullara (CC BY-SA) uyuyoruz:** atıf veriyoruz, uyarlanmış veriyi paylaşırsak aynı lisansla.
  Hangisinin bağlayıcı olduğuna dair hukuki yorum yok. Kaynaklar [36] figshare kaydı, [37] CC BY 4.0 legal code.
  CLAUDE.md, README.md ve plan.md (§2.7, §A) kullanıcı onayıyla bu çelişkiyi gösterecek şekilde güncellendi.
- **Gerekçe:** Lisans ve tanımlar resmî metinlerden doğrulandı (CC legalcode, sekilab/RoadDamageDetector README, gnu.org
  AGPL §13, ultralytics.com/license, GitHub Docs, mevzuat.gov.tr 6698 PDF). GDPR'ın madde metni EUR-Lex'ten okunamadı;
  yalnız AB Yayın Ofisi'ndeki resmî başlık kullanıldı, tanım metne konmadı. Kamera modu henüz yok → gelecek zaman.
- Ayrıntı: [rapor/yasal.md](rapor/yasal.md) (Kaynak Kontrol Tablosu; git dışı kopyası ve Türkçe açıklaması `rapor/ozel/` altında)

## 2026-11-12 — Ara rapor: Effects on Health, Environment and the Problems of the Age
- **Karar:** Dört kısa paragraf: güvenlik ve sağlık (WHO bilgi notu), ekonomik ve çevresel etkiler (NCHRP 720, FHWA
  pavement preservation, projenin kendi enerji maliyeti), toplumsal boyut ve çağın sorunları (Maeda [1], RDD2022 [4],
  final modelin GTX 1650 hızı), güvenli kullanım (kaynaksız tasarım kararı: kamera modu sabit montaj ya da yolcu).
  **Kaza azaltma iddiası yok**; sistemin etkisi yalnız "hasarı daha erken bulmaya yardım". Metin 1.403 kr.; kaynaklar
  geçici olarak [38]–[40]. Motosiklet el kitabı ve SDG hedefleri çıkarıldı (SDG bölümüne bırakıldı).
- **WHO sayısı:** 2023 raporu "1.19 million", Temmuz 2026 bilgi notu "Approximately 1.16 million" diyor; daha güncel
  bilgi notu kullanıldı, rapor kaynakçaya alınmadı.
- **Kendi verimiz:** Yedi deneyin toplam eğitimi (results.csv eğitim döngüleri) 2.774 dk ≈ 46 GPU saati (deneme
  koşuları ve Kaggle kurulumu dahil değil). CO₂ değeri yazılmadı (doğrulanmış hesap yok).
- **Gerekçe:** Her iddia resmî / birincil kaynakta birebir alıntıyla doğrulandı (WHO, NAP + Crossref, fhwa.dot.gov,
  Maeda ve RDD2022 arXiv PDF'leri). Doğrulanamayanlar metne konmadı: erken bakımın çevre faydası (highways.dot.gov 403,
  FHWA-HIF-15-002 404), bakım/çukur ile kaza arasındaki nedensellik (WHO sayfasında yok). Yaşlanan altyapı fikri
  Maeda'da birebir geçtiği için ("aging road infrastructure") kullanıldı.
- **Kendi cümlelerimiz:** İlk taslakta Safety, Economic ve Social paragraflarındaki cümleler kaynak ifadelerine çok
  yakındı (WHO, NCHRP, FHWA, Maeda, RDD2022); literatürdeki kurala göre anlam aynı kalacak şekilde yeniden yazıldı.
- Ayrıntı: [rapor/saglik-cevre.md](rapor/saglik-cevre.md) (Kaynak Kontrol Tablosu; git dışı kopyası ve Türkçe açıklaması `rapor/ozel/` altında)

## 2026-11-12 — Ara rapor: Sustainable Development Goal
- **Karar:** Seçilen hedef SDG 11. Ana bağlantı **11.2'nin yalnız yol güvenliği kısmı** (hedef yılı 2030); toplu taşıma
  kısmı ve 11.2.1 göstergesi metne girmedi. Destekleyici yalnız **9.1** (tek cümle; hedef yılı yok). **3.6 çıkarıldı:**
  resmî metinde hedef yılı 2020 (2026 düzeltmeli çerçevede de değişmemiş), süresi geçmiş; ölüm verileri
  Health/Environment'ta. Katkı "destekler" düzeyinde: hasarın yerini göstererek bakımın daha erken planlanmasına yardım;
  hedefe tek başına ulaştırmaz, yol güvenliğine etkisi ölçülmedi. Metin 1.269 kr.; tek kaynak [41].
- **Kaynak:** BM'nin resmî gösterge çerçevesi (A/RES/71/313, E/CN.3/2026/12 düzeltmesiyle; unstats.un.org PDF);
  sdgs.un.org goal sayfalarıyla birebir aynı. sdgs.un.org Goal 11 sayfası ayrı kaynak olarak eklenmedi.
- **Gerekçe:** Bağlantıyı abartmamak ve Health/Environment'ı tekrar etmemek. BM metinleri kendi cümlelerimizle
  anlatıldı; birebir metinler yalnız Kaynak Kontrol Tablosu'nda.
- Ayrıntı: [rapor/sdg.md](rapor/sdg.md) (Kaynak Kontrol Tablosu; git dışı kopyası ve Türkçe açıklaması `rapor/ozel/` altında)
