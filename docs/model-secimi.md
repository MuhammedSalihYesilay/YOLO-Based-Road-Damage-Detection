# Model seçimi: neden YOLO26s, imgsz 1024 (e5)?

**Final model (2026-11-08): e5 — YOLO26s, imgsz 1024.** GTX 1650'de 25,0 FPS (hedef 15), CPU'da 4,2 FPS; bu yüzden
GPU'su olmayan bilgisayarlarda kamera için **YOLO26n (e4)** yedek model (CPU 23,4 FPS).
Seçim iki aşamada yapıldı: önce mimari (2026-11-02: YOLO26s, §1–6), sonra aynı mimaride ayar deneyleri
(2026-11-08: imgsz 1024, §7). Karar kayıtları: [kararlar.md](kararlar.md) (2026-11-02, 2026-11-08). Sayıların kaynağı:
[deneyler.md](deneyler.md) ve `docs/degerlendirme/<model>_val/` altındaki özet CSV'ler. Ayrıntılı yorumlar:
[adim-6-karsilastirma.md §6](adimlar/adim-6-karsilastirma.md).

## Kısa özet (sunumdan önce bak)
Tüm sayılar val seti, yerel ölçüm (`evaluate.py`, FP32). "Puan" = mAP'de 0,01. Her deney bir öncekinden **tek bir
şeyi** değiştiriyor.

| Deney | Ne değişti | Val mAP50 (yerel FP32) | Sonuç | Neden seçilmedi / neden seçildi |
|---|---|---|---|---|
| baseline | YOLOv8s, 640 (referansla aynı mimari) | 0,571 | Karşılaştırma noktası | Diğer s modellerinin gerisinde (e3'ten −1,8) |
| e2 | Model: YOLO11s | 0,582 | baseline'dan +1,1 | e3'ten −0,7 (ayrılamıyor); çukurda (−2,3) ve Japonya+Hindistan'da (−1,5) e3 önde |
| e3 | Model: YOLO26s | 0,589 | Mimari olarak seçildi (2026-11-02) | Sonraki deneylerin tabanı oldu; 640'ta kaldığı için e5 geçti |
| e4 | Model: YOLO26n (en küçük) | 0,560 | e3'ten −2,9 | Ana model için zayıf; CPU'da 23,4 FPS → **yedek kamera modeli** |
| **e5** | **imgsz 640 → 1024** | **0,609** | **e3'ten +2,0 → FİNAL MODEL** | En yüksek mAP50; Norveç +10,0, ince çatlaklar (D00 +2,6, D10 +3,2); GPU'da 25 FPS, hedef tutuyor |
| e6 | Sınıf ağırlığı `cls_pw 0.5` | 0,590 | e3'ten +0,1 | 1 puanın altında; çukurda recall ↑ precision ↓, AP değişmedi |
| e7 | Çukurlu görüntüler 2 kez (oversampling) | 0,593 | e3'ten +0,4 | 1 puanın altında; ama çukurda AP +2,0 (recall +8,2, precision −4,1) |

Birleşik model (1024 + D40 ×2) yapılmadı: kurala göre iki ayarın da ayrı ayrı kazandırması gerekiyordu. Zaman ve kota
kalırsa final teslimden önce isteğe bağlı deney / gelecek çalışma.

**Hocaya böyle anlat**
- **1 puan kuralı:** Deneylerden önce koyduk: bir değişiklik val mAP50'yi en az 1 puan artırmıyorsa "kazandırdı"
  demiyoruz. Her modeli tek seed'le eğittik, daha küçük farklar şans eseri çıkabilir.
- **Tek değişken:** Her deneyde yalnızca bir şeyi değiştirdik; veri, epoch, batch, seed, optimizer ve ölçüm script'i
  aynı kaldı. Böylece bir fark çıkınca nedenini biliyoruz.
- **1024 neden kazandı:** Norveç görüntüleri büyük, hasarlar küçük; 640'a küçültünce kutuların ~%23'ü 8 pikselin altına
  iniyor. 1024'te Norveç +10 puan, ince çatlaklar (boyuna, enine) +3 puan civarı. Bedeli hız: 50'den 25 FPS'e indi ama
  15 hedefinin üstünde.
- **Oversampling ve çukur:** Çukurlu görüntüleri iki kez göstermek genel sonucu değiştirmedi ama çukurda AP'yi 2 puan
  artırdı: model çukurların %43'ü yerine %51'ini buluyor, biraz daha fazla yanlış alarmla. Raporda bulgu olarak
  yazıyoruz, 1024 ile birleştirmeyi gelecek çalışma olarak bırakıyoruz.

---

> **Bölüm 1–6 mimari seçimini anlatır (2026-11-02):** YOLO26s seçildi; sonraki deneyler (e5–e7) bu modelle yapıldı.
> Final seçim (e5) için §7.

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

## 7. Final seçim: YOLO26s, imgsz 1024 (e5) (2026-11-08)
YOLO26s ile, ayarlar e3 ile aynı, tek değişken değişerek üç deney yapıldı; her biri **e3'e karşı** karşılaştırıldı:
| | e3 (640) | **e5 (1024)** | e6 (`cls_pw 0.5`) | e7 (D40 ×2) |
|---|---|---|---|---|
| Hedef | — | Norveç'teki küçük çatlaklar | Çukur (D40): kayıpta ağırlık | Çukur (D40): veri tekrarı |
| **mAP50** | 0,589 | **0,609** | 0,590 | 0,593 |
| e3'e fark (1 puan kuralı) | — | **+2,0 (kazandırıyor)** | +0,1 (kazandırmıyor) | +0,4 (kazandırmıyor) |
| D40 AP50 | 0,500 | 0,516 | 0,503 | **0,520** |
| Norveç | 0,280 | **0,380** | 0,308 | 0,316 |
| Japonya+Hindistan (referans 0,547) | 0,537 | **0,544** | 0,534 | 0,531 |
| FPS GTX 1650 / CPU | 50,5 / 9,9 | 25,0 / 4,2 | 51,9 / 11,0 | 51,8 / 10,9 |
| Eğitim döngüsü (results.csv) | 7 sa 5 dk | 12 sa 55 dk (2 oturum) | 5 sa 5 dk | 6 sa 7 dk |

- **e5 seçildi:** 1 puan kuralını geçen tek ayar; artış 4 sınıfın hepsinde, en çok Norveç ve ince çatlaklarda.
  Japonya+Hindistan'da referansa fark 0,3 puan (val'de ön karşılaştırma).
