# Adım 6: Karşılaştırma deneyleri (val seti)

## 1. Bu adımda ne yapıyoruz, neden
Baseline (YOLOv8s, imgsz 640) val setinde mAP50 **0,571** aldı. Zayıf noktalar belli: **D40 (çukur) 0,464**,
**Norveç 0,295**, Japonya+Hindistan 0,522 (referansın 0,547'sinin altında). Bu adımda baseline'dan **tek bir
değişkeni** değiştirerek eğitimler yapıyoruz ve her birini baseline ile karşılaştırıyoruz. Böylece bir iyileşme
olursa nedenini biliyoruz.

Kurallar:
- **Tek değişken:** Ortak ayarlar baseline ile aynı (batch 16, patience 10, save_period 5, seed 42, cache kapalı,
  workers 4, Ultralytics varsayılan augmentation, 50 epoch). Her deneyde yalnızca bir şey değişir.
- **Seçim val ile yapılır:** test setine bu adımda bakılmaz (Adım 9).
- **Resmî değer yerel ölçüm:** her model `src/eval/evaluate.py` ile yerelde, FP32 ölçülür. Kaggle'ın eğitim sonu
  değeri yalnızca not (kararlar.md, 2026-10-30).

---

## 2. Deneyler ve sırası
| Sıra | Ad | Neyi değiştiriyoruz | Hangi soruyu cevaplıyor |
|---|---|---|---|
| 1 | `baseline_v8s` ✅ | — (YOLOv8s, 640) | Karşılaştırma noktası; referansla aynı mimari |
| 2 | `e2_yolo11s` | Model: YOLO11s | Bir sonraki nesil, daha az parametreyle daha iyi mi? |
| 3 | `e3_yolo26s` | Model: YOLO26s | En yeni sürüm (küçük nesne için STAL, NMS'siz) bizim veride kazandırıyor mu? |
| 4 | `e4_yolo26n` | Model: YOLO26n | En küçük model; kamera için ne kadar hız kazanıp ne kadar doğruluk kaybediyoruz? |
| — | **Model seçimi** | 2–4 bitince | Sonraki deneyler seçilen s modeliyle yapılır |
| 5 | `e5_<model>_1024` | imgsz 640 → 1024 | Norveç'teki küçük çatlaklar daha büyük görüntüyle bulunuyor mu? |
| 6 | `e6_<model>_clspw` | Sınıf ağırlığı (`cls_pw 0.5`) | Az örnekli D40'a daha çok önem vermek çukur sonucunu iyileştiriyor mu? |
| 7 | `e7_<model>_d40x2` | D40'lı görüntüleri 2 kez göstermek (oversampling) | Aynı soru, farklı yöntemle: veri tekrarı mı, ağırlık mı daha iyi? |
| (8) | birleşik | 1024 + 6/7'nin iyi olanı | Yalnızca ikisi de val'de ayrı ayrı kazandırırsa: final model adayı |
| (zaman kalırsa) | mosaic kapalı | `mosaic=0` (referans gibi) | Referansın augmentation tercihi bizim veride fark yaratıyor mu? |

`<model>` seçilen modelin kısa adı (ör. `yolo11s`).

**Model seçimi kuralı:** 2–4 ve baseline içinden val mAP50'si (yerel FP32) en yüksek **s** modeli seçilir. Fark
1 puandan azsa GTX 1650'de FPS'i yüksek olan seçilir. YOLO26n ayrıca kamera modeli adayı olarak değerlendirilir.

### Her deneyin amacı (biraz daha ayrıntılı)
- **YOLO11s / YOLO26s:** COCO'da YOLOv8s'ten 2–4 puan iyiler, ama yol hasarı literatüründe fark ~1 puan
  (docs/arastirma/yolo-modelleri.md). Kendi verimizde ölçmek raporda başlı başına bir bulgu.
- **YOLO26n:** Baseline GTX 1650'de zaten 53 FPS (hedef 15). n modeli, "s yerine n kullansak doğruluktan ne kaybederiz"
  sorusunu cevaplar ve hızın sınırda kaldığı bilgisayarlar için yedek olur.
- **imgsz 1024:** Norveç görüntüleri 1280 px'e küçültülmüş durumda; 640'ta eğitince kutuların ~%23'ü 8 pikselin
  altına iniyor, 1024'te ~%10 (Adım 2 analizi). Beklenti: Norveç ve ince çatlaklarda artış, hızda düşüş. FPS de 1024'te ölçülür.
- **cls_pw 0.5 (sınıf ağırlığı):** Kayıp (loss) hesabında her sınıfa, ne kadar az örneği varsa o kadar büyük ağırlık
  verilir. `cls_pw=1` tam ters frekans (D00:D40 ≈ 4:1 olduğu için D40 4 kat ağır), `0.5` bunun karekökü (~2 kat).
  Yumuşak değer seçtik: tam ters frekans çok örnekli D00'ı fazla cezalandırabilir.
- **D40 oversampling (×2):** Görüntüler kopyalanmaz; train listesinde D40 içeren görüntüler 2 kez yazılır, model her
  epoch'ta onları 2 kez görür. Train'de D40 içeren **2.991** görüntü var (21.211'in %14'ü) → liste **24.202** satır
  (yerelde `data/yolo` üzerinde notebook'un aynı koduyla sayıldı). Val ve test değişmez. Dikkat: aynı görüntülerdeki
  diğer sınıflar da 2 kez görülür.

---

## 3. Notebook: `notebooks/train_experiment.ipynb`
Tüm deneyler aynı notebook'la yapılır; `train_baseline.ipynb` olduğu gibi kalır. Değişen yalnızca **Bölüm 4'teki
ayar hücresi**.

### 3.1 Ayar hücresine ne yazılır
| Deney | `MODEL` | `IMGSZ` | `NAME` | `EXTRA` | `OVERSAMPLE_D40` |
|---|---|---|---|---|---|
| 2 | `"yolo11s.pt"` | 640 | `"e2_yolo11s"` | `{}` | 1 |
| 3 | `"yolo26s.pt"` | 640 | `"e3_yolo26s"` | `{}` | 1 |
| 4 | `"yolo26n.pt"` | 640 | `"e4_yolo26n"` | `{}` | 1 |
| 5 | seçilen | 1024 | `"e5_<model>_1024"` | `{}` | 1 |
| 6 | seçilen | 640 | `"e6_<model>_clspw"` | `{"cls_pw": 0.5}` | 1 |
| 7 | seçilen | 640 | `"e7_<model>_d40x2"` | `{}` | 2 |
| mosaic | seçilen | 640 | `"e9_<model>_nomosaic"` | `{"mosaic": 0.0}` | 1 |

`EPOCHS = 50` ve ortak ayarlar (`COMMON`) değiştirilmez.

### 3.2 `MODE` ve `MAX_HOURS`
| `MODE` | Ne zaman | Ne yapar |
|---|---|---|
| `"deneme"` | Yeni bir model veya imgsz ilk kez kullanılacaksa (özellikle 1024: bellek kontrolü) | Train'in %10'u, 2 epoch. 1. epoch sonunda süre sınırı bilerek tetiklenir, aynı hücre hemen `last.pt`'den devam ettirir. Model indirme, batch ve dur+devam tek koşuda test edilir |
| `"egitim"` | Asıl eğitim | 50 epoch (erken durma açık). **Save Version → Save & Run All (Commit)** |
| `"devam"` | Eğitim süre sınırıyla durduysa | Önceki versiyonun output'u "Add Input" ile eklenir, `PREV_OUTPUT` = o output'taki `runs/<NAME>` yolu; kaldığı epoch'tan devam |

**`MAX_HOURS` (süre sınırı):** Kaggle oturumu en fazla 12 saat sürüyor ve süre dolunca zorla kesiyor. Notebook her
epoch sonunda (Ultralytics `last.pt`'yi kaydettikten sonra) "bir epoch daha sığar mı" diye bakar. Sığmayacaksa eğitimi
düzgünce durdurur, log'a `SÜRE SINIRI` yazar. Versiyon başarılı biter, `runs/<NAME>` output'ta kalır; sonraki
oturumda `MODE="devam"` ile sürdürülür. Varsayılan 11; uzun bir eğitimi bilerek iki oturuma bölmek için daha küçük
bir değer verilir (ör. 1024 deneyi).

**Neden `last.pt` devam ettirilebilir kalıyor?** Ultralytics eğitim normal bittiğinde `last.pt`'den optimizer'ı siler
ve onu "bitmiş" işaretler, artık devam edilemez. Bizim durdurmamız bu son adımdan önce olduğu için `last.pt` optimizer'ıyla
kalıyor. (Kaynak koddan doğrulandı: `ultralytics/engine/trainer.py`, kayıt → `on_fit_epoch_end` sırası.)

**Batch uyarısı:** Ultralytics 8.4.182, ilk epoch'ta GPU belleği yetmezse batch'i kendiliğinden yarıya indiriyor.
Notebook eğitim sonunda gerçek batch'i kontrol eder; 16 değilse `UYARI` yazar. Bu durumda deneyler.md'ye not düşülür
(tek değişken kuralı bozulmuş olur).

### 3.3 Kaggle'da adımlar (her deney)
1. Kaggle'da notebook'u aç (ilk seferde `train_experiment.ipynb`'yi yükle), sağ panel: GPU T4, Internet açık, input `rdd2022_yolo`.
2. Ayar hücresini tablodaki gibi doldur.
3. Yeni model/imgsz ise önce `MODE="deneme"` ile interaktif çalıştır; log'da `SÜRE SINIRI` → `Resuming training` →
   `DENEME BAŞARILI` görülmeli. Sonra oturumu kapat.
4. `MODE="egitim"` → **Save Version → Save & Run All (Commit)**, versiyon adı = `NAME`.
5. Bitince versiyonun **Output** sekmesinden `<NAME>_indir.zip`'i indir. Log'da `SÜRE SINIRI` varsa 3.2'deki `"devam"` adımı.

---

## 4. Çıktılar nereye kaydedilir
| Yer | İçerik | Git |
|---|---|---|
| Kaggle versiyon Output: `runs/<NAME>/` | Tüm koşu: `last.pt`, `epoch*.pt`, `best.pt`, grafikler (devam için gerekli) | — |
| Kaggle versiyon Output: `<NAME>_indir.zip` | `weights/best.pt`, `args.yaml`, `results.csv`, png/jpg grafikler | — |
| `runs/kaggle/<NAME>/` (yerel) | Zip'in açılmış hali | ❌ dışı |
| `runs/eval/<NAME>/` (yerel) | evaluate.py / measure_fps.py ham çıktıları | ❌ dışı |
| `docs/degerlendirme/<NAME>_val/` | `summary.md`, sınıf/alt küme CSV'leri, `fps.csv`, confusion matrix, PR eğrisi | ✅ girer |
| `docs/deneyler.md` | Ayarlar + Sonuçlar tablolarında birer satır | ✅ girer |
| GitHub Releases | Yalnızca seçilen final modelin `best.pt`'si (kararlar.md, 2026-10-18) | — |

## 5. Her deney bitince yerelde
Komutlar proje klasöründen (`C:\dev\yol-hasari`), PowerShell'de:

1. **Zip'i aç:**
   ```powershell
   Expand-Archive -Path $HOME\Downloads\e2_yolo11s_indir.zip -DestinationPath runs\kaggle\e2_yolo11s
   ```
   Kontrol: `runs\kaggle\e2_yolo11s\weights\best.pt` var.
2. **Doğruluk (val, FP32):**
   ```powershell
   .\venv\Scripts\python.exe src\eval\evaluate.py --weights runs/kaggle/e2_yolo11s/weights/best.pt --name e2_yolo11s
   ```
   1024 deneyinde sona `--imgsz 1024` eklenir. Script "Tümü" sonucunu Ultralytics'in sonucuyla karşılaştırır; tutmazsa durur.
3. **Hız (GTX 1650 + CPU, FP32, batch 1):**
   ```powershell
   .\venv\Scripts\python.exe src\eval\measure_fps.py --weights runs/kaggle/e2_yolo11s/weights/best.pt --name e2_yolo11s
   ```
   1024 deneyinde `--imgsz 1024`.
4. **`docs/deneyler.md`'ye ekle:**
   - *Ayarlar* tablosu: #, tarih, ad, model, imgsz, epoch (`durduğu / 50`, `results.csv`'nin satır sayısı), batch (uyarı
     varsa gerçek değer), augmentation/değişiklik (ör. `cls_pw 0.5`), **ortam ve gerçek süre** (Kaggle log'undaki
     `epochs completed in X hours`; devamlı eğitimde oturumların toplamı), Kaggle eğitim sonu mAP50, ağırlık yolu.
   - *Sonuçlar* tablosu: `docs/degerlendirme/<NAME>_val/summary.md`'den P, R, F1, mAP50, mAP50-95, sınıf AP50'leri,
     Norveç, China_Drone, Drone hariç, Japonya+Hindistan; `fps.csv`'den GPU ve CPU FPS.
5. Baseline ile karşılaştır: hangi sınıf/ülke iyileşti, hangisi kötüleşti → bu belgenin §6'sına kısa yorum.

---

## 6. Sonuçlar
*(Deneyler bitince doldurulacak. Sayıların kaynağı `docs/deneyler.md`.)*

| Ad | mAP50 | Fark (baseline'a göre) | D40 | Norveç | Japonya+Hindistan | FPS GTX 1650 | Yorum |
|---|---|---|---|---|---|---|---|
| baseline_v8s | 0,571 | — | 0,464 | 0,295 | 0,522 | 53,2 | Karşılaştırma noktası |
| e2_yolo11s | 0,582 | +1,1 | 0,477 | 0,265 | 0,522 | 53,4 | Genelde biraz iyi, Norveç'te kötü (§6.1) |
| e3_yolo26s | 0,589 | +1,8 | 0,500 | 0,280 | 0,537 | 50,5 | En yüksek mAP50 ve D40; e2'den farkı 1 puanın altında (§6.2) |
| e4_yolo26n | 0,560 | −1,1 | 0,458 | 0,239 | 0,509 | 61,2 | s'den ~3 puan düşük, CPU'da 23 FPS (§6.3) |
| e5 (1024) | | | | | | | |
| e6 (cls_pw) | | | | | | | |
| e7 (D40 ×2) | | | | | | | |

**Seçilen model:** **YOLO26s (e3)** (2026-11-02; gerekçe §6.4 ve [model-secimi.md](../model-secimi.md)).
YOLO26n yedek kamera modeli.

### 6.1 e2 YOLO11s sonuçları (val seti, yerel ölçüm, FP32)
Eğitim ayarları baseline ile birebir aynı (`args.yaml` kontrol edildi); tek fark model: YOLOv8s yerine YOLO11s.
50 epoch'un hepsi tamamlandı, erken durma devreye girmedi; son epoch'larda val mAP50 yatay (0,595–0,597).
Ölçüm baseline ile aynı yoldan: `evaluate.py` (val, imgsz 640, batch 16) ve `measure_fps.py`.
Ayrıntılı tablolar: [e2_yolo11s_val/summary.md](../degerlendirme/e2_yolo11s_val/summary.md).

**Genel**
| Model | P | R | F1 | **mAP50** | mAP50-95 |
|---|---|---|---|---|---|
| baseline (YOLOv8s) | 0,621 | 0,541 | 0,578 | 0,571 | 0,286 |
| e2 (YOLO11s) | 0,638 | 0,542 | 0,586 | **0,582** | 0,294 |
| Fark | +1,7 | +0,1 | +0,8 | **+1,1** | +0,8 |

*Yorum:* YOLO11s genel mAP50'de baseline'dan 1,1 puan önde. Artış neredeyse tamamen **precision**'dan geliyor
(+1,7); recall değişmedi (0,541 → 0,542). Yani YOLO11s gerçek hasarlardan **daha fazlasını bulmuyor**, ama "hasar"
dediği yerlerde daha az yanılıyor (daha az yanlış alarm). mAP50-95'teki artış (+0,8) kutuların biraz daha iyi
oturduğunu gösteriyor.

**Sınıf bazında (AP50)**
| Sınıf | baseline | e2 | Fark |
|---|---|---|---|
| D00 boyuna çatlak | 0,569 | 0,572 | +0,3 |
| D10 enine çatlak | 0,574 | 0,591 | +1,7 |
| D20 timsah çatlağı | 0,679 | 0,690 | +1,1 |
| D40 çukur | 0,464 | 0,477 | +1,3 |

*Yorum:* Dört sınıfın hepsi az da olsa iyileşti; en çok enine çatlak (+1,7). Sıralama değişmedi: en iyi yine D20,
en zayıf yine **D40 (0,477)**. Mimari değişikliği çukur sorununu çözmüyor; D40 deneyleri (6 ve 7) hâlâ gerekli.
D40'ın recall'u 0,425: çukurların yarıdan fazlası hâlâ kaçıyor.

**Ülke bazında (mAP50)**
| Ülke | Kutu | baseline | e2 | Fark |
|---|---|---|---|---|
| China_MotorBike | 439 | 0,882 | 0,906 | +2,4 |
| ABD | 1.083 | 0,607 | 0,640 | +3,3 |
| China_Drone | 308 | 0,593 | 0,666 | **+7,3** |
| Japonya | 1.582 | 0,558 | 0,565 | +0,7 |
| Çek Cumhuriyeti | 157 | 0,445 | 0,472 | +2,7 |
| Hindistan | 698 | 0,405 | 0,413 | +0,8 |
| Norveç | 960 | 0,295 | 0,265 | **−3,0** |

*Yorum:*
- **Norveç'te tek düşüş (−3,0).** Recall 0,304'ten 0,266'ya indi; düşüş en çok çukurda (0,127 → 0,076) ve timsah
  çatlağında (0,348 → 0,256). Norveç'in sorunu küçük nesneler (640'ta kutuların ~%23'ü 8 pikselin altında). Daha
  yeni bir mimari bu sorunu çözmedi, hatta biraz kötüleşti. Bu, sorunun modelde değil **görüntü çözünürlüğünde**
  olduğunu destekliyor: imgsz 1024 deneyi (5) bu yüzden önemli.
- **China_Drone'da büyük artış (+7,3).** Dikkat: yalnızca 308 kutu var; küçük alt kümelerde birkaç doğru/yanlış
  tahmin sonucu birkaç puan oynatabilir. Yönü olumlu, büyüklüğüne fazla güvenilmemeli. Aynı uyarı Çek (157 kutu) için de geçerli.
- **ABD (+3,3)** büyük bir alt küme (1.083 kutu) olduğu için bu artış daha güvenilir.

**Özel alt kümeler**
| Alt küme | baseline | e2 | Fark |
|---|---|---|---|
| Drone hariç | 0,568 | 0,577 | +0,9 |
| Japonya+Hindistan | 0,522 | 0,522 | 0,0 |

*Yorum:* Japonya+Hindistan'da hiç değişiklik yok; referansın 0,547'sinin hâlâ 2,5 puan altında (val'de ön
karşılaştırma). Japonya'daki küçük artış (+0,7) ile Hindistan'daki (+0,8) birleşik alt kümede birbirini dengeleyen sınıf
farklarıyla sıfırlanıyor (ör. D00 0,465 → 0,446). Yani YOLO11s'in kazancı daha çok ABD ve Çin görüntülerinden geliyor.

**Hız (FPS, FP32, batch 1)**
| Cihaz | baseline | e2 | Fark |
|---|---|---|---|
| GTX 1650 | 53,2 | 53,4 | ≈ aynı |
| CPU | 9,5 | 10,6 | +%11 |

*Yorum:* YOLO11s kâğıt üzerinde daha hafif (9,4 M parametre / 21,6 GFLOPs; YOLOv8s 11,2 M / 28,6). CPU'da bu %11
hız olarak görünüyor. GTX 1650'de fark yok. Olası neden: tek görüntülük (batch 1) çıkarımda GPU tam dolmuyor ve
süreyi işlem sayısından çok katman sayısı ve bellek erişimi belirliyor; YOLO11'in ek dikkat (attention) bloğu da
FLOPs kazancını dengeliyor olabilir (ayrıca ölçmedik).
Her iki model de 15 FPS hedefinin 3,5 katında.

**Baseline'la fark ve olası nedeni**
YOLO11s, YOLOv8s'e göre iki mimari değişiklik getiriyor: daha verimli **C3k2** blokları (daha az parametreyle benzer
kapasite) ve **C2PSA** adlı bir dikkat bloğu (görüntünün önemli bölgelerine odaklanmayı sağlar). Bizim ölçümde bunun
etkisi "daha az yanlış alarm" olarak görünüyor (precision +1,7), "daha çok hasar bulma" olarak değil (recall aynı).
Literatürdeki beklentiyle uyumlu: yol hasarında yeni sürümlerin kazancı ~1 puan ([yolo-modelleri.md](../arastirma/yolo-modelleri.md)).

**Bu fark anlamlı mı?** +1,1 puan, model seçim kuralındaki 1 puan sınırının hemen üstünde. Ancak her model **tek bir
seed** ile eğitildi; aynı modeli farklı seed'le eğitince de sonuç ~1 puan oynayabilir (bunu ölçmedik, kota yok).
Bu yüzden "YOLO11s kesin daha iyi" demek yerine "YOLO11s biraz önde, fark küçük" demek doğru. Seçim, YOLO26s (e3)
ölçülünce yapılacak.

**Sayıların anlamı (kısaca)**
- mAP50 0,582: model, hasarı bulup kutuyu en az %50 örtüşecek şekilde çizdiğinde "doğru" sayılıyor; tüm güven
  eşiklerindeki ortalama kesinliğin 4 sınıf ortalaması 0,58.
- P 0,64: modelin "hasar" dediklerinin yaklaşık üçte ikisi gerçekten hasar. R 0,54: gerçek hasarların yarıdan biraz
  fazlası bulunuyor.
- "+1,1 puan": 0,571'den 0,582'ye, yani 0,011'lik mutlak artış (yaklaşık %2 göreli).

**Hocaya nasıl anlatırım (e2)**
"Baseline ile aynı veri, aynı ayarlar ve aynı seed ile yalnızca modeli değiştirdik: YOLOv8s yerine bir sonraki nesil
YOLO11s. Genel mAP50 0,571'den 0,582'ye çıktı. Artış precision'dan geliyor, yani model daha az yanlış alarm veriyor ama
daha fazla hasar bulmuyor. Dört sınıfın hepsi az da olsa iyileşti, ama çukur hâlâ en zayıf sınıf. Tek kötüleşme
Norveç'te: orada sorun küçük nesneler, model değiştirmek bunu çözmüyor; bunu görüntü boyutunu büyüterek deneyeceğiz.
Hız GTX 1650'de aynı, saniyede 53 kare. Fark küçük ve tek seed'le ölçüldü; bu yüzden YOLO26s'i de ölçüp öyle seçeceğiz."

### 6.2 e3 YOLO26s sonuçları (val seti, yerel ölçüm, FP32)
Eğitim ayarları baseline ve e2 ile birebir aynı (`args.yaml` kontrol edildi); tek fark model: YOLO26s.
50 epoch'un hepsi tamamlandı; en iyi val mAP50 epoch 43'te, son epoch'larda yatay (0,598–0,599).
Ölçüm aynı yoldan: `evaluate.py` (val, imgsz 640, batch 16) ve `measure_fps.py`.
Ayrıntılı tablolar: [e3_yolo26s_val/summary.md](../degerlendirme/e3_yolo26s_val/summary.md).
Farklar puan cinsinden (0,01 = 1 puan), tablolardaki yuvarlanmış değerlerden hesaplandı.

**Genel**
| Model | P | R | F1 | **mAP50** | mAP50-95 |
|---|---|---|---|---|---|
| baseline (YOLOv8s) | 0,621 | 0,541 | 0,578 | 0,571 | 0,286 |
| e2 (YOLO11s) | 0,638 | 0,542 | 0,586 | 0,582 | 0,294 |
| e3 (YOLO26s) | 0,641 | 0,547 | 0,591 | **0,589** | 0,294 |
| e3 − baseline | +2,0 | +0,6 | +1,3 | **+1,8** | +0,8 |
| e3 − e2 | +0,3 | +0,5 | +0,5 | **+0,7** | 0,0 |

*Yorum:* YOLO26s üç model içinde en yüksek mAP50'ye sahip: baseline'dan 1,8 puan, e2'den 0,7 puan önde. e2'deki gibi
artışın çoğu precision'dan (daha az yanlış alarm) geliyor; e3'te recall da biraz artmış (+0,6). Kutuların ne kadar iyi
oturduğunu gösteren mAP50-95 e2 ile aynı (0,294).

**Sınıf bazında (AP50)**
| Sınıf | baseline | e2 | e3 | e3 − baseline | e3 − e2 |
|---|---|---|---|---|---|
| D00 boyuna çatlak | 0,569 | 0,572 | 0,578 | +0,9 | +0,6 |
| D10 enine çatlak | 0,574 | 0,591 | 0,588 | +1,4 | −0,3 |
| D20 timsah çatlağı | 0,679 | 0,690 | 0,691 | +1,2 | +0,1 |
| D40 çukur | 0,464 | 0,477 | **0,500** | **+3,6** | **+2,3** |

*Yorum:* e3'ün e2'ye üstünlüğü neredeyse tamamen **çukurdan (D40)** geliyor: 0,477 → 0,500. Diğer üç sınıfta e2 ile
e3 arasındaki fark 1 puanın altında. D40 hâlâ en zayıf sınıf ve recall'u 0,430: çukurların yarıdan fazlası hâlâ
kaçıyor. D40 deneyleri (6 ve 7) gerekli olmaya devam ediyor.

**Ülke bazında (mAP50)**
| Ülke | Kutu | baseline | e2 | e3 | e3 − baseline | e3 − e2 |
|---|---|---|---|---|---|---|
| China_MotorBike | 439 | 0,882 | 0,906 | 0,924 | +4,2 | +1,8 |
| ABD | 1.083 | 0,607 | 0,640 | 0,616 | +0,9 | −2,4 |
| China_Drone | 308 | 0,593 | 0,666 | 0,666 | +7,3 | 0,0 |
| Japonya | 1.582 | 0,558 | 0,565 | 0,574 | +1,6 | +0,9 |
| Çek Cumhuriyeti | 157 | 0,445 | 0,472 | 0,426 | −1,9 | −4,6 |
| Hindistan | 698 | 0,405 | 0,413 | 0,433 | +2,8 | +2,0 |
| Norveç | 960 | 0,295 | 0,265 | 0,280 | −1,5 | +1,5 |

*Yorum:*
- **Japonya ve Hindistan'da e3 en iyisi.** Hindistan'da artış belirgin (+2,8 / +2,0).
- **ABD'de e3, e2'nin gerisinde (−2,4).** ABD'de e3'ün P'si 0,548'e düşüp R'si 0,628'e çıkıyor (e2: 0,692 / 0,597).
  P ve R tek bir güven eşiğinde ölçülüyor ve bu eşik modelden modele değişiyor; mAP ise eşikten bağımsız. Bu yüzden
  karşılaştırmada mAP'ye bakmak gerekiyor; o da 2,4 puan geride.
- **Norveç hâlâ baseline'ın altında (−1,5).** YOLO26'nın küçük nesneler için getirdiği yenilik (STAL, aşağıda) Norveç'te
  baseline'ı geçmeye yetmedi. Bu, e2'deki gibi, sorunun mimaride değil **görüntü çözünürlüğünde** olduğunu destekliyor
  (imgsz 1024 deneyi, 5).
- **Çek (157 kutu) ve China_Drone (308 kutu) küçük alt kümeler.** Çek'teki −4,6 ve Drone'daki +7,3 birkaç tahminle
  oynayabilecek büyüklükte; yön göstergesi olarak okunmalı, kesin sonuç olarak değil.

**Özel alt kümeler**
| Alt küme | baseline | e2 | e3 | e3 − baseline | e3 − e2 |
|---|---|---|---|---|---|
| Drone hariç | 0,568 | 0,577 | 0,584 | +1,6 | +0,7 |
| Japonya+Hindistan | 0,522 | 0,522 | **0,537** | **+1,5** | **+1,5** |

*Yorum:* Japonya+Hindistan'da ilk kez anlamlı bir artış var: 0,522 → 0,537. Referansın 0,547'sine fark 2,5 puandan
**1,0 puana** indi (val'de ön karşılaştırma; kesin karşılaştırma Adım 9'da test setinde). Drone hariç sonuç genel
sonuçla aynı yönde: Drone görüntüleri sonucu şişirmiyor.

**Hız (FPS, FP32, batch 1)**
| Cihaz | baseline | e2 | e3 |
|---|---|---|---|
| GTX 1650 FPS | 53,2 | 53,4 | **50,5** |
| GTX 1650 çıkarım ms | 15,3 | 15,5 | 16,3 |
| GTX 1650 son işleme ms | 1,4 | 1,3 | 1,4 |
| CPU FPS | 9,5 | 10,6 | 9,9 |

*Yorum:* e3 GTX 1650'de üç modelin en yavaşı: e2'den ~%5 yavaş (50,5 / 53,4 FPS). Fark sinir ağı hesabından
(çıkarım 16,3 ms) geliyor. Son işleme süresi değişmedi (1,4 ms), çünkü ölçümümüzde NMS hâlâ çalışıyor (aşağıya bakın).
15 FPS hedefinin yine 3 katından fazla; kamera için sorun değil.

**YOLO26'nın mimari farkları (kısaca) ve bizim ölçümde ne gördük**
| Yenilik | Ne demek | Bizim deneyde |
|---|---|---|
| **NMS'siz uçtan uca başlık** | Normalde model aynı nesneye birçok kutu önerir, NMS (non-maximum suppression) adlı son adım üst üste binenleri ayıklar. YOLO26'nın ek bir "bire-bir" başlığı her nesne için tek kutu üretmeyi öğrenir, NMS'e gerek kalmaz | Ultralytics 8.4.182'de bu mod **isteğe bağlı** (`nms=False`), varsayılan değil. Hem Kaggle'daki eğitim içi doğrulama hem bizim ölçümümüz varsayılanla, yani **NMS'li** yapıldı. e3'ün sonuçları YOLO26'nın "bire-çok" başlığı + NMS ile alındı. Son işleme süresinin aynı kalması bunu doğruluyor |
| **DFL'nin kaldırılması** | YOLOv8/11 kutu kenarının yerini bir olasılık dağılımı olarak tahmin eder (DFL, 16 aralık). YOLO26 kenar uzaklığını doğrudan tahmin eder; model sadeleşir, başka formatlara aktarmak kolaylaşır | Checkpoint'te doğrulandı (`reg_max` 16 → 1). mAP50-95 (kutu oturması) e2 ile aynı: kayıp da kazanç da yok |
| **STAL** | Küçük nesnelere eğitim sırasında daha fazla "aday kutu" atayan etiket atama yöntemi | Norveç (küçük nesne) e2'den iyi ama baseline'dan kötü. Belirgin bir küçük nesne kazancı görmedik. YOLO26 makalesinde de kazanç küçük (AP_S 29,0 → 29,6) |
| **ProgLoss** | Eğitim boyunca kayıp bileşenlerinin ağırlığını kademeli değiştiren yöntem | Ayrıca ölçülemedi; sonuca toplam katkısı içinde |
| **MuSGD optimizer** | YOLO26 ile tanıtılan optimizer | **Bizim deneylerde fark değil:** `optimizer=auto` uzun eğitimlerde her modelde MuSGD seçiyor. Checkpoint'lerden doğrulandı: baseline, e2 ve e3'ün üçü de MuSGD ile eğitildi |

Kaynak: [yolo-modelleri.md](../arastirma/yolo-modelleri.md); başlık, `reg_max` ve optimizer bilgisi bizim `best.pt`
dosyalarından okundu.

**Bu fark anlamlı mı? (1 puan kuralı, kararlar.md 2026-10-31)**
- **e3 − baseline = +1,8 puan:** 1 puan sınırının açıkça üstünde. YOLO26s, YOLOv8s'ten daha iyi.
- **e3 − e2 = +0,7 puan:** 1 puan sınırının **altında**. Genel mAP50'de e2 ile e3'ü birbirinden ayıramıyoruz; kurala
  göre bu durumda GTX 1650 FPS'ine bakılacak. Bunun yanında e3, en zayıf sınıf olan D40'ta (+2,3) ve hedef alt küme
  Japonya+Hindistan'da (+1,5) 1 puanın üstünde önde.
- Her model **tek seed** ile eğitildi; seed değişince sonucun ne kadar oynadığını ölçmedik. Küçük farklar bu oynaklığın
  içinde kalabilir.
- **Model seçimi henüz yapılmadı:** e4 (YOLO26n) ölçülünce üç model birlikte değerlendirilecek.

**Sayıların anlamı (kısaca)**
- mAP50 0,589: tüm güven eşiklerindeki ortalama kesinliğin 4 sınıf ortalaması; kutu en az %50 örtüşürse doğru sayılıyor.
- D40 0,500: çukurda bu ortalama kesinlik yarı yarıya. Hâlâ en zayıf sınıf, ama baseline'dan 3,6 puan yukarıda.
- 50,5 FPS: GTX 1650 saniyede ~50 görüntü işliyor, yani bir görüntü ~20 ms.

**Hocaya nasıl anlatırım (e3)**
"Üçüncü deneyde yine yalnızca modeli değiştirdik: en yeni sürüm YOLO26s. Genel mAP50 0,589 ile üç modelin en iyisi:
baseline'dan 1,8 puan, YOLO11s'ten 0,7 puan yukarıda. YOLO11s ile farkı bizim 1 puanlık sınırımızın altında, yani
genel sonuçta ikisini ayıramıyoruz. Ama en zayıf sınıfımız çukurda 2,3 puan, referansla karşılaştırdığımız
Japonya+Hindistan'da 1,5 puan önde; referansa olan farkımız 2,5 puandan 1 puana indi. YOLO26'nın tanıtılan
yeniliklerinden NMS'siz çıkarım, kullandığımız sürümde varsayılan olarak kapalı. Bu yüzden ölçümümüz NMS'li ve hız
avantajı görünmüyor: GTX 1650'de 50 FPS, YOLO11s'ten biraz yavaş ama hedefin üç katı. Optimizer'ın bütün modellerde
aynı (MuSGD) olduğunu checkpoint'lerden doğruladık, yani fark optimizer'dan değil mimariden geliyor. Seçimi en küçük model YOLO26n
ölçülünce yapacağız."

### 6.3 e4 YOLO26n sonuçları (val seti, yerel ölçüm, FP32)
Eğitim ayarları diğer üç modelle birebir aynı (`args.yaml` kontrol edildi; optimizer yine MuSGD); tek fark model:
YOLO26'nın en küçük boyu **n** (nano). 50 epoch'un hepsi tamamlandı; en iyi val mAP50 epoch 45'te, son epoch'larda
yatay (0,576). Ölçüm aynı yoldan. Ayrıntılı tablolar: [e4_yolo26n_val/summary.md](../degerlendirme/e4_yolo26n_val/summary.md).

Bu deneyin sorusu farklı: "en iyi model hangisi" değil, **"aynı nesilde s yerine n kullanınca ne kadar doğruluk
kaybedip ne kadar hız kazanıyoruz?"** Bu yüzden asıl karşılaştırma e4 ↔ e3 (ikisi de YOLO26). n modeli s'nin ~¼'ü
büyüklüğünde: 2,4 M parametre / 5,5 GFLOPs (s: 9,5 M / 20,9).

**Genel**
| Model | P | R | F1 | **mAP50** | mAP50-95 |
|---|---|---|---|---|---|
| baseline (YOLOv8s) | 0,621 | 0,541 | 0,578 | 0,571 | 0,286 |
| e2 (YOLO11s) | 0,638 | 0,542 | 0,586 | 0,582 | 0,294 |
| e3 (YOLO26s) | 0,641 | 0,547 | 0,591 | 0,589 | 0,294 |
| e4 (YOLO26n) | 0,610 | 0,534 | 0,570 | **0,560** | 0,281 |
| e4 − e3 | −3,1 | −1,3 | −2,1 | **−2,9** | −1,3 |

*Yorum:* Modeli 4 kat küçültmek mAP50'de **2,9 puan** kaybettiriyor (0,589 → 0,560). Bu kayıp, s modelleri arasındaki
farklardan (en fazla 1,8 puan) daha büyük: model **boyu**, model **sürümünden** daha çok etkiliyor. e4 baseline'ın da
1,1 puan altında. Kayıp çoğunlukla precision'da (−3,1): küçük model daha çok yanlış alarm veriyor.

**Sınıf bazında (AP50)**
| Sınıf | baseline | e2 | e3 | e4 | e4 − e3 |
|---|---|---|---|---|---|
| D00 boyuna çatlak | 0,569 | 0,572 | 0,578 | 0,543 | −3,5 |
| D10 enine çatlak | 0,574 | 0,591 | 0,588 | 0,569 | −1,9 |
| D20 timsah çatlağı | 0,679 | 0,690 | 0,691 | 0,670 | −2,1 |
| D40 çukur | 0,464 | 0,477 | 0,500 | 0,458 | **−4,2** |

*Yorum:* En çok kaybeden sınıf **D40 (−4,2)**: e3'ün çukurdaki kazancı n boyunda tamamen kayboluyor, e4 çukurda
baseline'ın bile altında (0,458). Az örnekli ve çeşitli görünümlü (çukur, tümsek, tekerlek izi) bir sınıfı öğrenmek
daha fazla kapasite istiyor. D00'daki kayıp da büyük (−3,5): ince, uzun çatlaklar küçük modelde daha zor.

**Ülke bazında (mAP50)**
| Ülke | Kutu | baseline | e2 | e3 | e4 | e4 − e3 |
|---|---|---|---|---|---|---|
| China_MotorBike | 439 | 0,882 | 0,906 | 0,924 | 0,891 | −3,3 |
| ABD | 1.083 | 0,607 | 0,640 | 0,616 | 0,574 | −4,2 |
| China_Drone | 308 | 0,593 | 0,666 | 0,666 | 0,658 | −0,8 |
| Japonya | 1.582 | 0,558 | 0,565 | 0,574 | 0,551 | −2,3 |
| Çek Cumhuriyeti | 157 | 0,445 | 0,472 | 0,426 | 0,426 | 0,0 |
| Hindistan | 698 | 0,405 | 0,413 | 0,433 | 0,389 | −4,4 |
| Norveç | 960 | 0,295 | 0,265 | 0,280 | **0,239** | −4,1 |

*Yorum:* Neredeyse her ülkede kayıp var. En büyük kayıplar **Hindistan (−4,4), ABD (−4,2) ve Norveç (−4,1)**. Norveç
0,239 ile tüm modellerin en düşük değeri: küçük nesne sorunu küçük modelde daha da ağırlaşıyor. China_Drone (−0,8) ve
Çek (0,0) neredeyse aynı kaldı; ikisi de küçük alt küme olduğu için bu "kayıp yok" sonucu da dikkatli okunmalı.

**Özel alt kümeler**
| Alt küme | baseline | e2 | e3 | e4 | e4 − e3 |
|---|---|---|---|---|---|
| Drone hariç | 0,568 | 0,577 | 0,584 | 0,554 | −3,0 |
| Japonya+Hindistan | 0,522 | 0,522 | 0,537 | 0,509 | −2,8 |

*Yorum:* Japonya+Hindistan'da e4 0,509; referansın 0,547'sinin 3,8 puan altında. n modeli, referansla karşılaştırma
hedefi için uygun değil.

**Hız (FPS, FP32, batch 1)**
| Cihaz | baseline | e2 | e3 | e4 | e4 / e3 |
|---|---|---|---|---|---|
| GTX 1650 FPS | 53,2 | 53,4 | 50,5 | **61,2** | ×1,2 |
| GTX 1650 çıkarım ms | 15,3 | 15,5 | 16,3 | 13,1 | |
| CPU FPS | 9,5 | 10,6 | 9,9 | **23,4** | ×2,4 |
| CPU çıkarım ms | 100,0 | 90,5 | 97,2 | 39,0 | |

*Yorum:*
- **GPU'da kazanç küçük (×1,2).** İşlem sayısı ¼'e indiği halde süre yalnızca %20 kısalıyor. Tek görüntülük (batch 1)
  çıkarımda GTX 1650 tam dolmuyor; süreyi işlem sayısından çok katman sayısı ve ön/son işleme belirliyor (§6.1'deki
  gözlemle aynı). GTX 1650'de s modelleri zaten hedefin 3 katı hızlı olduğu için n'ye geçmenin burada pratik bir faydası yok.
- **CPU'da kazanç büyük (×2,4) ve önemli:** CPU'da süre işlem sayısıyla orantılı. e4 CPU'da **23,4 FPS** ile 15 FPS
  hedefini geçen **tek model**; s modelleri CPU'da 10 FPS civarında kalıyor. Yani GPU'su olmayan bir bilgisayarda
  (ör. sunum bilgisayarı) gerçek zamanlı kamera yalnızca n modeliyle mümkün.

**Doğruluk / hız dengesi (özet):** e3 → e4: mAP50 −2,9 puan, D40 −4,2 puan; karşılığında GPU'da +%21, CPU'da +%136 hız.
GPU'lu bilgisayarda bu takas değmez; GPU'suz bilgisayarda kamerayı mümkün kılan tek seçenek.

**Hocaya nasıl anlatırım (e4)**
"Dördüncü deneyde aynı nesil YOLO26'nın en küçük boyunu eğittik: s modelinin yaklaşık dörtte biri büyüklüğünde. Doğruluk
2,9 puan düştü (0,589'dan 0,560'a); en çok kaybeden çukur sınıfı ve küçük nesnelerin olduğu Norveç oldu. Bu kayıp,
farklı sürümler arasındaki farklardan büyük: modelin boyu, sürümünden daha önemli çıktı. Hızda ilginç bir sonuç gördük:
GPU'da sadece %20 hızlandı, çünkü tek görüntüde GPU zaten tam dolmuyor; ama CPU'da 2,4 kat hızlandı ve saniyede 23
görüntüyle GPU'suz da gerçek zamanlı hedefimizi geçen tek model oldu. Bu yüzden onu GPU'suz bilgisayarlar için yedek
kamera modeli olarak tutuyoruz."

### 6.4 Model seçimi
> **Karar (2026-11-02): YOLO26s (e3)**, seçim kuralından bilinçli sapmayla. YOLO26n yedek kamera modeli.
> Tek başına okunabilen anlatım: **[model-secimi.md](../model-secimi.md)** · Karar kaydı: [kararlar.md](../kararlar.md) (2026-11-02)

Sonraki deneylerde (1024, D40) kullanılacak s modeli seçildi. Aşağıdaki tablo, seçimi etkileyen ölçütleri bir araya
getiriyor (val, yerel FP32; süre `deneyler.md`'deki Kaggle runtime'ı).

| Ölçüt | baseline (YOLOv8s) | e2 (YOLO11s) | e3 (YOLO26s) | e4 (YOLO26n) |
|---|---|---|---|---|
| mAP50 | 0,571 | 0,582 | **0,589** | 0,560 |
| e3'e fark (1 puan kuralı) | −1,8 (ayrılıyor) | −0,7 (ayrılamıyor) | — | −2,9 (ayrılıyor) |
| D40 AP50 | 0,464 | 0,477 | **0,500** | 0,458 |
| Japonya+Hindistan (0,547'ye fark) | 0,522 (−2,5) | 0,522 (−2,5) | **0,537 (−1,0)** | 0,509 (−3,8) |
| Norveç | **0,295** | 0,265 | 0,280 | 0,239 |
| FPS GTX 1650 (hedef 15) | 53,2 ✅ | **53,4** ✅ | 50,5 ✅ | 61,2 ✅ |
| FPS CPU (hedef 15) | 9,5 ❌ | 10,6 ❌ | 9,9 ❌ | **23,4** ✅ |
| Kaggle süresi (640, 50 epoch) | 4 sa 55 dk | 7 sa 11 dk | 8 sa 22 dk | 5 sa 21 dk |

**1. Kuralın harfiyen sonucu (kararlar.md, 2026-10-31):** s modelleri içinde mAP50'si en yüksek olan e3 (0,589).
e2 ile farkı 0,7 puan, yani 1 puanın altında → kurala göre GTX 1650 FPS'i yüksek olan seçilir: **e2 (YOLO11s)**,
53,4 FPS'e karşı 50,5.

**2. Seçilen: e3 (YOLO26s). ⚠️ Kuraldan bilinçli sapma (2026-11-02'de onaylandı).**
Gerekçe:
- **Kuralın FPS'e bakmasının amacı kamera hedefiydi.** İki model de GTX 1650'de hedefin (15 FPS) üç katından hızlı;
  aradaki 2,9 FPS'lik fark kamerada hissedilmez. Bu durumda FPS'e göre seçmek pratik bir şey kazandırmıyor.
- **Sonraki deneylerin hedeflediği yerlerin üçünde de e3 önde:** D40'ta +2,3 puan (D40 deneyleri bu sınıf için),
  Japonya+Hindistan'da +1,5 puan (referansa fark 1,0 puana iniyor; ara rapordaki ana karşılaştırma), Norveç'te +1,5
  puan (1024 deneyi bu ülke için). İlk ikisi 1 puan sınırının üstünde.
- e3 genel mAP50'de de üç s modelinin en iyisi (fark küçük olsa da yönü aynı).

**Seçimin zayıf yanları (dürüst değerlendirme):**
- **Eğitim süresi:** e3, e2'den yaklaşık %16 daha uzun sürdü (8 sa 22 dk / 7 sa 11 dk). 1024 deneyi bu farkı büyütür
  ve Kaggle kotasını daha çok zorlar. Seçimdeki en somut maliyet bu.
- **D40 ve Japonya+Hindistan alt kümeleri genelden küçük** (586 ve 2.280 kutu); farklar tek seed'le ölçüldü, bir
  kısmı oynaklık olabilir.
- Ülkelerde tablo karışık: e3, e2'den Japonya, Hindistan, Norveç ve China_MotorBike'ta önde; ABD (−2,4) ve Çek'te geride.

**Kurala uyulursa (e2 seçilirse):** genel doğrulukta pratik bir kayıp yok (0,7 puan), eğitimler daha kısa sürer;
ama D40 ve Japonya+Hindistan'da 1 puandan fazla geriden başlanır.

**3. YOLO26n'in (e4) rolü:** Ana model adayı değil (s modellerinden ~3 puan düşük, D40 ve Norveç'te en zayıf).
**GPU'suz bilgisayarlar için yedek kamera modeli** olarak tutulur (CPU'da 15 FPS hedefini geçen tek model). Üzerinde
1024 / D40 deneyi yapılmaz; Adım 8'de (kamera) seçenek olarak sunulur.

**4. Baseline (YOLOv8s):** Referansla aynı mimari olduğu için raporda karşılaştırma noktası olarak kalır; sonraki
deneylere geçmez.

**5. Sonraki deneylerin adları:** `e5_yolo26s_1024`, `e6_yolo26s_clspw`, `e7_yolo26s_d40x2`; ayar hücresinde
`MODEL = "yolo26s.pt"`. Her biri **e3'e karşı** karşılaştırılır.

---

## 7. Bu adımda ne öğreneceğim
- Kontrollü deney: tek değişken değiştirip gerisini sabit tutmak, sonucu bir nedene bağlayabilmek.
- Model boyutu (n/s) ile hız ve doğruluk arasındaki denge; parametre ve FLOPs'un FPS'e etkisi.
- Görüntü boyutunun (imgsz) küçük nesnelere etkisi ve bunun hıza maliyeti.
- Sınıf dengesizliğiyle başa çıkmanın iki yolu: kayıpta sınıf ağırlığı ve oversampling; farkları ve yan etkileri.
- Uzun eğitimi checkpoint ile oturumlara bölmek; Ultralytics callback'leriyle eğitime müdahale etmek.
- Model seçimini val ile yapmanın, test setini sona saklamanın anlamı.

## 8. Hocaya nasıl anlatırım
"Baseline'dan sonra her deneyde yalnızca bir şeyi değiştirdik; diğer bütün ayarlar (batch, epoch, seed, augmentation)
aynı kaldı. Önce üç modeli karşılaştırdık: referansla aynı YOLOv8s, bir sonraki nesil YOLO11s ve en yeni YOLO26s;
ayrıca kamera için en küçük YOLO26n. En iyisini val setine göre seçtik. Sonra baseline'da gördüğümüz iki zayıflığa
yöneldik: Norveç'teki küçük çatlaklar için görüntü boyutunu 640'tan 1024'e çıkardık; en az örneği olan çukur sınıfı
için iki dengeleme yöntemini, sınıf ağırlığını ve çukurlu görüntüleri iki kez göstermeyi denedik. Bütün modelleri aynı
script'le, aynı bilgisayarda ölçtük; sonuçlar bu tabloda. Test setine yalnızca en sonda, seçilen modelle bir kez bakacağız."
