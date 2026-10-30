# Adım 5: Değerlendirme (val seti, 2026-10-30)

## 1. Bu adımda ne yaptık, neden
Adım 4'te eğittiğimiz baseline modeli (YOLOv8s, imgsz 640) kendi bilgisayarımızda **val setinde** ayrıntılı ölçtük.
Kaggle yalnızca genel ve sınıf bazında sonuç veriyordu. Biz ek olarak ülke bazında, "Drone hariç" ve
"Japonya+Hindistan" sonuçlarını hesapladık ve modelin GTX 1650'de saniyede kaç görüntü işlediğini (FPS) ölçtük.
Test setine bilerek bakmadık; test, model seçildikten sonra Adım 9'da bir kez kullanılacak.

---

## 2. Metrikler: basit açıklama

**Önce IoU (örtüşme oranı).** Modelin çizdiği kutu ile gerçek (etiket) kutunun ne kadar üst üste geldiğini ölçer:
`IoU = kesişim alanı / birleşim alanı`. 1 = tam üst üste, 0 = hiç değmiyor.
*Örnek:* İki kutu 100 piksel² ortak alana sahip, birleşimleri 200 piksel² → IoU = 0,5.

Bir tahmin **doğru (TP)** sayılır, eğer sınıfı doğruysa ve gerçek bir kutuyla IoU'su eşiğin (ör. 0,5) üstündeyse.
Aksi halde **yanlış pozitif (FP)**. Hiçbir tahminin yakalamadığı gerçek kutu **kaçırılmış (FN)** sayılır.

| Metrik | Ne sorar | Örnek |
|---|---|---|
| **Precision (P, kesinlik)** | Modelin "hasar var" dediklerinin ne kadarı gerçekten hasar? `TP / (TP + FP)` | Model 10 kutu çizdi, 7'si doğru → P = 0,70 |
| **Recall (R, duyarlılık)** | Gerçek hasarların ne kadarını bulabildi? `TP / (TP + FN)` | Görüntülerde 10 çukur var, model 6'sını buldu → R = 0,60 |
| **F1** | P ve R'nin dengeli ortalaması: `2·P·R / (P + R)` | P 0,70, R 0,60 → F1 ≈ 0,65 |
| **AP (ortalama kesinlik)** | Güven eşiği yüksekten düşüğe indirilirken P–R eğrisinin altındaki alan. Tek eşiğe bağlı değil | Model hem kesin hem kapsayıcıysa AP 1'e yaklaşır |
| **mAP50** | Her sınıfın AP'si (IoU ≥ 0,5 ile) hesaplanır, 4 sınıfın ortalaması alınır. **Ana metriğimiz** | D00 0,57, D10 0,57, D20 0,68, D40 0,46 → ort. 0,571 |
| **mAP50-95** | Aynı hesap IoU 0,50, 0,55, …, 0,95 olmak üzere 10 eşikte yapılıp ortalanır. Kutunun **tam yerinde** olmasını da ister, daha serttir | Bizde 0,286: kutular hasarı genelde buluyor ama sınırları tam oturmuyor |

**P ve R hangi eşikte?** Model her kutuya bir güven skoru verir. Tablolardaki P ve R, 4 sınıfın ortalama F1'ini
en yüksek yapan güven eşiğinde verilir; Ultralytics de böyle yapar.

**Neden mAP50-95 düşük?** Çatlakların sınırı belirsizdir: "çatlak nerede bitiyor" sorusunun tek doğru cevabı yok.
Etiketleyen kişiler de kutuları farklı genişlikte çizmiş (Adım 3'te Norveç'te gevşek kutular gördük). Bu yüzden
yüksek IoU eşiklerinde puan düşüyor. Ana metrik olarak mAP50'yi seçmemizin bir nedeni bu, diğeri referansla
karşılaştırma (referans da mAP50 raporluyor).

**Confusion matrix (karışıklık matrisi):** Satırlar modelin tahmini, sütunlar gerçek sınıf.
Ör. gerçek D00 (boyuna çatlak) sütunu: 2.489 etiketin 1.871'i doğru D00, 202'si D10, 179'u D20, 42'si D40 sanılmış,
195'i hiç bulunamamış ("background" satırı). Not: Ultralytics bu matrisi val'in çok düşük güven eşiğiyle (0,001)
çiziyor. Bu yüzden "background" sütunundaki yanlış alarm sayıları (on binler) gerçek kullanımı yansıtmıyor. Arayüzde
eşik ~0,25 olacak.

---

