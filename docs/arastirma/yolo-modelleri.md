# Araştırma: YOLO modelleri (2026-10-15)

**Karar:** YOLOv8s, YOLO11s, YOLO26s karşılaştırılacak; gerçek zamanlı kamera ve hız için YOLO26n.

## Resmi Ultralytics tabloları (COCO, 640 px)
| Model | Çıkış | mAP50-95 (COCO) | CPU ONNX ms | Parametre (M) | FLOPs (B) |
|---|---|---|---|---|---|
| YOLOv8n | Oca 2023 | 37,3 | 80,4 | 3,2 | 8,7 |
| YOLOv8s | Oca 2023 | 44,9 | 128,4 | 11,2 | 28,6 |
| YOLO11n | Eyl 2024 | 39,5 | 56,1 | 2,6 | 6,5 |
| YOLO11s | Eyl 2024 | 47,0 | 90,0 | 9,4 | 21,6 |
| YOLO26n | Oca 2026 | 40,9 | 38,9 | 2,4 | 5,5 |
| YOLO26s | Oca 2026 | 48,6 | 87,2 | 9,5 | 20,9 |
| YOLO26m | Oca 2026 | 53,1 | 220,0 | 20,4 | 68,4 |

Kaynaklar: [YOLOv8](https://docs.ultralytics.com/models/yolov8/), [YOLO11](https://docs.ultralytics.com/models/yolo11/), [YOLO26](https://docs.ultralytics.com/models/yolo26), [YOLO26 vs YOLO11](https://docs.ultralytics.com/compare/yolo26-vs-yolo11), [YOLO26 makalesi](https://arxiv.org/abs/2606.03748)

**YOLO26'nın yenilikleri:**
- NMS gerektirmeyen uçtan uca çıkarım (isteğe bağlı)
- DFL'in kaldırılması
- ProgLoss
- Küçük nesneler için **STAL** etiket ataması
- MuSGD optimizer

Makalenin kendi deneyinde STAL'ın küçük nesnelerdeki kazancı küçük: AP_S 29,0'dan 29,6'ya çıkıyor.

## Yol hasarında kanıtlar
- **RDD2022, topluluk sonuçları** (hakemli değil, zayıf kanıt). Ayarlar: 4 sınıf, 70/15/15 bölme, 640 px, 50 epoch.
  - mAP50: **YOLOv8s 61,45**, **YOLO26s 61,27**, YOLO26m 61,24, YOLOv8m 62,03, YOLOv8n 58,8.
  - Sınıf bazında (YOLO26s): pothole 74,5, alligator 62,1, longitudinal 54,7, transverse 53,8.
  - Model kartı ayrıca büyük kareler 640'a küçültülünce ince çatlakların kaybolduğunu not ediyor.
  - Kaynak: [HF model kartı](https://huggingface.co/dronefreak/rdd2022-yolo26s)
- **Çatlak veri seti (MDPI Sensors 2026):** mAP50 YOLO26s %89,0, YOLO11s %88,6, YOLOv8s yaklaşık %88,1. Fark yaklaşık 1 puan. Kaynak: [doi:10.3390/s26165113](https://doi.org/10.3390/s26165113)
- **Sonuç:** Yol hasarında yeni sürümlerin kazancı 1 puanı geçmiyor, bazen hiç yok. Bu yüzden karşılaştırmayı kendi verimizde yapmak raporda anlamlı bir bulgu olacak.

## Seçilen modeller ve gerekçeleri
| Model | Neden |
|---|---|
| **YOLOv8s** | Referansla aynı mimari ve boyutta. 0,547 karşılaştırmasının dayanağı: farkın veriden ve eğitimden mi, yoksa mimariden mi geldiğini ayırmayı sağlar. |
| **YOLO11s** | Bir önceki nesil. Daha az parametre ve FLOPs ile COCO'da 2 puan daha yüksek; olgun ve yaygın kullanılan bir sürüm. |
| **YOLO26s** | En yeni sürüm. Küçük nesne odaklı STAL, CPU'da daha hızlı ve NMS'siz çıkarım (kamerada gecikmeyi azaltır). Bu kazancın kendi verimizde gerçekleşip gerçekleşmediği raporun ilginç sorularından biri. |
| **YOLO26n** | Gerçek zamanlı kamera için en küçük ve en hızlı model. "s yerine n kullanınca ne kadar doğruluk kaybediyoruz?" sorusunu da cevaplar. |

**Dahil edilmeyenler:**
- **m/l/x:** Kaggle süresi ve GTX 1650 hızı açısından pahalı. RDD2022'de m'nin s'ye üstünlüğü yaklaşık 0,6 puan.
- **YOLOv8n, YOLO11n:** Zaman kalırsa eklenir; n tarafında tek model (YOLO26n) yeterli.

## Eğitim süresi ve bütçe
Tahmindir, ilk koşuda ölçülecek.
- ~30 bin train görüntüsü, s modeli, 640 px, Kaggle T4/P100: epoch başına kabaca 10–15 dk (**doğrulanmadı**). 50 epoch yaklaşık 8–12 saat, yani yaklaşık 1 Kaggle oturumu. Haftalık ~30 saatlik kotayla haftada 2–3 koşu yapılabilir.
- Karşılaştırma koşuları **aynı ayarlarla 50 epoch + early stopping** (patience 10) yapılacak. Seçilen model gerekirse daha uzun eğitilecek. Checkpoint ve resume şart.
- Norveç'in 4040 px'lik görüntüleri veri yüklemeyi yavaşlatıyor. Önceden küçültülmüş bir kopya hem süreyi hem disk kullanımını azaltır.
- **Küçük nesne deneyi:** Seçilen modelle imgsz 640 ile 960/1024 karşılaştırılacak. Bu, Norveç'te ince çatlakların kaybolması sorununa doğrudan cevap verir.
- GTX 1650'de Ultralytics'in AMP (FP16) kontrolü sorun çıkarabiliyor; yerel denemeler FP32 ile yavaş olabilir. Asıl eğitim Kaggle'da yapılacak.
- Kamera hızı: s modellerinin GTX 1650'de ≥ 15 FPS'i büyük olasılıkla karşılaması, n'nin ise daha rahat karşılaması bekleniyor (**ölçülecek**).

## Gerçekçi hedef
Topluluk sonucuna göre tüm RDD2022'de s modelleriyle mAP50 yaklaşık 0,61. Tüm ülkeler için genel hedefimizde 0,55–0,60 makul bir aralık; baseline sonrası kesinleşecek. Japonya+Hindistan hedefi (≥ 0,547) aynı kalıyor.
