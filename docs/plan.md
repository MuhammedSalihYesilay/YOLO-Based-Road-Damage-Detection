# Yol Hasarı Tespiti — Proje Planı (v2, 2026-10-15)

## Context
Danışmana verilen proje önerisi (YOLO-Based Road Damage Detection, `docs/proje-onerisi.md`)
CLAUDE.md ve plan v1 ile karşılaştırıldı. Öneri; 4 hasar sınıfı, YOLO ile eğitim,
standart metriklerle değerlendirme ve görüntü + gerçek zamanlı kamera girdisi alan
bir Streamlit web arayüzünden oluşuyor. CLAUDE.md'deki GPS, veritabanı, harita ve
hasar takibi öneride yok. **Karar:** ana kapsam önerinin kendisi, bu dört özellik
zaman kalırsa yapılacak ek özellikler. Arayüz Streamlit web, backend tamamen Python.
Bu plan v1'in yerini alıyor; v1'deki veri seti bulguları (A bölümü) korunuyor.

---

## 1. Öneri ile CLAUDE.md / plan v1 karşılaştırması

| Konu | Öneri | CLAUDE.md / plan v1 (eski) | Değerlendirme |
|---|---|---|---|
| Sınıflar | pothole, longitudinal, transverse, alligator | D00/D10/D20/D40, aynı 4 sınıf | ✅ Uyumlu |
| Model | Ultralytics YOLO | YOLO tabanlı, sürüm açık | ✅ Uyumlu; sürüm hâlâ açık |
| Veri | "publicly available dataset" | RDD2022 (datasetninja) | ✅ Uyumlu |
| Değerlendirme | "standard object detection metrics" | Hiç yok | ❌ Eksikti → §4 |
| Arayüz | Web, Streamlit, görüntü yükleme + gerçek zamanlı kamera | "Web mi mobil mi" açık; "kameradan prototip" | ⚠️ Karar netleşti: Streamlit web |
| Backend | Teknolojilerde sadece Python | "Python mı, Python + Spring Boot mu" açık | ⚠️ Karar: tamamen Python, Spring Boot yok |
| GPS, veritabanı, harita, takip | Yok | Ana bileşen olarak yazılı | ⚠️ Ek özelliklere taşındı |
| Teknolojiler | Python, PyTorch, Ultralytics, OpenCV, Streamlit, Git | Listelenmemiş | ❌ Eksikti → §3 |
| SDG 11 / Kategori | Var | Yok | ❌ Eksikti (rapor için gerekli) |
| Video | "images and real-time video streams" | Yok | ⚠️ Gerçek zamanlı kamera var; video dosyası yükleme de eklendi (az ek iş) |

## 2. Eksikler listesi (giderilenler)
1. Teknoloji listesi ve her birinin rolü → §3
2. Değerlendirme metrikleri ve hedef (referans mAP50 = 0,547) → §4
3. Eğitim ortamı (yerel GTX 1650 4 GB yetmez) → §5
4. Streamlit arayüzü ve gerçek zamanlı kamera adımları → §6, Adım 7-8
5. Rapor ve sunum hazırlığı → Adım 10
6. Haftalık zaman çizelgesi → §8
7. **Ek olarak bulunan eksikler:**
   - **Test setinin tek kullanımı:** test parçası sadece en sonda, seçilen model için bir kez kullanılır. Model seçimi val üzerinden yapılır; aksi halde sonuç "kopya" sayılır.
   - **Adil karşılaştırma:** referansın 0,547'si kendi Japonya+Hindistan val bölmesinde ölçülmüş. Bizim modeli test setimizin Japonya+Hindistan alt kümesinde ayrıca ölçüp raporlanan 0,547 ile karşılaştıracağız. Referansın hazır modelini bizim test setimizde ölçmeyeceğiz (veri sızıntısı, bkz. Doğrulama).
   - **Deney kayıt tablosu:** her eğitimin ayarları ve sonuçları `docs/deneyler.md` dosyasına yazılır (rapordaki karşılaştırma tablosunun kaynağı).
   - **Tekrarlanabilirlik:** sabit seed, `requirements.txt` sürümleri sabit, veri bölme listesi dosyaya kaydedilir.
   - **Ekip içi görev dağılımı:** 2 kişi paralel çalışabilir (biri model, biri arayüz) → §7 sonu.
   - **Git/GitHub iş akışı:** uzak depo; `data/` ve ağırlık dosyaları (`*.pt`) git dışında; ağırlıklar GitHub Releases'ta saklanır (kararlar.md, 2026-10-18).
   - **Lisans ve atıf:** RDD2022 CC BY-SA 4.0, atıf zorunlu. Referans projede LICENSE dosyası yok; kodunu kopyalamayıp inceleyerek kendimiz yazacağız ve raporda atıf vereceğiz.
   - **Risk planı:** eğitim süresi, Kaggle kotası, tarayıcı kamera izinleri (webrtc), sunumda internet olmaması → yedek demo videosu.
   - **Referans uygulamadaki bir hata:** görüntüyü elle 640x640'a `cv2.resize` ediyor, bu en-boy oranını bozuyor. Biz Ultralytics'in kendi `imgsz` ön işlemesini kullanacağız.

