"""
Model yükleme ve tahmin. Görüntü, Video ve Kamera sayfaları aynı fonksiyonları kullanır.

Sabit ayarlar (kararlar.md):
- Final model e5: YOLO26s, imgsz 1024 (2026-11-08).
- FP32 (quantize=32): GTX 1650'de FP16 bozuk sonuç veriyor, val mAP50 0,04 (2026-10-30).
  Not: Ultralytics 8.4.182'de eski `half=False` parametresi kullanımdan kalkıyor; yerine `quantize=32` (aynı anlam).
- Model bir kez çok düşük eşikle (0,05) çalıştırılır; kullanıcının eşiği sonra yalnızca kutuları süzer.
  Böylece kaydırıcı oynatılınca model yeniden çalışmaz, ekran anında güncellenir.
"""

import time
from pathlib import Path

import numpy as np
import streamlit as st
import torch
from ultralytics import YOLO

from core.classes import CLASS_CODES

ROOT = Path(__file__).resolve().parents[3]  # repo kökü (src/app/core/model.py → 3 üst klasör)
WEIGHTS = ROOT / "runs" / "kaggle" / "e5_yolo26s_1024" / "weights" / "best.pt"  # git dışı, yerelden
MODEL_NAME = "YOLO26s"  # arayüzde gösterilen ad
IMGSZ = 1024  # eğitimdeki boyut; değiştirilirse sonuçlar ölçtüğümüz değerlerle tutmaz
PRECISION = 32  # FP32; FP16 (16) GTX 1650'de bozuk
MIN_CONF = 0.05  # modelin döndürdüğü en düşük güven; arayüz eşiği bunun üstünde süzer
DEFAULT_CONF = 0.25  # varsayılan arayüz eşiği: val F1 eğrisinin tepesi 0,276 (e5, BoxF1_curve.png)


def pick_device():
    """GPU varsa "0" (ilk CUDA kartı), yoksa "cpu" döndürür."""
    return "0" if torch.cuda.is_available() else "cpu"


@st.cache_resource(show_spinner=False)
def load_model(weights=str(WEIGHTS)):
    """Modeli bir kez yükler ve bellekte tutar (st.cache_resource: her tıklamada yeniden yüklenmez).

    Yüklemeden hemen sonra boş bir görüntüyle bir tahmin yapılır (ısınma): ilk tahminde CUDA başlatılır ve
    bellek ayrılır; bu gecikme kullanıcının ilk görüntüsüne yansımasın.
    """
    model = YOLO(weights)
    dummy = np.zeros((IMGSZ, IMGSZ, 3), dtype=np.uint8)  # siyah görüntü
    model.predict(dummy, imgsz=IMGSZ, quantize=PRECISION, device=pick_device(), verbose=False)
    return model


def predict(model, rgb):
    """Bir RGB görüntüde tahmin yapar; (tespit listesi, süre ms) döndürür.

    Her tespit bir sözlük: {"code": "D40", "conf": 0.82, "box": (x1, y1, x2, y2)} (piksel, görüntü koordinatı).
    """
    bgr = np.ascontiguousarray(rgb[:, :, ::-1])  # RGB → BGR: Ultralytics numpy girdiyi OpenCV gibi BGR bekler
    t0 = time.perf_counter()
    result = model.predict(bgr, imgsz=IMGSZ, conf=MIN_CONF, quantize=PRECISION, device=pick_device(),
                           verbose=False)[0]
    ms = (time.perf_counter() - t0) * 1000  # ön işleme + çıkarım + son işleme toplam süre

    boxes = result.boxes
    detections = []
    for xyxy, conf, cls in zip(boxes.xyxy.tolist(), boxes.conf.tolist(), boxes.cls.tolist()):
        detections.append({
            "code": CLASS_CODES[int(cls)],  # sınıf numarası → D kodu (eğitim sırası)
            "conf": float(conf),
            "box": tuple(round(v) for v in xyxy),
        })
    return detections, ms


def filter_detections(detections, conf, codes):
    """Eşiğin altındaki ve seçilmemiş sınıflardaki tespitleri atar (model yeniden çalışmaz)."""
    return [d for d in detections if d["conf"] >= conf and d["code"] in codes]
