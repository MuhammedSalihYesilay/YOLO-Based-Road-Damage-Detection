# YOLO-Based Road Damage Detection

Yol görüntülerinden ve gerçek zamanlı videodan yol hasarlarını tespit edip sınıflandıran, derin öğrenme tabanlı bir sistem (bitirme projesi).
Herkese açık bir veri setiyle eğitilen YOLO modeli dört hasar türünü bulur: boyuna çatlak, enine çatlak, timsah çatlağı ve çukur. Model standart nesne tespiti metrikleriyle değerlendirilir.
Streamlit web arayüzünde görüntü, video ya da kamera girdisi verilir; tespit edilen hasarlar kutu, sınıf ve güven skoruyla gösterilir.

## Belgeler
- [Proje önerisi](docs/proje-onerisi.md)
- [Plan](docs/plan.md)
- [Kararlar](docs/kararlar.md)
- Araştırma: [Python sürümü](docs/arastirma/python-surumu.md), [YOLO modelleri](docs/arastirma/yolo-modelleri.md)
- Öğrenme: [Metrikler](docs/ogrenme/metrikler.md)

## Repoda olmayanlar
Veri seti ve referans proje boyut ve lisans nedeniyle repoya konmadı (`.gitignore`). Ayrıca indirilmeleri gerekir:

- **Veri seti (RDD2022, ~12,9 GB):** https://datasetninja.com/road-damage-detector/ adresinden Supervisely formatında indirilip `data/rdd2022/` altına açılır.
  Lisans CC BY-SA 4.0. Atıf: Arya, Maeda, Sekimoto vd., "RDD2022: A multi-national image dataset for automatic Road Damage Detection", 2022, [arXiv:2209.08538](https://arxiv.org/abs/2209.08538).
- **Referans proje (RoadDamageDetection):** https://github.com/oracl4/RoadDamageDetection adresinden indirilip `reference/RoadDamageDetection-main/` altına açılır. Sadece incelemek için kullanılıyor; LICENSE dosyası olmadığından kodu kopyalanmaz.