---

## 3. Teknolojiler: projede ne işe yarıyor?
| Teknoloji | Ne işe yarıyor | Projedeki yeri |
|---|---|---|
| **Python 3.13** | Tüm kodun yazıldığı dil | Analiz, dönüştürme, eğitim, arayüz |
| **venv** | Projeye özel paket ortamı; sürüm çakışmalarını önler | Kurulum |
| **PyTorch** | Sinir ağlarının hesaplandığı derin öğrenme kütüphanesi (GPU üzerinde tensör işlemleri, geri yayılım) | Ultralytics arka planda bunu kullanır, biz doğrudan pek yazmayız |
| **Ultralytics YOLO** | Hazır YOLO modelleri ve `train / val / predict` komutları | Eğitim, değerlendirme, arayüzde tahmin |
| **OpenCV** | Görüntü ve video okuma/yazma, kutu çizme, kamera karelerini işleme | Video sayfası, gerçek zamanlı kamera, görselleştirme |
| **Streamlit** | Python ile birkaç satırda web arayüzü (HTML/JS bilmeden) | Görüntü / video / kamera sayfaları |
| **streamlit-webrtc** | Tarayıcı kamerasını Streamlit'e gerçek zamanlı aktarır | Gerçek zamanlı kamera sayfası |
| **pandas, matplotlib** | Tablo işleme ve grafik çizme | Veri analizi, rapor grafikleri |
| **Git / GitHub** | Sürüm kontrolü ve iki kişinin aynı kod üzerinde çalışması | Tüm proje boyunca |
| **Kaggle / Colab** | Ücretsiz bulut GPU | Asıl eğitimler |

