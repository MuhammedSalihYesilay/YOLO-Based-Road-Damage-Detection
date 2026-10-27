# Adım 3: YOLO formatına dönüştürme ve bölme (2026-10-27)

## Ne yaptık, neden
RDD2022'nin etiketli 38.385 train görüntüsünü (Supervisely JSON) YOLO'nun okuduğu formata çevirdik ve
%80 train / %10 val / %10 test olarak böldük. Uygulanan kararlar (Norveç 1280, boşlar train'de %10,
ülke + boş/dolu katmanlı bölme, seed 42, bozuk kutu) burada tekrar yazılmadı:
[kararlar.md → 2026-10-27 Adım 2 veri kararları](../kararlar.md#2026-10-27--adım-2-veri-kararları)
ve aynı tarihli "Adım 3 uygulama notları".

Orijinal veriye (`data/rdd2022/`) hiçbir şey yazılmaz. Diğer ülkelerin görüntüleri hardlink'tir
(kopya değil, aynı dosyaya ikinci isim; yer kaplamaz). Bu yüzden `data/yolo/images` içindeki dosyaları
düzenlemeyin; düzenleme orijinali de değiştirir. Norveç görüntüleri küçültülüp yeni dosya olarak yazılır.

## Tekrar üretme
Ön koşul: venv kurulu (`requirements.txt`), veri `data/rdd2022/train/{ann,img}` altında.

```powershell
# 1) Dönüştür + böl (en uzun kısım Norveç küçültmesi). data/yolo varsa script durur.
.\venv\Scripts\python.exe src\data\prepare_yolo.py --data-root data/rdd2022 --out data/yolo --seed 42 --workers 4

# 2) 20 rastgele görüntüyü (4'ü Norveç) YOLO etiketlerinden kutularıyla çiz → data/yolo_check/
.\venv\Scripts\python.exe src\data\draw_samples.py --yolo data/yolo --out data/yolo_check --n 20 --n-norway 4 --seed 42

# 3) Smoke test listeleri (2.000 train / 400 val, ülke + boş/dolu oranlı)
.\venv\Scripts\python.exe src\data\make_smoke_lists.py --yolo data/yolo --n-train 2000 --n-val 400 --seed 42

# 4) Smoke test eğitimi (hattın uçtan uca çalıştığını görmek için; sonuç önemli değil)
.\venv\Scripts\yolo.exe detect train model=yolov8n.pt data=data/yolo/data_smoke.yaml imgsz=640 epochs=3 batch=8 workers=2 cache=False project=runs/smoke name=v8n
```

Aynı seed ile aynı bölme çıkar; sayılar aşağıdaki tabloyla birebir tutmalı.

## Script'ler (`src/data/`)
| Script | Ne yapar |
|---|---|
| `prepare_yolo.py` | JSON'ları okur (`read_annotations`), kutuları YOLO satırına çevirir (`to_yolo_lines`), katmanlı böler (`split_images`), train'deki boşları %10'a indirir (`reduce_empty`), görüntü/etiketleri yazar (`write_dataset`), listeleri ve `data.yaml`'ı yazar, özet basar. Norveç görüntüsünün okunan boyutu JSON'dakiyle tutmazsa listeyi basıp hata ile durur. |
| `draw_samples.py` | Kutuları JSON'dan değil yazılan YOLO txt'lerinden çizer; dönüştürme hatası varsa gözle görülür. |
| `make_smoke_lists.py` | Küçük ama temsilî listeler + `data_smoke.yaml`. Ultralytics'in `fraction` ayarı kullanılmadı: listenin başını aldığı için neredeyse hepsi China_Drone olurdu. |

## Çıktılar (`data/yolo/`, git dışı)
| Dosya | İşe yarar |
|---|---|
| `images/{train,val,test}/` | Görüntüler (hardlink; Norveç 1280x717 yeni dosya) |
| `labels/{train,val,test}/*.txt` | Her satır `sınıf cx cy w h` (0-1 oran). Boş görüntü = boş txt |
| `train.txt`, `val.txt`, `test.txt` | Eğitimde kullanılacak görüntü listeleri; `data.yaml` bunları gösterir |
| `train_dropped_empty.txt` | Kenara konan 9.498 boş train görüntüsü (dosyaları duruyor, `train.txt`'te yok) |
| `split.csv` | Her görüntü: ülke, parça, boş mu, kullanılıyor mu |
| `data.yaml` | Sınıflar 0: D00, 1: D10, 2: D20, 3: D40; `path` yok, yaml'ın klasörü kullanılır (Kaggle'a taşınabilir) |
| `smoke_train.txt`, `smoke_val.txt`, `data_smoke.yaml` | Smoke test |
| `labels/*.cache` | Ultralytics'in etiket taraması önbelleği (eğitim oluşturur; Kaggle'a yüklenmez) |

