# Adım 7a: Streamlit görüntü prototipi (vize, 2026-11-14)

## 1. Bu adımda ne yaptık, neden
Proje önerisindeki web arayüzünün ilk parçasını yaptık: kullanıcı bir yol fotoğrafı yükler (veya hazır bir örnek
seçer), final model **e5 (YOLO26s, imgsz 1024)** hasarları bulur, her hasar **kutu + sınıf + güven skoru** ile
gösterilir. Güven eşiği ve gösterilecek sınıflar kenar çubuğundan değiştirilebilir. Arayüz Türkçe ve İngilizce.

Vize kapsamı yalnız görüntü (kararlar.md 2026-11-11). Video (7b) ve gerçek zamanlı kamera (Adım 8) vizeden sonra;
kod bunlar eklenebilecek şekilde çok sayfalı yapıda kuruldu.

---

## 2. Dosya yapısı ve görevleri
```
.streamlit/config.toml          tema ve sunucu ayarları (repo kökünde)
src/app/
  app.py                        giriş: sayfa ayarı, dil seçici, sayfa gezinmesi, alt not
  pages/goruntu.py              Görüntü sayfası: girdi, sonuç, eşik/sınıf filtresi, otomatik kaydırma
  core/model.py                 model yükleme (önbellekli + ısınma), tahmin, eşik süzme, cihaz seçimi
  core/texts.py                 tüm arayüz metinleri, sınıf ve ülke adları (TR/EN), t() yardımcı fonksiyonu
  core/classes.py               sınıf numarası → kod (D00…) ve sınıf renkleri
  core/draw.py                  kutu ve etiket çizimi
  core/images.py                görüntü okuma: EXIF yön düzeltme, uzun kenarı 1280'e küçültme
  assets/demo/                  10 örnek görüntü + KAYNAK.md (kaynak, lisans, değişiklikler) — git'e girer
src/data/select_demo_images.py  demo adaylarını seçen script (temas sayfası üretir)
runs/demo_secim/                aday listeleri ve temas sayfaları (git dışı)
```
`core/` modülleri sayfadan bağımsız: 7b'deki Video ve Adım 8'deki Kamera sayfaları aynı model, çizim ve metin
modüllerini kullanacak. Yeni sayfa `app.py`'deki `pages` listesine bir satırla eklenir; tek sayfa varken gezinme
menüsü gizli, sayfa sayısı artınca kendiliğinden görünür.

| Dosya | Önemli fonksiyonlar |
|---|---|
| `core/model.py` | `load_model` (bir kez yükle + ısınma), `predict` (tek tahmin, eşik 0,05), `filter_detections` (eşik + sınıf süzme), `pick_device` |
| `core/texts.py` | `t(anahtar)`, `class_name`, `country_name`, `check_keys` (iki dilin anahtarları eşit mi) |
| `core/draw.py` | `draw_detections`, `format_conf` (TR 0,82 / EN 0.82) |
| `core/images.py` | `load_image`, `limit_size` |
| `pages/goruntu.py` | `run_detection` (bayt önbelleği), `upload_tab`, `input_section`, `legend_line`, `detections_table`, `scroll_to_results` |

---

## 3. Nasıl çalıştırılır
Komutlar proje klasöründen (`C:\dev\yol-hasari`), PowerShell'de:
```powershell
venv\Scripts\activate
streamlit run src/app/app.py
```
Tarayıcıda `http://localhost:8501` açılır. Kurulum: `requirements.txt` (`streamlit==1.67.0` eklendi; kurulum torch,
ultralytics, numpy, pandas ve opencv sürümlerini değiştirmedi, `pip check` temiz).

- **Kökten çalıştırma şartı:** `.streamlit/config.toml` yalnızca komut repo kökünden çalıştırılınca okunur. Başka
  klasörden çalıştırılırsa uygulama açılır ama tema ve ayarlar uygulanmaz. (Model yolu dosya konumundan hesaplandığı
  için model her durumda bulunur.)
- **Değişiklikten sonra yeniden başlatma:** Dosya izleyici kapalı (`fileWatcherType = "none"`, §4.12). Kod
  değişince sayfa kendiliğinden yenilenmez: terminalde Ctrl+C, sonra yeniden `streamlit run`.
- **Model dosyası:** `runs/kaggle/e5_yolo26s_1024/weights/best.pt` git dışında. Başka bir bilgisayarda (ör. sunum
  bilgisayarı) bu dosya aynı yola elle kopyalanmalı; yoksa sayfa açık bir hata mesajı gösterir.