## 4. Değerlendirme metrikleri ve hedef
- **Metrikler:** Precision, Recall, F1, **mAP50** (ana metrik, referansla karşılaştırma için), **mAP50-95**, sınıf başına AP, karışıklık matrisi (confusion matrix), PR eğrisi, çıkarım hızı (ms/görüntü ve FPS; hem GPU hem CPU'da). (açıklamalar: docs/ogrenme/metrikler.md)
- **Kırılımlar:** ülke bazında mAP (özellikle Norveç ve China_Drone), sınıf bazında mAP (D40'ın azınlık sınıfı olarak durumu).
- **Hedef:**
  1. Test setinin Japonya+Hindistan alt kümesinde **mAP50 ≥ 0,547** (referansın raporladığı değeri yakalamak/geçmek).
  2. Tüm ülkeler için genel hedef baseline sonrası belirlenecek. Not: Norveç ve Drone eklendiği için genel mAP'ın Japonya+Hindistan'dan düşük çıkması normal.
  3. Gerçek zamanlı kamerada kullanılabilir hız (hedef: yerel GTX 1650'de ≥ 15 FPS).

## 5. Eğitim ortamı (önerilen)
- **Yerel (GTX 1650, 4 GB):** küçük denemeler, hattı doğrulama, arayüz ve tahmin. 4 GB ile v8s/640 için batch ≈ 8 civarı çalışır, tam eğitim günler sürer.
- **Kaggle (önerim):** haftada ~30 saat ücretsiz GPU (P100 / T4x2), oturum en fazla 12 saat; veri seti yüklenip kalıcı tutulabiliyor. Colab yedek seçenek.
- **İş bölümü (karar, 2026-10-18):** ağır eğitim Kaggle'da; analiz, dönüştürme, bölme, küçük denemeler, final test, değerlendirme, FPS ve arayüz yerelde. FPS yalnızca yerelde (GTX 1650).
- **Kaggle düzeni (karar, 2026-10-18):** veri Adım 3'ten sonra YOLO formatında, Norveç küçültülmüş halde private dataset olarak yüklenir; Hakan collaborator, kendi hesabıyla da eğitim yapabilir (kota hesap başına). Cache kapalı, veri `/kaggle/input`, çıktılar `/kaggle/working`.
- **Hazırlık:** Norveç görüntüleri 4040 px. Yüklemeden önce eğitim boyutuna uygun küçültülmüş kopya hazırlamak hem yükleme süresini hem disk kullanımını ciddi azaltır (Norveç boyut kararına bağlı, Adım 2).

## 6. Kapsam
**Ana kapsam (öneri, teslimde olmazsa olmaz):**
veri hazırlığı → YOLO eğitimi + model/augmentation karşılaştırması → metriklerle değerlendirme → Streamlit web: görüntü yükleme, video yükleme, gerçek zamanlı kamera (kutu + sınıf + güven skoru).

**Ek özellikler (ana kapsam bitince, öncelik sırasıyla):**
1. GPS eşleştirme (telefon konumu / video metadata) 2. Veritabanı kaydı 3. Harita gösterimi 4. Aynı hasarın zaman içinde takibi.
Teknoloji önerisi (karar ileride): SQLite + folium/streamlit-folium. Böylece her şey Python'da kalır.

---

## A. Veri seti bulguları
**Durum:** 1-10 ve 12-16 onaylandı ve CLAUDE.md'ye işlendi; 11 (ısı haritası) CLAUDE.md'den kaldırıldı.
Kaynak: tüm ann JSON'ları sayıldı (38.385 train + 9.035 test), görüntü boyutları ülke başına örneklemle doğrulandı, datasetninja sayfasıyla karşılaştırıldı.

| # | CLAUDE.md'de yazan (eski) | Gerçekte olan | Neden önemli |
|---|---|---|---|
| 1 | Sınıflar D00/D10/D20/D40 kodlarıyla | Veri setinde kod yok; **isim** var. Format **Supervisely JSON**, Pascal VOC XML değil. | Eşleme `classTitle` adıyla yapılmalı; referans dönüştürücü kullanılamaz. |
| 2 | "Diğer sınıflar (varsa)" | 7 sınıf var; **other corruption 5.850** (D43/D44). `block crack`, `repair` 0 etiket. | Kesin var; atılacak. |
| 3 | D40 ~6-7 bin (tahmini) | D00 26.196, D10 11.875, D20 10.617, D40 **6.544** | Teyit edildi. |
| 4 | D40 = çukur | Detay tag'i: "rutting, bump, pothole, separation" | Sınıf daha geniş. |
| 5 | ~47 bin görüntü, tamamı | 47.420 görüntünün **38.385'i etiketli**; test etiketsiz | Eğitim havuzu 38.385. |
| 6 | Japonya 600x600 | Ek olarak 540 (124), 1024 (147), 1080 (48) | Boyut kararı. |
| 7 | Norveç 3650x2044 | 4040x2035 (4.342), 3643x2041 (2.896), 3650x2044 (923); train 8.161 | Boyut kararı. |
| 8 | Çin 512x512 | İki alt küme: China_Drone (2.401, sadece train), China_MotorBike (1.977) | Drone ayrı ele alınmalı. |
| 9 | (Yok) | **12.658 boş görüntü (%33)**; Norveç %64, Çek %62, Hindistan %51, ABD %0 | Arka plan oranı kararı. |
| 10 | Referans Python 3.10 | Referans: Py 3.8, ultralytics 8.0.201, sadece Japonya+Hindistan, v8s, 640, mAP50 0,547 | Karşılaştırma değeri. |
| 11 | Isı haritası maddesi | Bağlantı bulunamadı | **Kaldırıldı.** |
| 12 | docs/, src/, .gitignore | src/ ve .gitignore yok, git deposu değil (docs/ oluşturuldu) | Git kuruldu 2026-10-15; src/ henüz yok. |
| 13 | Hindistan 720x720 | 960x720 çekilip 720x720'ye sıkıştırılmış | En-boy oranı bozuk. |
| 14 | Norveç 3650x2044 | Site de böyle diyor ama veride en az görülen boyut; Norveç CVAT ile etiketlenmiş | Veriye güveniyoruz. |
| 15 | Japonya/Çek 600x600 | Site eksik (madde 6) | Veriye güveniyoruz. |
| 16 | Ülke sayıları | Site sayıları train+test toplamı, bizimkiyle birebir tutuyor | Çelişki yok. |

Sitede tutanlar: toplamlar (47.420 görüntü, 61.082 etiket, 12,86 GB), sınıf etiket sayıları, etiketsiz 21.693 görüntü (= 12.658 boş train + 9.035 test), lisans CC BY-SA 4.0, kaynak Arya vd. 2022 (arXiv:2209.08538). Sitedeki "55.000'den fazla nesne", bizim 4 sınıfın toplamıyla (55.232) uyumlu.

---

## 7. Adımlar ("Ne öğreneceğim" ve "Hocaya nasıl anlatırım" notlarıyla)

**Adım 0: Kurulum**
~~git init + GitHub deposu, `.gitignore` (data/, reference/, venv/, runs/, *.pt, *.onnx, __pycache__/, kaggle.json)~~ ✅ 2026-10-15. (`docs/kararlar.md`, `docs/proje-onerisi.md` ve CLAUDE.md düzeltmeleri 2026-10-15'te yapıldı.)
- ✅ 2026-10-18: Hakan (hakan0363) collaborator daveti kabul etti; NVIDIA sürücüsü 617.42 (CUDA 13.4'e kadar); Kaggle hesabı hazır (telefon doğrulandı; GPU 30 sa/hafta, private dataset 214,75 GB); disk 72,9 GB boş
- ✅ 2026-10-18: python.org Python 3.13.16 + `venv/`; torch 2.14.1+cu130, ultralytics 8.4.182, opencv, pandas, matplotlib; `requirements.txt` (cu130 dahil); `torch.cuda.is_available()` = True; hazır model yeni ultralytics'te açıldı ve tahmin üretti, ONNX'e gerek yok (kararlar.md)
- Kalan: Kaggle GPU deneme notebook'u
- *Ne öğreneceğim:* venv neden gerekli, git commit/push/branch, iki kişiyle çakışmadan çalışma.
- *Hocaya:* "Proje sürüm kontrollü ve tekrar kurulabilir; büyük veri ve model dosyaları depoya girmiyor."

**Adım 1: Veri analizi** — `src/analysis/analyze_dataset.py` (argparse ile veri yolu ve çıktı klasörü) → `docs/analysis/` (`summary.md` + CSV + PNG)
Görüntüleri tek tek açmaz; sadece `ann/*.json` okunur, boyut doğrulaması için ülke başına küçük örneklem açılır. Hesaplananlar:
1. Ülke bazında görüntü sayısı, boş görüntü oranı (4 sınıf filtresinden önce/sonra), boyutlar
2. Sınıf × ülke tablosu (4 hedef sınıf + atılacaklar)
3. Görüntü başına etiket sayısı dağılımı
4. Kutu geometrisi (sınıf ve ülke bazında): normalize alan, genişlik/yükseklik, en-boy oranı; 640'a küçültüldüğünde kaç piksel kaldığı (Norveç kararı için kritik)
5. Kalite kontrolleri: taşan / sıfır boyutlu kutular, eşleşmeyen ann–img dosyaları, JSON `size` ile gerçek boyutun örneklemde uyuşması
6. Sınıf başına görüntü sayısı; sitedeki değerlerle karşılaştırma (13.657 / 7.744 / 8.412 / 3.674)
7. Norveç kutu stili (CVAT): diğer ülkelerden farklı mı?
8. China_Drone ayrı özeti
9. Bölme önizlemesi: ülke + "boş mu?" bilgisine göre katmanlı %80/10/10 bölmede her parçanın sınıf dağılımı (dosya kopyalanmaz)
- *Ne öğreneceğim:* Supervisely etiket formatı, bounding box kavramı, pandas/matplotlib, sınıf dengesizliği.
- *Hocaya:* "Modeli eğitmeden önce veriyi tanıdık: hangi sınıf az, hangi ülke farklı, küçük nesne sorunu nerede. Kararlarımız bu analize dayanıyor."

**Adım 2: Veri kararları** (Norveç boyutu, arka plan oranı, katmanlı bölme, eğitim ortamı) → kararlar.md
- *Ne öğreneceğim:* imgsz, tiling, arka plan görüntüsünün yanlış pozitiflere etkisi, train/val/test ayrımının anlamı.
- *Hocaya:* "Her kararın gerekçesi analizdeki bir sayıya dayanıyor" (ör. "Norveç'te kutuların %X'i 640'ta 8 pikselin altına düşüyor").

**Adım 3: YOLO formatına dönüştürme + bölme** — `src/data/prepare_yolo.py`, `data.yaml`, bölme listesi dosyaya kaydedilir
- Supervisely JSON → YOLO txt; eşleme isimle: longitudinal→0, transverse→1, alligator→2, pothole→3, diğerleri atılır.
- Referanstaki `convertPascal2YOLOv8` mantığı (normalize cx, cy, w, h) örnek alınır (`reference/.../training/0_PrepareDatasetYOLOv8.ipynb`). Referanstaki iki zayıflık düzeltilir: görüntü–etiket eşleştirmesi dosya adıyla yapılır; val'in yanında test parçası da üretilir.
- 10 GB'ı kopyalamamak için mümkünse hardlink.
- *Ne öğreneceğim:* YOLO etiket formatı (sınıf cx cy w h, normalize), stratified split, seed.
- *Hocaya:* "Etiketleri modelin anladığı formata çevirdik; %80/10/10 böldük, ülke dağılımı her parçada aynı. 20 rastgele örneği çizip doğruladık."

**Adım 4: Baseline eğitim** (önce yerelde YOLOv8n ile kısa deneme, sonra Kaggle'da referans ayarları: v8s, 640)
- **Checkpoint ile devam:** Kaggle oturumu en fazla 12 saat sürüyor. Eğitim her epoch sonunda `last.pt` kaydeder (ayrıca `save_period` ile ara kayıtlar alınır). Çıktı klasörü oturum bitmeden Kaggle "output/dataset" olarak saklanır. Yeni oturumda `YOLO("last.pt").train(resume=True)` ile kaldığı epoch'tan devam edilir. İlk denemede bilerek yarıda kesip devam ettirerek bu akış test edilir. Referans projedeki "Resume Training" hücresi örnek alınır (`reference/.../training/1_TrainingYOLOv8.ipynb`).
- *Ne öğreneceğim:* epoch, batch, öğrenme oranı, transfer learning (COCO ön-eğitimli ağırlıklar), loss eğrilerini okumak, overfitting, checkpoint/resume mantığı.
- *Hocaya:* "Sıfırdan değil, önceden eğitilmiş bir modeli kendi verimize uyarladık (transfer learning). Bu baseline'ımız."

**Adım 5: Değerlendirme script'i** — `src/eval/`: val/test metrikleri, ülke ve sınıf kırılımı, Japonya+Hindistan alt kümesi, FPS ölçümü → `docs/deneyler.md`
- *Ne öğreneceğim:* IoU, precision/recall, mAP50 ile mAP50-95 farkı, confusion matrix okuma.
- *Hocaya:* "mAP50, tahmin kutusu gerçek kutuyla en az %50 örtüşünce doğru sayılan ortalama kesinlik. Bizim modeli Japonya+Hindistan alt kümesinde ölçüp referansın raporladığı 0,547 ile karşılaştırdık."

**Adım 6: Karşılaştırma deneyleri** (val üzerinde)
- Modeller: YOLOv8s, YOLO11s, YOLO26s + kamera için YOLO26n; aynı ayarlarla 50 epoch + early stopping; seçilen modelde imgsz 640 ve 960/1024 deneyi (ayrıntı: docs/arastirma/yolo-modelleri.md)
- Augmentation: varsayılan, mosaic kapalı (referans gibi), çukur odaklı ek artırma.
- Sınıf dengesizliği: sınıf ağırlığı / oversampling denemesi.
- *Ne öğreneceğim:* model boyutu ile hız ve doğruluk ilişkisi, augmentation türleri, dengesiz veriyle başa çıkma.
- *Hocaya:* "Aynı veriyle, tek bir değişkeni değiştirerek karşılaştırdık; tablo ve grafik burada. En iyisini val'e göre seçtik, test'e en son bir kez baktık."

**Adım 7: Streamlit arayüzü** — `src/app/`: Home, Görüntü, Video sayfaları; güven eşiği kaydırıcısı; sonuç indirme. Bizim model hazır olana kadar referansın hazır modeliyle test edilir.
- *Ne öğreneceğim:* Streamlit sayfa yapısı, model önbellekleme (`st.cache_resource`), OpenCV ile video kare kare işleme.
- *Hocaya:* "Kullanıcı görüntü veya video yükler; model her hasarı kutu, sınıf ve güven skoruyla gösterir."

**Adım 8: Gerçek zamanlı kamera** (streamlit-webrtc; yerelde test, FPS ölçümü, düşük FPS'te küçük model/imgsz seçeneği)
- *Ne öğreneceğim:* WebRTC'nin temel mantığı, kare başına çıkarım süresi, hız/doğruluk dengesi.
- *Hocaya:* "Tarayıcı kamerasından gelen her kare modele gidiyor; GTX 1650'de X FPS elde ettik."

**Adım 9: Final değerlendirme** (seçilen modelle test setinde tek ölçüm, örnek doğru/yanlış tahminler, hata analizi)
- *Ne öğreneceğim:* hata analizi; modelin nerede, neden yanıldığını yorumlamak.
- *Hocaya:* "Model en çok X'te zorlanıyor çünkü Y" (ör. ince boyuna çatlaklar, Norveç'in küçük nesneleri).

**Adım 10: Rapor ve sunum** (rapor taslağı Aralık başında başlar; slaytlar; yedek demo videosu; SDG 11 bağlantısı; prova)
- *Ne öğreneceğim:* bilimsel rapor yapısı (giriş, ilgili çalışmalar, yöntem, deneyler, sonuç), sonuçları görselleştirme.
- *Hocaya:* "Belediyeler yol bakımını önceliklendirebilir → SDG 11 sürdürülebilir şehirler."

**Adım 11 (ek, zaman kalırsa):** GPS → SQLite → harita → takip.

### Görev dağılımı önerisi (2 kişi)
Kişi A / Kişi B'nin kim olacağı henüz belli değil (§10).
- **Kişi A (model):** Adım 1-6, 9
- **Kişi B (uygulama):** Adım 7-8 (başta referansın hazır modeliyle, sonra bizim modelle), Git düzeni, ek özellikler
- **Ortak:** Adım 2 kararları, rapor, sunum
- **Not:** Her hafta birbirimize yaptıklarımızı anlatırız; ikimiz de projenin tamamını sunabilmeliyiz.

## 8. Haftalık zaman çizelgesi (teslim ~2 Ocak 2027)
| Hafta | Tarih | Model tarafı (A) | Uygulama tarafı (B) |
|---|---|---|---|
| 1 | 19–25 Eki | Kurulum, analiz script'i | Kurulum, Git/GitHub, Streamlit + Ultralytics ile tanışma |
| 2 | 26 Eki–1 Kas | Analiz sonuçları, veri kararları, dönüştürücü + bölme | Referans uygulamayı çalıştırıp inceleme, iskelet `src/app/` |
| 3 | 2–8 Kas | Kaggle kurulumu, YOLOv8n kısa deneme (resume testi dahil) | Görüntü sayfası (hazır modelle) |
| 4 | 9–15 Kas | Baseline v8s/640, değerlendirme script'i | Video sayfası |
| 5 | 16–22 Kas | Model karşılaştırması | Gerçek zamanlı kamera (webrtc) ilk sürüm |
| 6 | 23–29 Kas | Augmentation + dengesizlik deneyleri | Kamera FPS ölçümü, arayüz iyileştirme |
| 7 | 30 Kas–6 Ara | Final model seçimi, test ölçümü, hata analizi | Final modeli arayüze bağlama |
| 8 | 7–13 Ara | **Ana kapsam tamam** (kontrol noktası). Rapor: veri + yöntem | Ek özellik 1 (GPS) başlarsa |
| 9 | 14–20 Ara | Rapor: deneyler + sonuçlar | Ek özellikler (DB, harita) zaman kalırsa |
| 10 | 21–27 Ara | Slaytlar, demo videosu, prova | Slaytlar, demo videosu, prova |
| 11 | 28 Ara–3 Oca | Tampon + teslim | Tampon + teslim |

Not: vize/final haftaları ve kesin teslim tarihi bilinince çizelge güncellenecek.

---

## 9. Belge değişiklikleri (onaylandı, 2026-10-15'te uygulandı)
- `docs/proje-onerisi.md` oluşturuldu (öneri metni aynen).
- `CLAUDE.md` güncellendi: ana kapsam / ek özellikler ayrımı, Teknolojiler ve Değerlendirme bölümleri, Streamlit + tamamen Python kararları, SDG 11 ve kategori, veri seti düzeltmeleri (A 1-10, 12-16), ısı haritası maddesinin silinmesi, ekip notu, "ne öğreneceğim / hocaya nasıl anlatırım" kuralı.
- `docs/plan.md` bu v2 ile değiştirildi.
- `docs/kararlar.md` oluşturuldu.

## 10. Açık konular (2026-10-18; çoğu Adım 1 analizini bekliyor)
1. **Deney bütçesi:** Hafta 5'teki 4 model karşılaştırması (50 epoch) haftalık 30 saatlik Kaggle kotasına sığmıyor. Adım 4'te baseline'ın epoch süresi ölçülünce iki hesapla ve koşu planıyla yeniden hesaplanacak.
2. **Ardışık kare (sekans) sızıntısı:** Adım 1'de dosya adlarında sekans/çekim bilgisi var mı bakılacak; varsa bölme sekans bazında yapılacak (aynı sekansın kareleri hem train hem test'e düşmemeli).
3. **Görev dağılımı:** Kişi A / Kişi B kim olacak, belli değil. Branch düzeni önerisi: herkes kendi dalında çalışır, `main`'e Pull Request ile birleştirir.
4. **`docs/deneyler.md` sütun şablonu** belirlenecek.
5. **Hindistan'ın bozuk en-boy oranı:** karar verilecek (muhtemelen dokunulmayacak).
6. **Vize/final tarihleri** belli olunca §8 çizelgesi güncellenecek.

## Doğrulama
- CLAUDE.md, plan.md ve proje-onerisi.md arasında kapsam, teknoloji ve karar çelişkisi kalmamalı.
- Adım 1: toplamlar tutmalı (38.385 görüntü / 61.082 etiket / D00 26.196 / D10 11.875 / D20 10.617 / D40 6.544).
- Adım 3: 20 rastgele örnek kutularıyla çizilip göz kontrolü; `yolo val/train` veri setini hatasız taramalı.
- Adım 5: bizim modelin Japonya+Hindistan test alt kümesindeki mAP50'si, referansın **raporladığı** 0,547 ile karşılaştırılır.
- **Referansın hazır modeli (`YOLOv8_Small_RDD.pt`) bizim test setimizde ölçülmez.** Aynı havuzdaki Japonya+Hindistan train görüntüleriyle eğitildi; bizim test görüntülerimizin bir kısmını görmüş olabilir (veri sızıntısı). Yalnızca arayüzün uçtan uca çalıştığını test etmek için kullanılır (Adım 7-8).
- Not: 0,547 referansın kendi val bölmesinde, farklı görüntülerde ölçüldü. Karşılaştırma yaklaşık; raporda böyle belirtilecek.
