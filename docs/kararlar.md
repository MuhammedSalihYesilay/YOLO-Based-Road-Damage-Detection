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