## 3. Sonuçlar (val seti, yerel ölçüm, FP32)

### 3.1 Genel
| Görüntü | Kutu | P | R | F1 | **mAP50** | mAP50-95 |
|---|---|---|---|---|---|---|
| 3.838 | 5.227 | 0,621 | 0,541 | 0,578 | **0,571** | 0,286 |

*Yorum:* Model gerçek hasarların yarısından biraz fazlasını buluyor (R 0,54). "Hasar" dediklerinin yaklaşık üçte
ikisi doğru (P 0,62). Bu, bundan sonraki her deneyin karşılaştırılacağı baseline değer.

### 3.2 Sınıf bazında
| Sınıf | Etiket | P | R | F1 | AP50 | AP50-95 |
|---|---|---|---|---|---|---|
| D00 boyuna çatlak | 2.489 | 0,612 | 0,547 | 0,578 | 0,569 | 0,299 |
| D10 enine çatlak | 1.102 | 0,602 | 0,564 | 0,583 | 0,574 | 0,284 |
| D20 timsah çatlağı | 1.050 | 0,678 | 0,625 | 0,650 | **0,679** | 0,365 |
| D40 çukur | 586 | 0,589 | 0,426 | 0,495 | **0,464** | 0,195 |

*Yorum:* En iyi sınıf D20 (timsah çatlağı). Geniş, ağ gibi desenli bir alan olduğu için ayırt etmesi kolay. En zayıf
sınıf D40 (çukur): hem en az örneği olan sınıf (train'de D00'ın ~¼'ü), hem de içinde tümsek, tekerlek izi gibi
farklı görünen hasarlar var. Recall'u 0,43, yani çukurların yarısından fazlası kaçıyor. Adım 6'daki dengesizlik
denemelerinin hedefi bu sınıf.

### 3.3 Ülke bazında
| Ülke | Görüntü | Kutu | P | R | F1 | mAP50 | mAP50-95 | AP50 D00 | AP50 D10 | AP50 D20 | AP50 D40 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| China_MotorBike | 197 | 439 | 0,860 | 0,836 | 0,848 | **0,882** | 0,530 | 0,827 | 0,888 | 0,959 | 0,856 |
| ABD | 480 | 1.083 | 0,651 | 0,549 | 0,596 | 0,607 | 0,348 | 0,740 | 0,635 | 0,702 | 0,349 |
| China_Drone | 240 | 308 | 0,590 | 0,550 | 0,570 | 0,593 | 0,345 | 0,619 | 0,755 | 0,320 | 0,680 |
| Japonya | 1.051 | 1.582 | 0,571 | 0,542 | 0,556 | 0,558 | 0,260 | 0,530 | 0,474 | 0,687 | 0,539 |
| Çek Cumhuriyeti | 283 | 157 | 0,508 | 0,407 | 0,452 | 0,445 | 0,201 | 0,567 | 0,511 | 0,411 | 0,292 |
| Hindistan | 771 | 698 | 0,444 | 0,455 | 0,449 | 0,405 | 0,178 | 0,324 | 0,195 | 0,655 | 0,446 |
| Norveç | 816 | 960 | 0,560 | 0,304 | 0,394 | **0,295** | 0,130 | 0,384 | 0,323 | 0,348 | 0,127 |

*Yorum:*
- **Norveç en zayıf (0,295).** Recall 0,30: hasarların %70'i bulunamıyor. Neden: Norveç görüntüleri çok büyük
  (4040 px) ve 640'a küçültülünce kutuların ~%23'ü 8 pikselin altına iniyor (Adım 2 analizi). Ayrıca etiket kutuları
  gevşek. Seçilen modelde imgsz 1024 denemesi tam bu sorun için (Adım 6).
- **Hindistan zayıf (0,405), özellikle enine çatlakta (0,195).** Hindistan görüntüleri 960x720'den 720x720'ye
  sıkıştırılmış. Yatay daralma enine (yatay) çatlakların görünüşünü bozuyor olabilir.
- **China_MotorBike çok iyi (0,882):** Yakın çekim, düzgün ve tek tip görüntüler; hasarlar büyük ve net.
- **China_Drone orta (0,593):** Yukarıdan çekim farklı bir bakış açısı. Timsah çatlağı (0,320) burada zayıf, çünkü
  yukarıdan bakınca ağ deseni yerden çekimdekinden farklı görünüyor.
- **Çek (0,445):** Val'de yalnızca 157 kutu var. Az örnek olduğu için bu sayı oynak, dikkatli yorumlanmalı.
- Ülke mAP'lerinin ortalaması genel mAP'ye eşit değildir. Genel mAP tüm görüntüler birlikte sıralanarak
  hesaplanır; bu yüzden her alt küme ayrıca hesaplandı.

### 3.4 Özel alt kümeler
| Alt küme | Görüntü | Kutu | P | R | F1 | mAP50 | mAP50-95 | AP50 D00 | AP50 D10 | AP50 D20 | AP50 D40 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Tümü | 3.838 | 5.227 | 0,621 | 0,541 | 0,578 | 0,571 | 0,286 | 0,569 | 0,574 | 0,679 | 0,464 |
| Drone hariç | 3.598 | 4.919 | 0,618 | 0,535 | 0,574 | 0,568 | 0,282 | 0,566 | 0,553 | 0,690 | 0,462 |
| Japonya+Hindistan | 1.822 | 2.280 | 0,548 | 0,520 | 0,533 | **0,522** | 0,236 | 0,465 | 0,462 | 0,676 | 0,483 |

*Yorum:*
- **Drone hariç ≈ Tümü (0,568 / 0,571).** Drone görüntülerini eğitime katmak yer seviyesindeki sonuçları bozmamış.
  "Drone dahil edilecek" kararı (CLAUDE.md) bu ölçümle destekleniyor.
- **Japonya+Hindistan (0,522), genelden düşük.** İçindeki Hindistan (0,405) ortalamayı aşağı çekiyor.

---

## 4. Referansın 0,547'siyle ön karşılaştırma
Referans proje Japonya+Hindistan verisiyle mAP50 **0,547** raporluyor. Bizim modelin val setinin Japonya+Hindistan
alt kümesindeki değeri **0,522**: yaklaşık 2,5 puan geride.

**Bu karşılaştırma neden kesin değil:**
1. **Farklı görüntüler:** Referansın 0,547'si kendi val bölmesinde ölçüldü, bizimki bizim val bölmemizde. İki
   bölmenin görüntüleri aynı değil.
2. **Val, test değil:** Kesin karşılaştırma Adım 9'da test setinde, seçilen modelle yapılacak.
3. **Farklı görev genişliği:** Referans yalnızca Japonya+Hindistan'la eğitildi; modelin tüm kapasitesi bu iki ülkeye
   ayrılmış. Bizim model 7 alt kümeyi birlikte öğreniyor (Norveç, Drone vb.). Aynı model boyutunda bu, iki ülkede
   biraz puan kaybettirebilir.
4. **Farklı ölçüm ortamı:** Referansın kullandığı ultralytics 8.0.201 ve ölçüm ayarları bizimkiyle aynı değil. Kendi
   ölçümümüzde bile ortam farkı ~2 puan yaratabiliyor (bkz. §6).

**Sonuç:** Baseline hedefin biraz altında. Adım 6'daki deneyler (YOLO11s/YOLO26s, augmentation, dengesizlik) bu farkı
kapatmayı hedefliyor.

---

## 5. Hız (FPS) — GTX 1650 ve CPU
Val setinden ülke oranlı 201 görüntü seçildi (Norveç dahil). Görüntüler önce belleğe okundu, sonra kameradaki gibi
**tek tek** işlendi. Ölçülen süre model.predict'in tamamı: ön işleme + çıkarım + son işleme. FP32, imgsz 640.

| Cihaz | Görüntü | ms/görüntü (ort.) | medyan | en yavaş %5 | **FPS** | ön işleme | çıkarım | son işleme |
|---|---|---|---|---|---|---|---|---|
| GTX 1650 | 201 | 18,8 | 19,8 | 21,4 | **53,2** | 1,7 | 15,3 | 1,4 |
| CPU | 50 | 104,9 | 102,1 | 127,3 | **9,5** | 2,7 | 100,0 | 0,7 |

*Yorum:* **15 FPS hedefi GPU'da rahatça tuttu** (53 FPS, hedefin ~3,5 katı). Süreyi asıl belirleyen çıkarım (sinir
ağının hesabı). Kamerada video çözme ve tarayıcıya gönderme de zaman alacağı için gerçek FPS daha düşük olacak, ama pay
geniş. CPU'da 9,5 FPS: GPU'suz bir bilgisayarda gerçek zamanlıya yetmez, görüntü ve video yükleme için yeterli.
Not: aynı ölçüm iki kez çalıştırıldı (53,2 ve 53,3 FPS); sonuç kararlı.

