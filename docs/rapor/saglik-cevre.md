# Effects on Health, Environment and the Problems of the Age — Taslak (ara rapor)

> **Durum:** Taslak; Word raporuna henüz eklenmedi. Şablon: "Realistic Constraints and Conditions → Effects on Health,
> Environment and the Problems of the Age Reflected in the Field of Engineering (midterm)", en az 1000 karakter
> (hedef 1200–1500). Şablon açıklaması: "Discuss the impact of your project on health, environment and safety in
> universal and social dimensions and the problems of the age reflected in the field of engineering."
> Her iddia resmî / birincil kaynakta doğrulandı (sondaki Kaynak Kontrol Tablosu); sistemimizin olmayan bir etkisi
> iddia edilmiyor. Kaynak stili IEEE; numaralar **geçici**: [1]–[19] literatür, [20]–[28] standartlar, [29]–[37]
> yasal, yeni kaynaklar [38]–[40].
> Bu dosyanın iki kopyası var ve her zaman aynı olmalı: `docs/rapor/ozel/saglik-cevre.md` (git dışı) ve
> `docs/rapor/saglik-cevre.md` (git'te). Türkçe açıklama: `docs/rapor/ozel/saglik-cevre-turkce.md`.

<!-- HEALTH-START -->
### Effects on Health, Environment and the Problems of the Age Reflected in the Field of Engineering

**Safety and health.** Road crashes kill about 1.16 million people each year, and pedestrians, cyclists and motorcyclists account for over half of these deaths [38]. According to WHO, the way a road is built has a large effect on how safe it is [38]. This project does not claim to prevent crashes; it only helps find damage earlier.

**Economic and environmental effects.** The state of the road surface changes how much drivers spend on fuel, tires and vehicle repairs [39]. Repairing a road before its condition becomes poor slows its decline and keeps it in use longer at a reasonable cost [40]. Our work also has an energy cost: the total training of the seven experiments took about 46 GPU hours.

**Social dimension and problems of the age.** Checking roads by eye depends on trained people and takes much time and money. Where such people and funds are scarce, roads are checked less often and aging roads become more dangerous, a problem Maeda et al. expect in many countries [1]. Cameras mounted on vehicles combined with automatic detection could let municipalities survey wide road networks cheaply and fast [4]; our final model runs at about 25 FPS on a GTX 1650 GPU.

**Safe use.** The real-time camera mode is meant to be used with a fixed mount or by a passenger, so that the driver is not distracted.
<!-- HEALTH-END -->

## REFERENCES (yeni kaynaklar; [1] ve [4] literatür taramasında)

[38] World Health Organization, "Road traffic injuries," Fact sheet, Jul. 20, 2026. [Online]. Available: https://www.who.int/news-room/fact-sheets/detail/road-traffic-injuries (accessed Nov. 12, 2026).

[39] K. Chatti and I. Zaabar, *Estimating the Effects of Pavement Condition on Vehicle Operating Costs*, NCHRP Report 720. Washington, DC, USA: Transportation Research Board, 2012, doi: 10.17226/22808.

[40] Federal Highway Administration, "Pavement preservation," U.S. Department of Transportation, updated Oct. 5, 2023. [Online]. Available: https://www.fhwa.dot.gov/pavement/preservation/ (accessed Nov. 12, 2026).
<!-- REF-END -->

---

## Kaynak Kontrol Tablosu

Not: WHO'nun 2023 raporu (*Global status report on road safety 2023*, ISBN 978-92-4-008651-7; "1.19 million") daha
güncel bilgi notuyla (2026, "Approximately 1.16 million") çeliştiği için kaynakçaya alınmadı (kullanıcı kararı); metinde
yalnız bilgi notu var. NCHRP 720 künyesi Crossref'ten (`https://api.crossref.org/works/10.17226/22808`), özet
cümlesi NAP sayfasından. Maeda [1] ve RDD2022 [4] alıntıları arXiv PDF'lerinden çıkarılan metinden (pypdf). Washington,
DC konumu doğrulanmadı (TRB'nin bilinen adresi); istenirse künyeden çıkarılabilir.

| # | Kaynak | Link | Metindeki iddia | Kaynaktan birebir kısa alıntı | Durum |
|---|---|---|---|---|---|
| 38 | WHO, "Road traffic injuries" bilgi notu, 20 Temmuz 2026 | https://www.who.int/news-room/fact-sheets/detail/road-traffic-injuries | Her yıl ~1,16 milyon ölüm; yarıdan fazlası savunmasız yol kullanıcıları; yol tasarımı güvenliği güçlü biçimde etkiliyor | "Approximately 1.16 million people die each year as a result of road traffic crashes." · "More than half of all road traffic deaths are among vulnerable road users, including pedestrians, cyclists and motorcyclists." · "Unsafe road infrastructure" başlığı altında: "The design of roads can have a considerable impact on their safety." | Doğru. Bakım (maintenance) hakkında cümle yok → çukur–kaza nedenselliği yazılmadı |
| 39 | Chatti, Zaabar, NCHRP Report 720, TRB, 2012, doi 10.17226/22808 | https://nap.nationalacademies.org/catalog/22808 · https://doi.org/10.17226/22808 | Kaplama durumu araç işletme maliyetini etkiliyor: yakıt, lastik aşınması, onarım ve bakım | "presents models for estimating the effects of pavement condition on vehicle operating costs. The models address fuel consumption, tire wear, and repair and maintenance costs" · Crossref: yazarlar Karim Chatti, Imen Zaabar; yayıncı Transportation Research Board; 2012-07-27 | Doğru. Yön ve sayı alıntıda yok → metinde yalnız "affects" |
| 40 | FHWA, "Pavement Preservation" (güncelleme 05.10.2023) | https://www.fhwa.dot.gov/pavement/preservation/ | Kaplama henüz iyi durumdayken yapılan bakım bozulmayı yavaşlatır, ömrü maliyet açısından etkin biçimde uzatır | "keeping good roads good" · "Constructing quality pavement preservation treatments when the pavement condition is still satisfactory" … "can impede deterioration, extend service life, and improve functionality in a cost-effective manner" | Doğru. Çevre faydası (malzeme/enerji/emisyon) sayfada yok → yazılmadı |
| 1 | Maeda vd. 2018, arXiv:1801.09454 PDF, §1 Introduction ve §2.1 | https://arxiv.org/pdf/1801.09454 | Elle denetim deneyimli personel ister, yavaş ve pahalı; uzman ve bütçe eksikliği denetimi seyrekleştiriyor, yaşlanan altyapının riskini artırıyor; sorun dünya genelinde | §2.1: "the visual inspection approach not only requires experienced road managers, but also is time-consuming and expensive" · "which increases the risk associated with aging road infrastructure" · "municipalities lacking the required resources do not conduct infrastructure inspections appropriately and frequently" · §1: "a shortage of field technicians (experts) and financial resources has resulted in many areas" · "The United States also has similar infrastructure aging problems" · "likely to be experienced by countries all over the world" | Doğru ("aging" birebir alıntıyla) |
| 4 | RDD2022, arXiv:2209.08538 PDF | https://arxiv.org/pdf/2209.08538 | Otomatik tespit belediyelere düşük maliyetli, geniş alanda hızlı denetim | "valuable for municipalities and road organizations for low-cost inspection of road conditions" · "providing support for a quick inspection of a large area" | Doğru |
| — | Kendi verimiz | `docs/deneyler.md`, `docs/model-secimi.md`, kararlar.md 2026-11-08 | 7 deneyin toplam eğitimi ≈ 46 GPU saati; final model GTX 1650'de ~25 FPS | Eğitim döngüleri: baseline 4 sa 34 dk, e2 5 sa 55 dk, e3 7 sa 5 dk, e4 4 sa 33 dk, e5 12 sa 55 dk, e6 5 sa 5 dk, e7 6 sa 7 dk → toplam 2.774 dk = 46 sa 14 dk · e5 GTX 1650 25,0 FPS | Doğru (deneme koşuları ve Kaggle kurulum süreleri dahil değil) |
| — | Kaynaksız tasarım kararı | — | Kamera modu sabit montaj ya da yolcu tarafından kullanılacak | — | Kendi kararımız (kullanıcı onayı) |

## Doğrulanamayanlar / çıkarılanlar

| Konu | Durum |
|---|---|
| Motosiklet/bisiklet için yüzey hasarı riski (WHO PTW el kitabı) | Kullanıcı kararıyla çıkarıldı; "vulnerable road users" ifadesi yeterli |
| Erken bakımın çevre faydası (malzeme, atık, emisyon) | highways.dot.gov 403, FHWA-HIF-15-002 404; doğrulanamadı → metinde yok |
| Çukur / bakım eksikliği ile kaza arasında nedensellik | WHO sayfalarında bakımla ilgili cümle yok → yazılmadı |
| WHO 2023 raporu (1,19 milyon) | Bilgi notuyla çelişiyor; kaynakçaya alınmadı (kullanıcı kararı) |
| SDG hedefleri (3.6, 11.2) | SDG bölümüne bırakıldı (kullanıcı kararı) |
| Eğitimin CO₂ değeri | Doğrulanmış bir hesap yok → yalnız GPU saati |

## Neden böyle yazıldı (sunumda nasıl anlatılır)

- **Şablonun dört isteği:** sağlık ve güvenlik (Safety and health), çevre (Economic and environmental effects),
  evrensel ve toplumsal boyut (WHO'nun dünya verisi; belediyeler; "countries all over the world"), mühendislik alanına
  yansıyan çağın sorunu (yaşlanan altyapı, uzman ve bütçe eksikliği). Her konu 1–2 cümle.
- **İddia sınırı:** Sistemimizin etkisi yalnız "hasarı daha erken bulmaya yardım"; "kazaları azaltır" denmiyor ve
  bu açıkça yazıldı. WHO yol tasarımından söz ediyor, bakımdan değil; bu yüzden çukur–kaza bağı kurulmadı.
- **Kendi cümlelerimiz (2026-11-12 düzeltmesi):** İlk taslakta bazı cümleler kaynağa çok yakındı (WHO "more than half …
  vulnerable road users" ve "design of roads … impact on their safety"; NCHRP "fuel consumption, tire wear, and repair
  and maintenance"; FHWA "still satisfactory … deterioration … service life … cost-effective"; Maeda "increases the
  risk … aging road infrastructure"; RDD2022 "low-cost … quick inspection of a large area"). Hepsi anlam aynı kalacak
  şekilde farklı yapı ve kelimelerle yeniden yazıldı (literatürdeki kural). Alıntılar tabloda kayıt olarak duruyor.
- **Sayılar:** Yalnız kaynakta birebir geçenler (1,16 milyon, "more than half") ve kendi ölçümlerimiz (46 sa, 25 FPS).
- **Dürüstlük:** Projenin kendi enerji maliyeti (yedi deneyin toplam eğitimi ≈ 46 GPU saati) yazıldı. "Bu yüzden
  deney sayısını sınırladık" denmedi: birleşik modelin eğitilmemesinin asıl gerekçesi 1 puan kuralıydı
  (kararlar.md 2026-11-08), enerji değil; 1500 karakter sınırı için de cümle kısaltıldı.
- **Güvenli kullanım:** Kaynaksız tasarım kararımız (sabit montaj ya da yolcu).
- *Anlatım:* "Trafik kazalarında her yıl 1,16 milyon kişi ölüyor; yol tasarımı ve altyapı güvenliği etkiliyor. Biz kaza
  azaltma iddiasında bulunmuyoruz, hasarın erken bulunmasına yardım ediyoruz. Kaplama durumu yakıt, lastik ve onarım
  maliyetini etkiliyor; erken bakım yolun ömrünü uzatıyor. Elle denetim yavaş ve pahalı, uzman ve bütçe eksikliği
  yaşlanan altyapıda risk yaratıyor; otomatik tespit belediyelere ucuz ve hızlı denetim sağlayabilir. Bunun bizim
  tarafımızda da bir enerji maliyeti var: yedi deneyin toplam eğitimi yaklaşık 46 saat GPU."
