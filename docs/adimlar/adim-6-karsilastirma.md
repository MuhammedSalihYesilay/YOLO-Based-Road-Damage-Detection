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
| e2_yolo11s | | | | | | | |
| e3_yolo26s | | | | | | | |
| e4_yolo26n | | | | | | | |
| e5 (1024) | | | | | | | |
| e6 (cls_pw) | | | | | | | |
| e7 (D40 ×2) | | | | | | | |

**Seçilen model:** *(model seçiminden sonra)*

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