---

## 6. Kaggle (0,589) ile yerel ölçüm (0,571) farkı
Kaggle eğitim bittiğinde val mAP50 **0,589** verdi. Aynı `best.pt` ile bizim script'imiz **0,571** ölçtü.

**Ne denendi:**
| Deneme | Sonuç | Ne gösterdi |
|---|---|---|
| Etiket sayıları karşılaştırıldı (confusion matrix sütunları) | Birebir aynı (D00 2.489, D10 1.102, …) | Veri aynı; fark tahminlerde |
| Batch 32 (Kaggle'ın son ölçümündeki gibi) | 0,571 | Batch boyutu etkilemiyor |
| CPU'da ölçüm | 0,571 | GTX 1650'ye özgü bir hata değil |
| FP16 ile ölçüm (Kaggle'ın son ölçümü FP16 yapılıyor) | **0,04 (bozuk)** | GTX 1650'de FP16 kullanılamaz, Kaggle'ın koşusu yerelde birebir tekrarlanamaz |

Kaggle'da eğitim AMP (yarı hassasiyet) ile yapıldığı için son ölçüm de FP16 ile yapılıyor. Bizim ölçümümüz FP32.
Farkın kalan nedeni araştırılmadı; konu kapatıldı.

**Karar (kararlar.md, 2026-10-30):** Bütün modeller bizim `evaluate.py` ile yerelde FP32 ölçülecek ve **yerel değer
esas alınacak**. Baseline = **0,571**. Kaggle'ın 0,589'u yalnızca "eğitim sonu değeri" olarak not edilir.
*Neden:* Tüm deneyler aynı yolla ölçülürse karşılaştırma adil olur. Yerel ölçüm üç farklı ayarda aynı sonucu verdi
(kararlı) ve herkes tarafından tekrar üretilebilir. **FP16 kararı:** GTX 1650'de FP16 bozuk sonuç verdiği için FPS
ölçümü ve arayüz FP32 ile yapılacak.

---

## 7. Script'ler ve çalıştırma
Komutlar proje klasöründen (`C:\dev\yol-hasari`), PowerShell'de çalıştırılır.

### `src/eval/evaluate.py`: doğruluk ölçümü
```powershell
.\venv\Scripts\python.exe src\eval\evaluate.py --weights runs/kaggle/baseline_v8s/weights/best.pt --name baseline_v8s
```
Süre ~2 dk (GTX 1650). Sonraki modeller için yalnızca `--weights` ve `--name` değişir (imgsz 1024 modelinde
`--imgsz 1024`). Test seti (yalnızca Adım 9): `--split test --final`. `--final` yazılmazsa script durur.

**Nasıl çalışıyor:** Val bir kez koşar. Ultralytics her görüntü için "hangi tahmin hangi gerçek kutuyla eşleşti"
bilgisini hesaplıyor ama iş bitince siliyor. Biz Ultralytics'in val sınıfından küçük bir alt sınıf yazıp bu bilgiyi
silinmeden önce sakladık. Sonra her görüntünün ülkesini `split.csv`'den bulup ülke ve alt küme sonuçlarını
Ultralytics'in kendi `ap_per_class` fonksiyonuyla hesapladık. *Neden:* Her alt küme için ayrı val koşturmak 10 kat
uzun sürerdi ve `data/yolo/` altına yeni cache dosyaları yazılırdı.

| Fonksiyon / sınıf | Ne yapar |
|---|---|
| `BreakdownValidator` | Ultralytics'in `DetectionValidator`'ı + görüntü adlarını ve görüntü başına sonuçları saklar |
| `compute_metrics` | Seçilen görüntülerin sonuçlarını birleştirip P, R, F1, mAP50, mAP50-95, sınıf başına AP50 hesaplar |
| `per_class_table` | Sınıf bazında tablo |
| `subset_table` | Tümü, Drone hariç, Japonya+Hindistan ve 7 ülke tablosu |
| `to_markdown` | Tabloyu `summary.md` için Markdown'a çevirir |
| `main` | Argümanlar, test koruması, val koşusu, **tutarlılık kontrolü** (bizim "Tümü" = Ultralytics'in sonucu, değilse durur), dosyaları yazma ve docs'a kopyalama |

### `src/eval/measure_fps.py`: hız ölçümü
```powershell
.\venv\Scripts\python.exe src\eval\measure_fps.py --weights runs/kaggle/baseline_v8s/weights/best.pt --name baseline_v8s
```
Süre ~1 dk. Seçenekler: `--imgsz`, `--n` (GPU görüntü sayısı, 200), `--n-cpu` (50; 0 = CPU atlanır), `--warmup` (20).

| Fonksiyon | Ne yapar |
|---|---|
| `sample_by_country` | Val'den her ülkeden orantılı rastgele görüntü seçer (seed 42) |
| `sync` | GPU'nun işini bitirmesini bekler; yoksa süre eksik ölçülür (GPU asenkron çalışır) |
| `measure` | 20 görüntülük ısınma (ilk çağrılar CUDA başlatma yüzünden yavaş), sonra tek tek tahmin ve süre |
| `main` | GPU + CPU ölçümü, `fps.csv`, hedefle karşılaştırma |

---

## 8. Çıktılar nerede
| Yer | İçerik | Git |
|---|---|---|
| `docs/degerlendirme/baseline_v8s_val/` | `summary.md`, `per_class.csv`, `per_subset.csv`, `fps.csv`, `confusion_matrix.png`, `confusion_matrix_normalized.png`, `BoxPR_curve.png` | ✅ girer |
| `runs/eval/baseline_v8s/val/` | Yukarıdakiler + Ultralytics'in tüm grafikleri (F1/P/R eğrileri, örnek tahmin görüntüleri) | ❌ dışı |
| `runs/eval/baseline_v8s/fps.csv` | FPS ham sonucu | ❌ dışı |
| `docs/deneyler.md` | Tüm deneylerin özet tablosu (ilk satır baseline) | ✅ girer |

---

## 9. Karşılaşılan sorunlar
1. **`val.cache` yeniden yazıldı.** Ultralytics etiketleri okurken `data/yolo/labels/val.cache` adında bir önbellek
   dosyası tutuyor. Adım 3'teki smoke test (400 val görüntüsü) da aynı dosya adını kullanmıştı. İlk koşuda
   Ultralytics cache'in tam val listesine (3.838) ait olmadığını görüp yeniden yazdı. Görüntü ve etiketler
   değişmedi; ikinci koşudan itibaren dosyaya dokunulmadı. Smoke test tekrar koşulursa cache yine değişir; zararsız.
2. **Kaggle–yerel farkı (0,589 / 0,571):** §6.
3. **GTX 1650'de FP16 bozuk:** mAP50 0,04. FP32 kullanılıyor.

---

## 10. Bu adımda ne öğrendim
- IoU ile doğru/yanlış tahminin nasıl belirlendiği; precision, recall, F1 ve AP'nin farkı.
- mAP50 ile mAP50-95 farkı: ilki "buldu mu", ikincisi "kutuyu tam oturttu mu" diye sorar. Çatlakta sınır belirsiz
  olduğu için mAP50-95 doğal olarak düşük.
- Tek sayı yanıltıcı: genel 0,571 iyi görünürken Norveç 0,295. Kırılım yapmadan bu görünmezdi.
- Alt küme mAP'si ayrı hesaplanır, ülke değerlerinin ortalaması genel mAP değildir.
- Confusion matrix nasıl okunur ve hangi eşikte çizildiğine neden dikkat etmek gerekir.
- Hız ölçümünde ısınma turu ve GPU senkronizasyonu neden gerekli.
- Aynı model farklı ortam ve hassasiyette (FP16/FP32) farklı sonuç verebilir. Bu yüzden tüm deneyleri tek ve sabit
  bir ölçüm yoluyla ölçüyoruz.
- Test setini sona saklamanın anlamı: val'de ne kadar ölçüm yaparsak yapalım, test "görülmemiş" kalıyor.

## 11. Hocaya nasıl anlatırım
"Modeli tek bir sayıyla değil, sınıf ve ülke bazında ölçtük. Val setinde genel mAP50 0,571. En iyi sınıf timsah
çatlağı (0,68), en zayıfı çukur (0,46); çukur en az örneği olan sınıf. Ülkelere bakınca en büyük sorunun Norveç
olduğunu gördük (0,30). Görüntüler çok büyük, 640'a küçültünce çatlaklar birkaç piksele iniyor. Bunu Adım 6'da daha
büyük görüntü boyutuyla deneyeceğiz. Referans projenin 0,547'sine karşılık bizim Japonya+Hindistan alt kümesinde val'de
0,522 aldık. Kesin karşılaştırmayı en sonda test setinde yapacağız. Hız ölçümünü hedef donanımda, kameradaki gibi kare
kare yaptık: GTX 1650'de 53 FPS, gerçek zamanlı hedefimiz 15 FPS. Ölçüm tutarlılığı için tüm modelleri kendi
yazdığımız tek bir script'le, aynı bilgisayarda ölçüyoruz."