## Sonuç
| Parça | Görüntü | Etiket | D00 % | D10 % | D20 % | D40 % | Boş % |
|---|---|---|---|---|---|---|---|
| train | 21.211 | 44.453 | 47,5 | 21,5 | 19,1 | 11,9 | 10,0 |
| val | 3.838 | 5.227 | 47,6 | 21,1 | 20,1 | 11,2 | 37,9 |
| test | 3.838 | 5.551 | 47,1 | 21,9 | 19,2 | 11,8 | 37,8 |

- Toplam 55.231 etiket (55.232 − 1 sıfır boyutlu kutu, `Japan_001265.jpg`).
- Bölme Adım 1 önizlemesiyle aynı (30.709 / 3.838 / 3.838; train'den 9.498 boş kenara kondu).
- Norveç'te boyut uyuşmazlığı çıkmadı. 20 örnek gözle kontrol edildi: kutular doğru yerde;
  bazı Norveç kutuları gevşek ama bu orijinal etiketten.

## Karşılaşılan sorunlar
1. **pandas `df.empty` tuzağı:** "boş görüntü mü" sütununa `empty` adı verilmişti. `images.empty` sütunu değil,
   pandas'ın "tablo boş mu?" özelliğini (tek bir False) döndürdü: bölmede her görüntü "dolu" sayıldı,
   boş azaltma hiç çalışmadı. Script özet aşamasında çöktü. Çözüm: sütun adı `is_empty`; hatalı `data/yolo` silinip
   yeniden üretildi. Ders: sütunlara pandas'ın kendi özellik isimlerini (`empty`, `size`, `shape`...) vermeyin.
2. **`.gitignore`:** `data/` satırı `src/data/` klasörünü de dışarıda bırakıyordu, script'ler git'e girmiyordu.
   `/data/` yapıldı: artık sadece kökteki veri klasörü git dışı.

## Smoke test (yerel, GTX 1650)
YOLOv8n, imgsz 640, 3 epoch, batch 8, workers 2, cache kapalı → hatasız, bozuk etiket yok.
Epoch başına ~55 sn (toplam ~3 dk, val dahil), GPU belleği 2,03 GB, çıkarım 5,7 ms/görüntü.

| Epoch | box_loss | cls_loss | dfl_loss | val mAP50 |
|---|---|---|---|---|
| 1 | 2,58 | 5,46 | 2,34 | 0,041 |
| 2 | 2,44 | 3,32 | 2,26 | 0,066 |
| 3 | 2,29 | 2,99 | 2,13 | 0,119 |

Uyarılar:
- **AMP:** Ultralytics GTX 1650'de karışık hassasiyetli (FP16) eğitimi kendisi kapattı (bu kartta NaN riski). NaN çıkmadı. Kaggle T4'te AMP açık kalır.
- **Çıktı yolu:** `project=runs/smoke` verilince sonuç `runs/detect/runs/smoke/v8n/` altına yazıldı (Ultralytics 8.4 başa `runs/detect` ekliyor). Yine `runs/` altında, git dışı.
- **`.cache` dosyaları:** eğitim `data/yolo/labels/` içine `train.cache`, `val.cache` yazdı (yeni dosya, hardlink değil).
- **"Slow image access":** okuma 14-20 MB/s ölçüldü; muhtemelen ilk okuma/antivirüs. Smoke testi etkilemedi.
- `yolov8n.pt` proje köküne indi (`*.pt` git dışı).

## Hocaya nasıl anlatırız
"38 bin etiketli görüntüyü YOLO formatına çevirip ülke ve boş/dolu oranını koruyarak %80/10/10 böldük; her parçada
sınıf oranları en fazla 1 puan farklı. Dönüştürmeyi 20 örneği kutularıyla çizerek doğruladık, küçük bir deneme
eğitimiyle de verinin modele uçtan uca aktığını gösterdik."