- **Demo görüntülerini yeniden üretmek** (gerekmedikçe değil):
  `venv\Scripts\python.exe src/data/select_demo_images.py` ve `... --cukur` (§5).

---

## 4. Teknik kararlar
1. **Tek tahmin + eşik süzme.** Model her görüntüde **bir kez**, çok düşük eşikle (0,05) çalışır. Kullanıcının
   eşiği (varsayılan **0,25**) ve sınıf filtresi yalnızca bu sonuçları süzer. Kaydırıcı oynatılınca model yeniden
   çalışmaz, ekran anında güncellenir. 0,25: e5'in val F1 eğrisinin tepesi 0,276; eğri 0,2–0,4 arası düz.
2. **Bayt önbelleği.** `run_detection` `st.cache_data` ile dosyanın içeriğine (baytlarına) göre önbelleğe alınır
   (20 görüntü). Aynı görüntü tekrar seçilince, dil değişince veya yüklenen fotoğraflar arasında geçilince model
   çalışmaz.
3. **Model bir kez yüklenir + ısınma.** `load_model` `st.cache_resource` ile tüm oturumlarda bir kez yüklenir.
   Hemen ardından siyah bir görüntüyle tahmin yapılır: ilk tahminde CUDA başlatma ve bellek ayırma olur, bu gecikme
   kullanıcının ilk görüntüsüne yansımaz.
4. **FP32: `quantize=32`.** GTX 1650'de FP16 bozuk (val mAP50 0,04; kararlar.md 2026-10-30). Ultralytics 8.4.182'de
   eski `half=False` parametresi kullanımdan kalkıyor ve her tahminde uyarı basıyordu; yerine `quantize=32` kullanıldı.
   Kaynak kod: `ultralytics/cfg/default.yaml` (`quantize`: "16/fp16 or 32/fp32/None … replaces deprecated half/int8
   args"), `ultralytics/cfg/__init__.py` (`half=False` → `quantize=None`), `ultralytics/engine/predictor.py`
   (`fp16 = quantize == 16`). **Doğrulama:** model yüklendikten sonra ağırlık tipine bakıldı:

   | quantize | fp16 bayrağı | ağırlık tipi |
   |---|---|---|
   | 32 | False | float32 |
   | None (varsayılan) | False | float32 |
   | 16 (kontrol) | True | float16 |

   `evaluate.py` ve `measure_fps.py` ikisini de vermiyor (varsayılan `None` = FP32); önceki ölçümler geçerli.
5. **Kendi çizimimiz** (`core/draw.py`), Ultralytics'in `result.plot()`'u değil:
   - sınıf renkleri bizim sabit paletimiz (Okabe–Ito, renk körü dostu): D00 mavi, D10 turuncu, D20 yeşil,
     D40 pembe-mor; aynı renkler kutuda, lejantta ve tabloda;
   - görüntü üzerindeki etiket kısa ve dilden bağımsız ("D40 0,82"); Türkçe adlar lejant ve tabloda;
   - Türkçe karakter çizilmediği için yazı tipi sorunu yok (Ultralytics ASCII dışı etikette internetten yazı tipi
     indirmeye çalışıyor; sunumda internet olmayabilir). Pillow'un içindeki yazı tipi kullanılıyor;
   - çizgi kalınlığı ve yazı boyu görüntü boyuyla orantılı.
6. **EXIF yön düzeltmesi.** Telefon fotoğrafları çoğu zaman yan kaydedilir, doğru yön EXIF bilgisindedir.
   `ImageOps.exif_transpose` ile düzeltilmeden modele giderse model yan yatmış yolu görür.
7. **Uzun kenar 1280'e küçültme.** Daha büyük görüntüler (ör. Norveç 4040 px, telefon fotoğrafları) 1280'e
   küçültülür. Norveç eğitimden önce de aynı şekilde küçültülmüştü (kararlar.md 2026-10-27); model zaten 1024'e
   indirdiği için doğruluk kaybı yok, çizim ve gösterim hızlanır. Yükleme sınırı 20 MB.
8. **Renk dönüşümü.** Görüntü RGB okunur; Ultralytics numpy girdiyi OpenCV gibi BGR beklediği için modele
   gitmeden önce çevrilir. Arayüzün kutu sayısı, aynı ayarlarla doğrudan `model.predict`'in sayısıyla karşılaştırıldı:
   aynı (duman testi, bir Norveç test görüntüsü).
9. **İki dil (TR/EN).** Tüm metinler `core/texts.py`'de, sayfalar metni `t("anahtar")` ile alır. Dil seçici kenar
   çubuğunun en üstünde, varsayılan Türkçe. Ondalık ayıracı dile göre (0,82 / 0.82). Eksik bir anahtar hata vermez,
   anahtarın kendisi görünür (sunumda çökmesin). `check_keys()` iki dilin anahtarlarının eşit olduğunu kontrol eder.
10. **Çoklu yükleme.** Birden fazla fotoğraf eklenebilir, çarpıya basılmadıkça listede kalır. Birden fazla dosya
    varsa dosya adlarıyla bir seçici çıkar; yeni eklenen fotoğraf otomatik seçilir. Dosyalar Streamlit'in her
    yüklemeye verdiği `file_id` ile ayırt edilir (aynı adlı iki dosya karışmaz). Örnek görüntüler sekmesiyle
    birlikte: en son yapılan seçim (yüklenen fotoğraf ya da örnek) gösterilir.
11. **Örnek görüntüler sekmesi.** 10 örnek, 5'erli iki satır. Küçük resimler ortadan **kare kırpılır** (Norveç geniş,
    diğerleri kare; böylece düğmeler aynı hizada). Yalnız küçük resim kırpılır, modele dosyanın tamamı gider.
    Küçük resmin altındaki düğmede yalnız ülke adı yazar; **seçili örneğin düğmesi vurgulu** (`type="primary"`).
    Sonuçların üstünde seçili görüntü satırı: "Seçili örnek: Çin (1/10)" veya "Yüklenen fotoğraf: <dosya adı>".
