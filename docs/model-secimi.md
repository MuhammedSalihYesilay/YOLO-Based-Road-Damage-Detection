# Model seçimi: neden YOLO26s? (2026-11-02)

**Karar:** Sonraki deneyler (görüntü boyutu 1024, çukur sınıfı için dengeleme) **YOLO26s** ile yapılacak.
**YOLO26n** GPU'su olmayan bilgisayarlar için yedek kamera modeli olarak kalacak.
Karar kaydı: [kararlar.md, 2026-11-02](kararlar.md). Sayıların kaynağı: [deneyler.md](deneyler.md) ve
`docs/degerlendirme/<model>_val/` altındaki özet CSV'ler. Ayrıntılı yorumlar:
[adim-6-karsilastirma.md §6.1–6.4](adimlar/adim-6-karsilastirma.md).

---

## 1. Hangi modelleri, neden karşılaştırdık?
| Deney | Model | Neden seçildi |
|---|---|---|
| baseline | **YOLOv8s** | Referans projeyle aynı mimari ve boyut. Referansın 0,547'siyle karşılaştırmanın dayanağı |
| e2 | **YOLO11s** | Bir sonraki nesil; daha az parametreyle COCO'da daha iyi. Olgun, yaygın kullanılan sürüm |
| e3 | **YOLO26s** | En yeni sürüm (Ocak 2026); küçük nesneler için yenilikler (STAL), sadeleşmiş başlık (DFL yok) |
| e4 | **YOLO26n** | En küçük ve en hızlı model. "s yerine n kullanınca ne kaybederiz?" sorusu ve kamera için |

Üç **s** modeli (aynı boy, farklı nesil) "en doğru model hangisi" sorusunu; **n** modeli ise "boyu küçültmenin
bedeli ne" sorusunu cevaplıyor. Model seçimi: [yolo-modelleri.md](arastirma/yolo-modelleri.md).

## 2. Karşılaştırmayı adil yapmak için neleri sabit tuttuk?
Dört modelde **yalnızca model değişti**; geri kalan her şey aynıydı:
- **Veri:** aynı train / val bölmesi (RDD2022, 4 sınıf, ülke + boş/dolu katmanlı, seed 42). Train 21.211, val 3.838 görüntü.
- **Eğitim ayarları:** COCO ön-eğitimli ağırlıklar, imgsz 640, 50 epoch, batch 16, patience 10, seed 42, Ultralytics
  varsayılan augmentation, cache kapalı, Kaggle T4. Her koşunun `args.yaml`'ı kontrol edildi.
