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