12. **Tema yalnız `config.toml` ile, özel CSS yok.** Vurgu rengi petrol mavisi `#1F4E5F`, sistem sans-serif yazı tipi
    (sunumda internet gerekmez), az yuvarlak köşeler, görünür giriş kenarlıkları, `paddingTop` ile başlık boşluğu.
    Streamlit'in iç CSS sınıflarına müdahale yok (sürüm değişince kırılabiliyor). Ayrıca: Deploy düğmesi gizli
    (`toolbarMode = "viewer"`), kullanım istatistiği kapalı, dosya izleyici kapalı (izleyici torch modüllerini
    tararken terminale hata basabiliyor).
13. **Otomatik kaydırma (JavaScript).** Örnek seçilince veya yeni fotoğraf yüklenince sayfa sonuç bölümüne kayar.
    - **Resmî yol yok:** Streamlit 1.67'nin Python API'sinde kaydırma fonksiyonu yok (`st` içinde ve kaynak kodda
      "scroll" geçen bir API bulunmadı).
    - **Çözüm:** sonuç bölümü `st.container(key="results")` içinde; Streamlit bu kaba `st-key-results` CSS sınıfını
      verir. `st.html(..., unsafe_allow_javascript=True)` ile eklenen kısa script 150 ms bekleyip bu öğeye yumuşakça
      kaydırır. `st.html` iframe'siz çalışır, yani script ana sayfada çalışır. Script sabit metin, kullanıcı girdisi
      içermez. `try/catch` sayesinde bir sorun olursa uygulama hata vermez, yalnız kaydırma olmaz.
    - **Yalnız seçim değişince:** son seçimin kimliği tutulur; eşik, sınıf filtresi veya dil değişince sayfa
      zıplamaz.
14. **Sorumluluk notu ve atıf.** Her sayfanın altında iki satır: "Bu araç karar desteği içindir; son karar
    insandadır." (Legal bölümündeki ilke) ve "Veri seti: RDD2022 (Arya vd., 2022), CC BY-SA 4.0."

---

## 5. Demo görüntülerinin seçimi
**Kaynak:** RDD2022'nin **etiketsiz resmî test klasörü** (`data/rdd2022/test/img`). Eğitimde, doğrulamada ve kendi
test bölmemizde kullanılmadı; kendi test bölmemize (`data/yolo` test) dokunulmadı. Görüntüler tek tek açılmadı;
script bir temas sayfası üretti, seçim oradan numarayla yapıldı.

