# Araştırma: Python sürümü (2026-10-15)

**Karar: Python 3.13** (yedek: 3.12)

## Bulgular
| Kontrol | Sonuç | Kaynak |
|---|---|---|
| Python 3.10 resmi desteği | **1 Ekim 2026'da sona erdi** (end-of-life). Artık güvenlik yaması da çıkmıyor. | [devguide](https://devguide.python.org/versions/) |
| Diğer sürümlerin destek bitişi | 3.11 → 2027-10, 3.12 → 2028-10, **3.13 → 2029-10**, 3.14 → 2030-10 | [devguide](https://devguide.python.org/versions/) |
| Colab | 3.12'den **3.13'e geçti** (Ağustos–Eylül 2026). Eski runtime seçilerek 3.12 kullanılabiliyor. | [colabtools #6081](https://github.com/googlecolab/colabtools/issues/6081), [Colab sürüm notları](https://colab.research.google.com/notebooks/relnotes.ipynb) |
| Kaggle | Kaggle imajı, Colab'ın 17.09.2026 imajı üzerine kurulu. Paket yolu `python3.13`, yani **3.13**. | [Kaggle docker-python Dockerfile](https://github.com/Kaggle/docker-python/blob/main/Dockerfile.tmpl) |
| torch 2.14.1 (30.09.2026) | Python 3.10–3.14 destekleniyor; Windows için cp313 wheel var | [PyPI torch](https://pypi.org/project/torch/) |
| ultralytics 8.4.177 | Python 3.8–3.14 | [PyPI ultralytics](https://pypi.org/project/ultralytics/) |
| opencv-python 5.0.0.93 | abi3 wheel: cp37 ve sonrası, yani 3.13 dahil | [PyPI opencv-python](https://pypi.org/project/opencv-python/) |
| streamlit 1.66.0 (14.10.2026) | **Python ≥ 3.11**; 3.10'u artık desteklemiyor | [PyPI streamlit](https://pypi.org/project/streamlit/) |
| streamlit-webrtc 0.78.1 | Python ≥ 3.10; aiortc ≥ 1.14 ve av ≥ 15.1 istiyor | [PyPI](https://pypi.org/project/streamlit-webrtc/), [pyproject](https://github.com/whitphx/streamlit-webrtc/blob/main/pyproject.toml) |
| aiortc 1.15.0 | Python 3.10–3.14, saf Python wheel. Geliştirme dalı ≥ 3.11'e çıktı. av < 20 istiyor. | [PyPI aiortc](https://pypi.org/project/aiortc/), [pyproject](https://github.com/aiortc/aiortc/blob/main/pyproject.toml) |
| av (PyAV) 19.0.1 | **Python ≥ 3.12**; Windows için cp312-abi3 wheel var (3.12, 3.13 ve sonrasında çalışır) | [PyPI av](https://pypi.org/project/av/) |

## Neden 3.13?
1. **Bulutla aynı sürüm:** Kaggle ve Colab 3.13 kullanıyor. Yerelde de 3.13 olursa "bende çalışıyor, Kaggle'da çalışmıyor" türü sorunlar azalır.
2. **Tüm paketler destekliyor.** Güncel `av` 3.12'nin altını, güncel `streamlit` ise 3.10'u artık desteklemiyor. 3.10'da kalırsak eski paket sürümleriyle yetinmek zorunda kalırız.
3. **Destek süresi:** 3.13 Ekim 2029'a kadar güvenlik yaması alacak; teslim Ocak 2027'de.
4. **Neden 3.14 değil?** Kaggle ve Colab henüz 3.14'e geçmedi; 3.14'ün yeni özellikleri (free-threading) bu projeye bir şey kazandırmıyor.
5. **Yedek 3.12:** 3.13'te bir paket sorun çıkarırsa 3.12'ye dönülür. Colab'da da 3.12 runtime'ı seçilebiliyor.

## Referans projeyle ilişki
- Referansın ortamına (Python 3.8, ultralytics 8.0.201) ihtiyacımız yok, çünkü karşılaştırmada referansın **raporladığı 0,547** kullanılıyor.
- **Mevcut durum:** Bilgisayardaki sistem Python'u 3.10.0; üzerinde `ultralytics 8.0.201` ve `torch 2.0.0+cpu` kurulu. Yani referans **CPU'da** çalıştırılmış, GPU kullanılmamış. Bu ortama dokunulmayacak, yedek olarak kalacak.
- **Hazır model (`YOLOv8_Small_RDD.pt`) güncel ultralytics'te açılır mı?** Paket kurulumu yapılmadığı için henüz test edilmedi. Kaynaklara göre yeni ultralytics, eski sürümde eğitilmiş modelleri genelde açabiliyor; sorunlar daha çok tersi yönde ve eski import yollarında çıkıyor ([#2587](https://github.com/ultralytics/ultralytics/issues/2587), [#1142](https://github.com/ultralytics/ultralytics/issues/1142)).
  - Adım 0'da yeni venv'de `YOLO("...pt").predict(örnek_görüntü)` ile test edilecek.
  - Açılmazsa yedek yol: mevcut sistem Python'unda (8.0.201) model ONNX'e dönüştürülür ve yeni ortamda `YOLO("model.onnx")` ile yüklenir. Referans klasörü değiştirilmez; çıktı `models/` altına yazılır.
  - Bu model yalnızca arayüz testinde kullanılacağı için kritik değil.

## Ek bulgu: GPU sürücüsü güncellenmeli
- Kurulu NVIDIA sürücüsü **512.74** (CUDA 11.x dönemine ait). torch 2.14 yalnızca CUDA 12.6 / 13.0 / 13.2 derlemeleri sunuyor; bunlar için sürücü sırasıyla ≥ 525 ve ≥ 580 olmalı ([CUDA 13.0 notları](https://docs.nvidia.com/cuda/archive/13.0.0/cuda-toolkit-release-notes/), [PyTorch RELEASE.md](https://github.com/pytorch/pytorch/blob/main/RELEASE.md)).
- GTX 1650 (Turing, sm_75) torch 2.14'te ve 2.15'te destekleniyor ([PyTorch duyurusu](https://dev-discuss.pytorch.org/t/notice-cuda-12-6-wheels-will-no-longer-be-published-from-pytorch-2-15-drops-maxwell-pascal-volta/3432)).
- Adım 0'da sürücü güncellenecek ve torch CUDA 13.0 derlemesiyle kurulacak. Kamera hızını ölçmek için bu gerekli.

## Doğrulama (Adım 0'da)
`python --version` → 3.13.x; `torch.cuda.is_available()` → True; hazır model bir test görüntüsünde tahmin üretmeli.