- **Bedeli hız:** GTX 1650'de 25,0 FPS, 15 hedefini tutuyor. CPU'da 4,2 FPS; GPU'suz bilgisayarda kamera için **YOLO26n
  (e4)** yedek (CPU 23,4 FPS).
- **Birleşik model yapılmadı:** koşul (1024 **ve** bir D40 yöntemi ayrı ayrı kazandırmalı) sağlanmadı. e7'nin çukur
  bulgusu (D40 +2,0) raporda yer alır; birleşik model (tahmini ~14,7 sa, iki Kaggle oturumu) zaman ve kota kalırsa
  isteğe bağlı deney / gelecek çalışma.
- Test setinde (Adım 9) yalnızca e5 ölçülür. Ayrıntı: [adim-6-karsilastirma.md §6.5–6.7](adimlar/adim-6-karsilastirma.md).

---

## 8. Hocaya nasıl anlatırım
"Dört YOLO modelini aynı veri, aynı ayarlar, aynı optimizer ve aynı ölçüm script'iyle karşılaştırdık; değişen tek
şey modeldi. En yüksek doğruluk YOLO26s'te: mAP50 0,589. Deneylerden önce bir kural koymuştuk: fark 1 puandan azsa
daha hızlı modeli seçeceğiz. YOLO26s ile YOLO11s arasındaki fark 0,7 puan olduğu için kural YOLO11s'i gösteriyordu.
Ama kuralın hıza bakma nedeni kamera hedefiydi ve iki model de hedefin üç katı hızlı. Öte yandan bundan sonraki
deneylerin hedeflediği üç noktada, yani çukur sınıfında, referansla karşılaştırdığımız Japonya+Hindistan'da ve
Norveç'te YOLO26s önde. Bu yüzden kuraldan bilinçli olarak saptık ve gerekçesini kayda geçirdik. En küçük model
YOLO26n doğrulukta 3 puan geride ama CPU'da saniyede 23 kare işleyen tek model; onu GPU'suz bilgisayarlar için yedek
kamera modeli olarak tutuyoruz. Sonra YOLO26s üzerinde üç ayarı tek tek denedik: görüntü boyutunu 1024'e çıkarmak
mAP50'yi 2 puan artırdı ve kuralımızı geçen tek ayar oldu; çukur sınıfı için denediğimiz iki dengeleme yöntemi genel
sonucu 1 puandan az değiştirdi. Final model bu yüzden 1024 piksellik YOLO26s."

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
Kaggle'ın haftalık 30 saatlik GPU kotası ve GTX 1650'nin hızı sınırlı. Bir topluluk sonucuna göre (Hugging Face model kartı, hakemsiz) RDD2022'de m modelinin s'ye üstünlüğü
~0,6 puan; bizde de n → s farkı (2,9 puan) nesiller arası farktan büyük çıktı, ama s → m'nin kazancı küçük bekleniyor.
Kalan kotayı Norveç (1024) ve çukur (D40) gibi bilinen zayıflıklara ayırmayı daha verimli bulduk.