**Yöntem** (`src/data/select_demo_images.py`; arayüzün kendi `core/` modüllerini kullanır, ayarlar birebir aynı:
imgsz 1024, FP32, eşik 0,25):
1. **Genel adaylar:** her ülkeden 8 rastgele görüntü (seed 42) → 48 aday, her ülke bir satır (#1–48).
2. **Çukur adayları:** ilk turda çukur (D40) yalnızca 2 görüntüde bulundu. Daha geniş örneklem tarandı: ABD hariç
   ülke başına 100 görüntü (seed 42), ilk turda olanlar atlandı → 497 görüntü, 51'inde D40. Önce en yüksek D40
   güvenine, eşitse en büyük çukur kutusuna göre sıralandı; en iyi 8'i ayrı temas sayfasında (#49–56).

**Seçilen 10 görüntü** (gösterim sırasıyla; `src/app/assets/demo/`):

| Sıra | Dosya | Aday no | Model ne buldu (eşik 0,25) |
|---|---|---|---|
| 01 | China_MotorBike_002019 | #1 | D00 1 |
| 02 | China_MotorBike_002021 | #2 | D10 1 |
| 03 | Japan_004644 | #26 | D10 1, D20 1 |
| 04 | China_MotorBike_002210 | #49 | D40 1 (0,86) |
| 05 | China_MotorBike_002459 | #51 | D00 6, D10 6, D20 1, D40 3 |
| 06 | Japan_002409 | #25 | D20 3, D40 2 |
| 07 | India_004435 | #20 | D20 1 |
| 08 | Norway_010007 | #38 | D00 3 |
| 09 | Japan_010270 | #30 | tespit yok (rögar kapağı çukur sanılmıyor) |
| 10 | Czech_001575 | #12 | tespit yok |

Norveç görüntüsü 3643×2041'den 1280×717'ye küçültüldü (arayüzle aynı yöntem, LANCZOS, JPEG 95); diğerleri bayt bayt
aynen kopyalandı. Toplam ~0,9 MB. Kaynak, lisans (CC BY-SA 4.0) ve değişiklikler `assets/demo/KAYNAK.md`'de.

**ABD neden yok:** ABD görüntülerinin alt köşelerinde "Google" filigranı var; Street View kaynaklı olabilirler ve
kullanım koşulları doğrulanmadı. Herkese açık repodaki demo setine ABD görüntüsü konmadı (kararlar.md 2026-11-14).
Eğitim ve değerlendirmede ABD görüntüleri kullanılmaya devam ediyor.

**Not:** Test klasörü etiketsiz; demodaki "doğru buldu" yalnız göz kararıdır. Sayısal sonuçlar val setinden gelir.

---

## 6. Elle yapılan testler ve gözlemler
Tarayıcıda (yerel, GTX 1650) elle denendi:

| Test | Sonuç |
|---|---|
| Dil geçişi (TR ↔ EN): metinler, sınıf/ülke adları, tablo başlıkları, ondalık ayıracı | Çalışıyor; seçimler ve eşik korunuyor |
| Eşik kaydırıcısı ve sınıf filtresi | Çalışıyor; model yeniden çalışmıyor |
| Çoklu yükleme, seçici, çarpıyla silme | Çalışıyor; geçişlerde model yeniden çalışmıyor |
| Örnek görüntüler: kare küçük resimler, vurgulu düğme, seçili görüntü satırı | Çalışıyor |
| Otomatik kaydırma | Seçim değişince kayıyor; eşik/dil değişince zıplamıyor |
| Alt not ve veri seti atfı | İki dilde görünüyor |
| Duman testi (betik): sayfa iki dilde hatasız, Norveç 4040 px → 1280×717, kutu sayısı = doğrudan `model.predict` | Geçti |

**Gözlemler: RDD2022 dışından yüklenen test fotoğrafları** (varsayılan eşik 0,25):

| Fotoğraf | Sonuç |
|---|---|
| Yol görünümü, alçak açı, ortada çatlak ağıyla çevrili büyük çukur | D40 bulunmadı; bölge **D20 0,86** olarak işaretlendi. 0,05 eşikte de çukur D40 olarak çıkmadı; ek kutular (D10 0,24 / 0,05, ikinci bir D40 0,08) yanlış pozitif görünümünde |
| Yakın çekim, içi su dolu çukur | **D40 0,84** |
| Hasarsız yol | Tespit yok |

- **Çatlak ağıyla çevrili çukurun D20 sanılması**, olası neden (doğrulanmadı): çukurun çevresindeki ağ deseni timsah
  çatlağının (D20) tipik görünümü; eğitim verisi araç kamerasından çekildiği için alçak açıdan çekilmiş büyük bir
  çukur farklı görünüyor olabilir. D40 zaten en zayıf sınıf (e5 val AP50 0,516).
- **Eşik düşünce yanlış pozitifler artıyor:** 0,05'te ek kutular çıkıyor (ilk satır). Varsayılanın 0,25 olmasının
  nedeni bu denge (§4.1).
- Örnek görüntülerden hasarsız yollar (09 ve 10) da varsayılan eşikte tespitsiz.

---

## 7. Bilinen sınırlar
- **Demo ≠ ölçüm:** Örnek görüntüler etiketsiz; arayüzde görülen başarı genellenemez. RDD2022 resmî test görüntüleri
  train ile aynı çekimlerden gelebilir (pHash kontrolü vizeden sonra).
- **Farklı bakış açısı:** model araç kamerası bakış açısıyla eğitildi. RDD2022 dışı fotoğraflarda sonuç değişken:
  su dolu yakın çekim çukur bulundu (D40 0,84), alçak açıdan çekilmiş, çatlak ağıyla çevrili büyük çukur D20 sanıldı
  (§6). Az sayıda fotoğrafla yapılan gözlem; genelleme yapılamaz.
- **CPU'da yavaş ama kullanılabilir:** e5 CPU'da 4,2 FPS (~0,25 s/görüntü); görüntü sayfası için yeterli, kamera için
  değil (Adım 8'de YOLO26n yedek).
- **`best.pt` git dışında:** başka bilgisayarda elle kopyalanmalı (GitHub Releases'a yükleme vizeden sonra).
- **Kaydırma JavaScript'e bağlı:** Streamlit'in iç yapısı değişirse (ör. `st-key-*` sınıfları) kaydırma sessizce
  durabilir; uygulama çalışmaya devam eder.
- **Dosya izleyici kapalı:** geliştirirken her değişiklikten sonra yeniden başlatmak gerekiyor.
- **Sonuç indirme yok:** 7b'de.

---

## 8. Bu adımda ne öğrendim
- Streamlit'in çalışma modeli: her etkileşimde script baştan sona yeniden çalışır; durum `st.session_state`'te tutulur.
- İki önbellek türü: `st.cache_resource` (model gibi paylaşılan nesne) ve `st.cache_data` (girdiye göre sonuç).
- Pahalı işi (model) bir kez yapıp ucuz işi (eşik süzme) her seferinde yapmak, arayüzü hızlı tutar.
- Bileşenlere `key` vermenin önemi: etiket dile göre değişse de bileşenin değeri korunur.
- `st.stop()` tüm script'i durdurur; sayfanın altındaki ortak öğeler (alt not) için erken çıkışta `return` kullanmak
  gerekir.
- Kütüphane uyarılarını okumak: `half` → `quantize` değişikliğini kaynak koddan doğrulayıp ağırlık tipiyle test etmek.
- Telefon fotoğraflarındaki EXIF yön bilgisi ve RGB/BGR farkı gibi küçük ama sonucu bozan ayrıntılar.

## 9. Hocaya nasıl anlatırım
"Arayüzü Streamlit ile yaptık, tamamen Python. Kullanıcı bir yol fotoğrafı yüklüyor ya da hazır örneklerden birini
seçiyor; final modelimiz YOLO26s, 1024 piksellik girdiyle hasarları buluyor ve her birini kutu, sınıf ve güven
skoruyla gösteriyor. Güven eşiğini kaydırıcıyla değiştirebiliyoruz: düşürünce daha çok hasar bulunuyor ama yanlış
alarm artıyor, yükseltince tersi. Varsayılan 0,25, doğrulama setinde F1'in en yüksek olduğu nokta. Model her
görüntüde bir kez çalışıyor, eşik yalnızca sonuçları süzüyor; bu yüzden arayüz anında tepki veriyor. GTX 1650'de
FP16 bozuk sonuç verdiği için FP32 kullanıyoruz ve bunu doğruladık. Örnek görüntüler veri setinin etiketsiz resmî
test klasöründen; eğitimde hiç kullanılmadı. Arayüz Türkçe ve İngilizce. Altta da belirttiğimiz gibi bu bir karar
destek aracı, son karar insanda. Video ve gerçek zamanlı kamera sayfaları aynı altyapıyla vizeden sonra eklenecek."
