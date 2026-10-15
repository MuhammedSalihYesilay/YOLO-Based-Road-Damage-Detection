# Metrikler: basit anlatım (yol hasarı örnekleriyle)

## Temel kavram
Model her tahmin için bir **kutu**, bir **sınıf** ve bir **güven skoru** (0–1) verir. Her tahmin şu üç durumdan birine düşer:
- **TP (doğru pozitif):** Gerçekten çukur olan yere "çukur" dedi.
- **FP (yanlış pozitif, yani yanlış alarm):** Gölgeye ya da yamaya "çukur" dedi.
- **FN (kaçırma):** Gerçek bir çatlağı hiç bulamadı.

## Metrikler
| Metrik | Ne demek, yol hasarı örneği | Unutmamak için | Projede neden bakacağız |
|---|---|---|---|
| **IoU** | Tahmin kutusu ile gerçek kutunun örtüşme oranı: kesişim alanı / birleşim alanı. Çukurun gerçek kutusunu yarı yarıya kapsayan bir tahminde ≈ 0,5; kutular tam üst üsteyse 1. | "İki kutu ne kadar üst üste?" | Bir tahminin "doğru" sayılması için eşik olarak kullanılır (genelde IoU ≥ 0,5). Diğer bütün metriklerin temeli. |
| **Precision (kesinlik)** | Modelin "hasar" dediklerinin yüzde kaçı gerçekten hasar. 10 yere "çukur" dedi, 8'i gerçek → 0,80. | "Dediğine güvenebilir miyim?" (yanlış alarm ölçüsü) | Düşükse belediye boşuna ekip gönderir. Güven eşiği yükseldikçe artar. |
| **Recall (duyarlılık)** | Gerçek hasarların yüzde kaçını buldu. Yolda 20 çukur var, 15'ini buldu → 0,75. | "Kaçırdığı var mı?" | Düşükse tehlikeli çukurlar gözden kaçar. Güven eşiği düştükçe artar. |
| **F1** | Precision ile recall'un dengeli ortalaması (harmonik ortalama). Biri çok düşükse F1 de düşer. | "İkisini birden tek sayıda özetler." | Streamlit'teki varsayılan güven eşiğini F1'in en yüksek olduğu noktadan seçeceğiz. |
| **AP (ortalama kesinlik)** | Tek bir sınıf için, güven eşiği baştan sona değiştirilirken çizilen precision–recall eğrisinin altında kalan alan. Eşikten bağımsız tek bir puan verir. | "Bir sınıfın genel karnesi." | mAP'ın yapı taşı. |
| **mAP50** | Dört sınıfın AP'lerinin ortalaması; IoU ≥ 0,5 olan tahmin doğru sayılır. | "Kutu yaklaşık doğruysa yeter." | **Ana metrik.** Referansın 0,547'si bu ölçüyle raporlanmış; model seçimi de buna göre yapılacak. |
| **mAP50-95** | Aynı hesap IoU 0,50, 0,55 … 0,95 eşiklerinde ayrı ayrı yapılır ve ortalaması alınır. Kutunun yerini çok hassas bulmayı ödüllendirir. | "Kutu ne kadar tam oturmuş?" | İkincil metrik. Çatlakların kutu sınırları belirsiz olduğu için düşük çıkması normal. mAP50'de berabere kalan modelleri ayırmak için kullanılır. |
| **Sınıf başına AP** | Her hasar türü için ayrı AP. Ör. çukur 0,74, enine çatlak 0,54. | "Hangi hasarda iyi, hangisinde kötü?" | D40'ı (az örnekli sınıf) ve dengesizlik deneylerinin etkisini görmek için. |
| **Confusion matrix (karışıklık matrisi)** | Satırlar gerçek sınıfı, sütunlar tahmini gösterir. "Boyuna çatlakların %15'i enine çatlak sanıldı" ya da "%20'si hiç bulunamadı (arka plan)" gibi bilgiler verir. | "Model neyi neyle karıştırıyor?" | Çatlak türleri arasındaki karışmayı ve arka plana verilen yanlış alarmları görmek için. Hata analizinin (Adım 9) temeli. |
| **PR eğrisi** | Güven eşiği değiştikçe precision'ın (dikey eksen) ve recall'un (yatay eksen) nasıl değiştiğini gösteren grafik. Sağ üst köşeye yaklaşan eğri iyidir; altında kalan alan AP'dir. | "Eşiği oynatınca ne kazanıp ne kaybediyorum?" | Sınıfları ve modelleri görsel olarak karşılaştırmak için; raporda grafik olarak yer alacak. |
| **ms/görüntü** | Bir görüntünün işlenme süresi (ön işleme + model + son işleme), milisaniye cinsinden. | "Bir kare kaç ms sürüyor?" | Hangi modelin kamerada kullanılabileceğine karar vermek için; GPU'da ve CPU'da ayrı ölçülür. |
| **FPS** | Saniyede işlenen kare sayısı ≈ 1000 / ms. Ör. 50 ms → 20 FPS. | "Görüntü akıcı mı?" | Gerçek zamanlı kamera hedefi: GTX 1650'de ≥ 15 FPS. |

## Projede neye nasıl bakacağız
- **Model seçimi:** val'de mAP50; eşitlik olursa mAP50-95 ve hız.
- **Referans karşılaştırması:** test setinin Japonya+Hindistan alt kümesinde mAP50.
- **Dengesizlik ve D40:** sınıf başına AP.
- **Norveç ve Drone:** ülke bazında mAP50.
- **Hata analizi:** confusion matrix ve örnek FP/FN görüntüleri.
- **Arayüz:** varsayılan güven eşiği F1'in en yüksek olduğu nokta; kamera modeli FPS'e göre seçilecek.