- **Optimizer:** `optimizer=auto` bırakıldı; Ultralytics dört modelde de **MuSGD** seçti (checkpoint'lerden doğrulandı).
  Yani farklar optimizer'dan değil, mimariden geliyor.
- **Ölçüm yöntemi:** Kaggle'ın eğitim sonu değeri değil, dört model de **aynı script'le** (`src/eval/evaluate.py`),
  **aynı bilgisayarda**, FP32, val setinde ölçüldü. Hız `src/eval/measure_fps.py` ile GTX 1650 ve CPU'da, kameradaki
  gibi tek tek görüntüyle (batch 1) ölçüldü.
- **Test seti kullanılmadı:** seçim yalnızca val ile yapıldı; test seti seçilen modelle en sonda bir kez kullanılacak.

## 3. Sonuçlar: dört model yan yana (val seti)
| | baseline (YOLOv8s) | e2 (YOLO11s) | **e3 (YOLO26s)** | e4 (YOLO26n) |
|---|---|---|---|---|
| **mAP50** (ana metrik) | 0,571 | 0,582 | **0,589** | 0,560 |
| mAP50-95 | 0,286 | 0,294 | 0,294 | 0,281 |
| D40 (çukur) AP50 | 0,464 | 0,477 | **0,500** | 0,458 |
| Japonya+Hindistan mAP50 (referans 0,547) | 0,522 | 0,522 | **0,537** | 0,509 |
| Norveç mAP50 | **0,295** | 0,265 | 0,280 | 0,239 |
| FPS GTX 1650 (hedef ≥ 15) | 53,2 | 53,4 | 50,5 | **61,2** |
| FPS CPU (hedef ≥ 15) | 9,5 | 10,6 | 9,9 | **23,4** |
| Kaggle eğitim süresi | 4 sa 55 dk (eğitim döngüsü: 4 sa 34 dk, results.csv) | 7 sa 11 dk (eğitim döngüsü: 5 sa 55 dk, results.csv) | 8 sa 22 dk (eğitim döngüsü: 7 sa 5 dk, results.csv) | 5 sa 21 dk (eğitim döngüsü: 4 sa 33 dk, results.csv) |

*Süre notu (2026-11-08):* İlk değerler Kaggle versiyonunun toplam çalışma süresi (kurulum, son doğrulama, zip dahil);
parantezdeki "eğitim döngüsü" results.csv `time` sütunundan, yalnızca eğitim. Karşılaştırma için eğitim döngüsü
kullanılır. Ayrıntı: [deneyler.md](deneyler.md).

Okuma ipucu: "1 puan" = mAP'de 0,01. Örneğin 0,589 − 0,582 = 0,7 puan.

## 4. Seçim kuralı, kuralın sonucu ve neden saptık
**Kural (deneylerden önce, 2026-10-31'de konuldu):** s modelleri içinde val mAP50'si en yüksek olan seçilir. Fark
1 puandan azsa GTX 1650'de daha hızlı olan seçilir. *Neden 1 puan?* Her model tek seed ile bir kez eğitildi; bu
kadar küçük farklar şans eseri de çıkabilir. O durumda kamera için hız belirleyici olsun istedik.

**Kuralın sonucu: YOLO11s (e2).** En yüksek mAP50 YOLO26s'te (0,589), ama YOLO11s ile farkı 0,7 puan (< 1). Kural bu
durumda hıza bakıyor: YOLO11s 53,4 FPS, YOLO26s 50,5 FPS → YOLO11s.

**Neden kuraldan saptık ve YOLO26s'i seçtik:**
1. **Kuralın hıza bakma nedeni kamera hedefiydi.** İki model de GTX 1650'de 15 FPS hedefinin üç katından hızlı. 53 ile
   50 FPS arasındaki fark kamerada hissedilmez; hıza göre seçmek pratikte bir şey kazandırmıyor.
2. **Sonraki deneylerin hedeflediği üç noktada da YOLO26s önde:**
   - **Çukur (D40):** 0,500 / 0,477 → +2,3 puan. D40 deneyleri tam bu sınıf için.
   - **Japonya+Hindistan:** 0,537 / 0,522 → +1,5 puan. Referansın 0,547'sine fark 2,5 puandan 1,0 puana iniyor; ara
     rapordaki ana karşılaştırma bu.
   - **Norveç:** 0,280 / 0,265 → +1,5 puan. 1024 deneyi bu ülke için.
   İlk ikisi 1 puan sınırının üstünde.
3. Genel mAP50'de de YOLO26s en iyisi; fark küçük ama yönü aynı.

**Bedeli:** YOLO26s'in eğitimi YOLO11s'ten ~%16 daha uzun sürdü (8 sa 22 dk / 7 sa 11 dk; eğitim döngüsüyle ~%20: 7 sa 5 dk / 5 sa 55 dk, results.csv). 1024 deneyinde bu fark
büyüyecek ve Kaggle kotasını daha çok zorlayacak. Kuraldan sapma ve gerekçesi kararlar.md'ye açıkça yazıldı.

## 5. YOLO26n'in rolü: yedek kamera modeli
- **Ana model değil:** YOLO26s'e göre mAP50'de 2,9 puan düşük (0,560); en çok çukurda (−4,2) ve küçük nesnelerin olduğu
  Norveç'te kaybediyor. Japonya+Hindistan'da referansın 3,8 puan altında.
- **Ama CPU'da gerçek zamanlı olan tek model:** CPU'da 23,4 FPS (s modelleri ~10 FPS). GPU'su olmayan bir bilgisayarda
  (ör. sunum bilgisayarı) kamera sayfası yalnızca bu modelle 15 FPS hedefini tutturuyor.
- GPU'da n'ye geçmenin faydası küçük (61 / 50 FPS): tek görüntüde GPU zaten tam dolmuyor.
- Bu yüzden üzerinde 1024 / D40 deneyi yapılmayacak; kamera adımında (Adım 8) seçenek olarak sunulacak.

## 6. Sınırlamalar
- **Tek seed:** Her model bir kez eğitildi. Aynı modeli farklı seed'le eğitince sonucun ne kadar oynadığını ölçmedik
  (Kaggle kotası). 1 puandan küçük farklar bu oynaklığın içinde kalabilir.
- **NMS'li ölçüm:** YOLO26'nın tanıtılan "NMS'siz çıkarım" özelliği kullandığımız Ultralytics sürümünde (8.4.182)
  isteğe bağlı; eğitim ve ölçüm varsayılanla, yani NMS'li yapıldı. YOLO26'nın olası hız avantajı bu ölçümde yok.
- **Alt küme oynaklığı:** D40 (586 kutu) ve Japonya+Hindistan (2.280 kutu) genel val'den (5.227 kutu) küçük. Çek (157)
  ve China_Drone (308) gibi alt kümelerde birkaç tahmin sonucu birkaç puan oynatabiliyor.
- **Val, test değil:** Bütün sayılar val setinde. Referansla kesin karşılaştırma Adım 9'da test setinde yapılacak.

## 7. Sırada ne var?
Hepsi **YOLO26s** ile, ayarlar e3 ile aynı, tek değişken değişerek; her biri **e3'e karşı** karşılaştırılacak:
| Deney | Değişen | Hedef |
|---|---|---|
| e5_yolo26s_1024 | imgsz 640 → 1024 | Norveç'teki küçük çatlaklar (640'ta kutuların ~%23'ü 8 pikselin altında) |
| e6_yolo26s_clspw | sınıf ağırlığı `cls_pw 0.5` | Çukur (D40): az örnekli sınıfa kayıpta daha çok ağırlık |
| e7_yolo26s_d40x2 | D40'lı görüntüler 2 kez (oversampling) | Çukur (D40): aynı soruya veri tekrarıyla cevap |
İkisi de kazandırırsa 1024 ile iyi olan D40 yöntemi birleştirilir. Ayrıntı:
[adim-6-karsilastirma.md §2–3](adimlar/adim-6-karsilastirma.md).

---

## 8. Hocaya nasıl anlatırım
"Dört YOLO modelini aynı veri, aynı ayarlar, aynı optimizer ve aynı ölçüm script'iyle karşılaştırdık; değişen tek
şey modeldi. En yüksek doğruluk YOLO26s'te: mAP50 0,589. Deneylerden önce bir kural koymuştuk: fark 1 puandan azsa
daha hızlı modeli seçeceğiz. YOLO26s ile YOLO11s arasındaki fark 0,7 puan olduğu için kural YOLO11s'i gösteriyordu.
Ama kuralın hıza bakma nedeni kamera hedefiydi ve iki model de hedefin üç katı hızlı. Öte yandan bundan sonraki
deneylerin hedeflediği üç noktada, yani çukur sınıfında, referansla karşılaştırdığımız Japonya+Hindistan'da ve
Norveç'te YOLO26s önde. Bu yüzden kuraldan bilinçli olarak saptık ve gerekçesini kayda geçirdik. En küçük model
YOLO26n doğrulukta 3 puan geride ama CPU'da saniyede 23 kare işleyen tek model; onu GPU'suz bilgisayarlar için yedek
kamera modeli olarak tutuyoruz."

### Hocanın sorabileceği sorular
**1. "0,7 puanlık fark gerçek mi, yoksa şans mı?"**
Kesin bilemiyoruz; her model tek seed'le eğitildi. Bu yüzden genel mAP50'ye tek başına dayanmadık. Asıl
gerekçemiz, sonraki deneylerin hedeflediği alt kümelerde (D40 +2,3, Japonya+Hindistan +1,5) 1 puandan büyük ve aynı
yönde farklar. Bunların da tek seed'le ölçüldüğünü sınırlama olarak yazdık.

**2. "Kendi koyduğunuz kuraldan neden saptınız? Bu sonucu istediğiniz yöne çekmek olmuyor mu?"**
Kural deneylerden önce yazıldı ve harfiyen sonucunu (YOLO11s) belgeledik. Sapmamızın gerekçesi kuralın kendi amacına
dayanıyor: hıza bakmanın sebebi kamera hedefiydi ve iki model de hedefin çok üstünde. Seçim val setiyle yapıldı; test
setine hiç bakılmadı, yani sapma test sonucunu etkilemiyor. Karar, gerekçesi ve bedeli (daha uzun eğitim) kayıtlı.

**3. "YOLO26 'NMS'siz' değil miydi, neden hızlı çıkmadı?"**
Kullandığımız Ultralytics sürümünde NMS'siz mod isteğe bağlı, varsayılan değil. Eğitim ve ölçümleri varsayılanla
(NMS'li) yaptık; bu yüzden son işleme süresi diğer modellerle aynı (1,4 ms). Ayrıca GTX 1650'de tek görüntüde süreyi
asıl belirleyen sinir ağının hesabı, NMS değil.

**4. "Neden daha büyük bir model (m, l) denemediniz?"**
Kaggle'ın haftalık 30 saatlik GPU kotası ve GTX 1650'nin hızı sınırlı. Literatürde RDD2022'de m modelinin s'ye üstünlüğü
~0,6 puan; bizde de n → s farkı (2,9 puan) nesiller arası farktan büyük çıktı, ama s → m'nin kazancı küçük bekleniyor.
Kalan kotayı Norveç (1024) ve çukur (D40) gibi bilinen zayıflıklara ayırmayı daha verimli bulduk.
