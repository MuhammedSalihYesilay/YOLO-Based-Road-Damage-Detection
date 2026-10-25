# Veri analizi özeti (Adım 1)

`src/analysis/analyze_dataset.py` ile üretildi. Sadece `train|test/ann/*.json` okundu.

## Doğrulama (beklenen = CLAUDE.md)

| index | expected | found | ok |
|---|---|---|---|
| images | 38385 | 38385 | OK |
| labels | 61082 | 61082 | OK |
| D00 | 26196 | 26196 | OK |
| D10 | 11875 | 11875 | OK |
| D20 | 10617 | 10617 | OK |
| D40 | 6544 | 6544 | OK |

## Ülkeler: görüntü sayısı ve boş oranı

| country | train_images | test_images | empty_before_pct | empty_after_pct |
|---|---|---|---|---|
| China_Drone | 2401 | 0 | 20.1 | 20.1 |
| China_MotorBike | 1977 | 500 | 2.2 | 2.2 |
| Czech | 2829 | 709 | 62.1 | 62.1 |
| India | 7706 | 1959 | 51.1 | 56.9 |
| Japan | 10506 | 2627 | 11.4 | 24.8 |
| Norway | 8161 | 2040 | 64.3 | 64.3 |
| United_States | 4805 | 1200 | 0.0 | 0.0 |
| TOPLAM | 38385 | 9035 | 33.0 | 37.8 |

## 640'a küçültülünce küçük kalan kutular

| country | boxes | median_short_640 | pct_under_8px | pct_under_16px |
|---|---|---|---|---|
| China_Drone | 3068 | 47.5 | 0.0 | 0.1 |
| China_MotorBike | 4650 | 65.0 | 0.3 | 3.9 |
| Czech | 1745 | 44.8 | 0.0 | 0.7 |
| India | 7056 | 69.3 | 0.0 | 0.7 |
| Japan | 16470 | 57.6 | 0.1 | 3.0 |
| Norway | 11229 | 15.8 | 23.5 | 50.6 |
| United_States | 11014 | 52.0 | 0.0 | 2.3 |
| TOPLAM | 55232 | 45.3 | 4.8 | 12.1 |

## Sınıf başına görüntü (site ile)

| class | images | site | diff |
|---|---|---|---|
| D00 | 13657 | 13657 | 0 |
| D10 | 7744 | 7744 | 0 |
| D20 | 8412 | 8412 | 0 |
| D40 | 3674 | 3674 | 0 |

## Kalite kontrolü

| check | count |
|---|---|
| Görüntü dışına taşan kutu | 0 |
| Sıfır genişlik/yükseklikli kutu | 1 |
| Görüntüsü olmayan etiket dosyası | 0 |
| Etiket dosyası olmayan görüntü | 0 |
| Dosya adı ile ülke etiketi farklı | 0 |

## China_Drone karşılaştırması

| index | China_Drone | Diğer (Drone hariç) |
|---|---|---|
| images | 2401.0 | 35984.0 |
| empty_after_pct | 20.1 | 39.0 |
| boxes_per_nonempty_image | 1.6 | 2.38 |
| median_area_pct | 2.45 | 1.36 |
| median_aspect | 1.09 | 1.27 |
| D00_pct | 46.5 | 47.5 |
| D10_pct | 41.2 | 20.3 |
| D20_pct | 9.6 | 19.8 |
| D40_pct | 2.8 | 12.4 |

## Bölme önizlemesi (seed 42)

| part | D00 | D10 | D20 | D40 | D00_pct | D10_pct | D20_pct | D40_pct | images | empty_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| train | 21095 | 9556 | 8499 | 5303 | 47.5 | 21.5 | 19.1 | 11.9 | 30709 | 37.8 |
| val | 2489 | 1102 | 1050 | 586 | 47.6 | 21.1 | 20.1 | 11.2 | 3838 | 37.9 |
| test | 2612 | 1217 | 1068 | 655 | 47.0 | 21.9 | 19.2 | 11.8 | 3838 | 37.8 |

## Sekans kontrolü (ardışık vs rastgele çift)

| country | pairs | consec_mean | random_mean | consec_pct_ge_0.5 | random_pct_ge_0.5 |
|---|---|---|---|---|---|
| China_Drone | 1532 | 0.015 | 0.012 | 0.3 | 0.1 |
| China_MotorBike | 1890 | 0.045 | 0.049 | 0.8 | 1.1 |
| Czech | 331 | 0.038 | 0.04 | 0.3 | 0.9 |
| India | 1122 | 0.057 | 0.06 | 1.2 | 1.1 |
| Japan | 4778 | 0.045 | 0.046 | 1.1 | 0.9 |
| Norway | 1065 | 0.027 | 0.028 | 0.3 | 0.3 |
| United_States | 4804 | 0.04 | 0.041 | 0.2 | 0.3 |
| TOPLAM | 15522 | 0.04 | 0.041 | 0.6 | 0.6 |

## Öne çıkan bulgular

1. **Norveç'te küçük nesne sorunu:** 640'a küçültülünce kısa kenarı 8 px altına düşen kutu oranı %23.5, 16 px altına düşen %50.6 (diğer ülkelerde 8 px altı en fazla %0.3). Norveç boyut kararının dayanağı.
2. **Sekans sızıntısı işareti yok:** ardışık çiftlerin ortalama benzerliği 0.04, rastgele çiftlerin 0.041. Rastgele katmanlı bölme yeterli görünüyor. Sınır: araç hareketiyle kutular kayıyorsa IoU bunu yakalayamayabilir; bu bir göstergedir, kanıt değil.
3. **`other corruption` atılınca boş oran artıyor:** Japonya %11.4 → %24.8, Hindistan %51.1 → %56.9, toplam %33.0 → %37.8.
4. **China_Drone farklı:** D10 payı %41.2 (diğerlerinde %20.3), D40 payı %2.8 (diğerlerinde %12.4).
5. **Bölme önizlemesi dengeli:** train/val/test sınıf oranları en fazla 1.0 puan farklı.
6. **Hatalı kutu:** 1 adet sıfır boyutlu kutu (`Japan_001265.jpg` (D20)); Adım 3'te atılacak.
