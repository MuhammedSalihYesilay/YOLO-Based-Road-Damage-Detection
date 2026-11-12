# Standards to be Used — Taslak (ara rapor)

> **Durum:** Taslak; Word raporuna henüz eklenmedi. Şablon: "Standards to be Used (midterm)", en az 1000 karakter
> (hedef 1200–1500). Her standart resmî / birincil kaynakta doğrulandı (sondaki Kaynak Kontrol Tablosu). Kaynak stili
> IEEE. Numaralar **geçici**: [1]–[19] literatür taramasında (`literatur-taramasi.md`), yeni kaynaklar [20]–[28];
> rapor birleştirilirken yeniden sıralanacak.
> Bu dosyanın iki kopyası var ve her zaman aynı olmalı: `docs/rapor/ozel/standartlar.md` (git dışı) ve
> `docs/rapor/standartlar.md` (git'te). Türkçe açıklama: `docs/rapor/ozel/standartlar-turkce.md`.

<!-- STD-START -->
## STANDARDS TO BE USED

**Requirements and quality.** The functional and non-functional requirements of the system are written in the Use Case Model section of this report according to ISO/IEC/IEEE 29148:2018 [20], which describes what a well-formed requirement looks like. Quality targets such as detection accuracy and frame rate will be expressed with the product quality model of ISO/IEC 25010:2023 [21], which divides product quality into nine characteristics.

**Testing.** The system tests planned for the final term will follow ISO/IEC/IEEE 29119-1:2021 [22] for general testing concepts and ISO/IEC/IEEE 29119-3:2021 [23] for test documentation.

**Modeling.** The use case and class diagrams in this report are drawn in UML 2.5.1 [24].

**Road damage.** Our four damage classes follow the labeling scheme of RDD2022 [4]; these categories were first defined according to a Japanese road maintenance guidebook and were not taken from ASTM D6433-24 [25]. ASTM D6433 also judges pavement condition from damage that inspectors can see on the surface, which is the same kind of damage our model detects. This project does not compute a Pavement Condition Index (PCI).

**Evaluation and code.** Detection accuracy is reported with the metrics of the COCO evaluation [10], [26]: mAP50, which COCO also calls the PASCAL VOC metric, and mAP50-95. The Python code is written following PEP 8 conventions [27], and the references follow the IEEE reference style [28].
<!-- STD-END -->

## REFERENCES (yeni kaynaklar; [4] ve [10] literatür taramasında)

[20] *Systems and Software Engineering — Life Cycle Processes — Requirements Engineering*, ISO/IEC/IEEE 29148:2018, ISO/IEC/IEEE, Nov. 2018. [Online]. Available: https://standards.ieee.org/ieee/29148/6937/

[21] *Systems and Software Engineering — Systems and Software Quality Requirements and Evaluation (SQuaRE) — Product Quality Model*, ISO/IEC 25010:2023, ISO/IEC, Nov. 2023. [Online]. Available: https://www.iso.org/standard/78176.html

[22] *Software and Systems Engineering — Software Testing — Part 1: General Concepts*, ISO/IEC/IEEE 29119-1:2021, ISO/IEC/IEEE, Jan. 2022. [Online]. Available: https://standards.ieee.org/ieee/29119-1/10779/

[23] *Software and Systems Engineering — Software Testing — Part 3: Test Documentation*, ISO/IEC/IEEE 29119-3:2021, ISO/IEC/IEEE, Oct. 2021. [Online]. Available: https://standards.ieee.org/ieee/29119-3/7499/

[24] *OMG Unified Modeling Language (OMG UML)*, Version 2.5.1, OMG Document formal/17-12-05, Object Management Group, Dec. 2017. [Online]. Available: https://www.omg.org/spec/UML/2.5.1

[25] *Standard Practice for Roads and Parking Lots Pavement Condition Index Surveys*, ASTM D6433-24, ASTM International, 2024. [Online]. Available: https://store.astm.org/d6433-24.html

[26] COCO, "Detection evaluation," COCO dataset website. [Online]. Available: https://cocodataset.org/#detection-eval (accessed Nov. 11, 2026).

[27] G. van Rossum, B. Warsaw, and A. Coghlan, "PEP 8 – Style guide for Python code," Python Enhancement Proposal 8, 2001. [Online]. Available: https://peps.python.org/pep-0008/ (accessed Nov. 11, 2026).

[28] IEEE, "IEEE reference style guide for authors," V 3.28.2025, 2025. [Online]. Available: https://journals.ieeeauthorcenter.ieee.org/your-role-in-article-production/ieee-editorial-style-manual/ (accessed Nov. 11, 2026).
<!-- REF-END -->

---

## Kaynak Kontrol Tablosu

Not: iso.org ve IEC webstore otomatik erişime 403/404 verdi. ISO/IEC/IEEE ortak standartları IEEE SA sayfasından
(ortak yayıncı), ISO/IEC 25010 kullanıcı tarafından iso.org'da elle doğrulandı (2026-11-11). Kaynakçadaki standart
biçimi [28]'deki "Title of Standard, Standard number, Corporate author, location, date." kalıbına göre; konum (ör.
Cenevre) resmî sayfalarda doğrulanmadığı için yazılmadı.

| # | Kaynak | Link | Metindeki iddia | Kaynaktan birebir kısa alıntı (İngilizce) | Durum |
|---|---|---|---|---|---|
| 20 | ISO/IEC/IEEE 29148:2018, Requirements engineering (yayın 2018-11-30, aktif; 29148-2011'in yerini aldı) | https://standards.ieee.org/ieee/29148/6937/ | Gereksinimler bu raporun Use Case bölümünde buna göre yazılıyor; iyi bir gereksinimin yapısını tanımlıyor | "contains provisions for the processes and products related to the engineering of requirements" · "It defines the construct of a good requirement, provides attributes and characteristics of requirements" | Doğru (IEEE SA) |
| 21 | ISO/IEC 25010:2023, SQuaRE — Product quality model (Edition 2, yayın 2023-11) | https://www.iso.org/standard/78176.html | Kalite hedefleri bu modelle ifade edilecek; dokuz özellik | "The product quality model is composed of nine characteristics (which are further subdivided into subcharacteristics) that relate to quality properties of the products." | Doğru (kullanıcı iso.org'da elle doğruladı, 2026-11-11). Özelliklerin adları doğrulanmadı → metinde adla geçmiyor |
| 22 | ISO/IEC/IEEE 29119-1:2021, Software testing — Part 1: General concepts (yayın 2022-01-27, aktif) | https://standards.ieee.org/ieee/29119-1/10779/ | Final dönem testleri: genel test kavramları | "This document specifies general concepts in software testing and presents key concepts for the ISO/IEC/IEEE 29119 series." | Doğru (IEEE SA). Numaradaki yıl 2021, yayın 2022 |
| 23 | ISO/IEC/IEEE 29119-3:2021, Software testing — Part 3: Test documentation (yayın 2021-10-28, aktif) | https://standards.ieee.org/ieee/29119-3/7499/ | Test belgeleri buna göre | "ISO/IEC/IEEE 29119-3 includes templates and examples of test documentation." | Doğru (IEEE SA) |
| 24 | OMG UML 2.5.1, formal/17-12-05, Ara 2017 (listelenen en güncel sürüm) | https://www.omg.org/spec/UML/2.5.1 | Use case ve class diyagramları UML 2.5.1 ile | "A specification defining a graphical language for visualizing, specifying, constructing, and documenting the artifacts" | Doğru |
| 25 | ASTM D6433-24, Standard Practice for Roads and Parking Lots Pavement Condition Index Surveys (aktif; sayfa son güncelleme 15 Kas 2024) | https://store.astm.org/d6433-24.html · https://store.astm.org/d6433-23.html | Sınıflar ASTM'den alınmadı; ASTM D6433 görsel denetimle gözlenen yüzey hasarına dayanıyor, modelin bulduğu hasar da bu türden (görünür yüzey hasarı); PCI hesaplamıyoruz | D6433-24: "This practice covers the determination of roads and parking lots pavement condition through visual surveys" · D6433-23 §4.1: "based on the distress observed on the surface of the pavement" | Doğru. Sayfada hasar türü listesi yok → ASTM'nin hasar adları metne konmadı |
| 4 | RDD2022 (Arya vd.), arXiv:2209.08538 PDF, s. 2 | https://arxiv.org/pdf/2209.08538 | Sınıflarımız RDD2022'nin etiketleme şemasını izliyor; kategoriler ilk olarak Japon kılavuzuna göre tanımlandı (RDD2018/2019); RDD2020'den itibaren birden fazla ülkenin standartları dikkate alındı ve 4 kategori kaldı | "Since RDD2018 and RDD2019 captured the data from a single country, the damage categories defined in the Japanese Road Maintenance and Repair Guidebook 2013 [7] were used." · "in RDD2020, the involvement of multiple countries required considering multiple road damage standards" · "the following four damage categories – Longitudinal Cracks (D00), Transverse Cracks (D10), Alligator Cracks (D20), and Potholes (D40), were included" | Doğru. PDF metninde "ASTM", "pavement condition" geçmiyor (arandı) |
| (1) | Maeda vd. 2018, arXiv:1801.09454, Table 1 (destekleyici; metinde atıf yok) | https://arxiv.org/pdf/1801.09454 | Kılavuzun yayıncısı | "Source: Road Maintenance and Repair Guidebook 2013 JRA (2013) in Japan." · kaynakça: "JRA (2013). Maintenance and repair guide book of the pavement 2013. Japan Road Association" | Doğru |
| (2) | RDD2020 (Arya vd.), Data in Brief, Section 2 (destekleyici; metinde atıf yok) | https://pmc.ncbi.nlm.nih.gov/articles/PMC8166755/ | Aynı bilgi | "The damage categories for annotating Japanese data are defined using the Japanese Road Maintenance and Repair Guidebook 2013." | Doğru |
| 26 | COCO "Detection evaluation" sayfası (cocodataset.org; sayfa JavaScript ile yüklendiği için sitenin GitHub kaynağından okundu) | https://cocodataset.org/#detection-eval · https://raw.githubusercontent.com/cocodataset/cocodataset.github.io/master/dataset/detection-eval.htm | mAP50 (= PASCAL VOC metriği) ve mAP50-95 | "AP at IoU=.50:.05:.95 (primary challenge metric)" · "AP at IoU=.50 (PASCAL VOC metric)" | Doğru |
| 27 | PEP 8 – Style Guide for Python Code (van Rossum, Warsaw, Coghlan; 05-Jul-2001; Active) | https://peps.python.org/pep-0008/ | Kod stili | "This document gives coding conventions for the Python code comprising the standard library" | Doğru |
| 28 | IEEE Reference Style Guide for Authors, V 3.28.2025 (IEEE Editorial Style Manual sayfasındaki resmî bağlantı, Google Doc) | https://journals.ieeeauthorcenter.ieee.org/your-role-in-article-production/ieee-editorial-style-manual/ | Kaynakça IEEE stilinde; standart künyesi biçimi | "Title of Standard, Standard number, Corporate author, location, date." | Doğru |

## Doğrulanamayanlar / çıkarılanlar

| Kaynak | Neden konmadı |
|---|---|
| ISO/IEC 19505-1/-2:2012 (UML'in ISO sürümü) | iso.org ve IEC webstore 403/404; UML için doğrulanmış OMG 2.5.1 yeterli (kullanıcı kararı) |
| PASCAL VOC makalesi (Everingham vd., IJCV 88(2):303–338, 2010) | Künye Crossref'te doğru, ama makale metni açılamadı (sunucu bağlantıyı reddetti, Springer giriş istiyor). COCO sayfası AP50'yi "PASCAL VOC metric" diye tanımladığı için ayrı kaynak eklenmedi (kullanıcı kararı) |
| ASTM D6433'ün hasar türü listesi (alligator, longitudinal/transverse cracking, pothole …) | Resmî sayfada liste yok; standardın tam metni ücretli. Bu yüzden metinde sınıf eşlemesi yok; yalnız "görsel denetimle gözlenen yüzey hasarı" ortak noktası |
| ISO/IEC 25010'un dokuz özelliğinin adları | Kullanıcının doğruladığı alıntıda adlar yok; metinde yalnız "nine characteristics" |
| Japon kılavuzunun kendisi (JRA 2013) | Japonca, ücretli basılı kılavuz; ayrı kaynak yerine RDD2022 [4] üzerinden atıf |

## Neden böyle yazıldı (sunumda nasıl anlatılır)

- **Kısa ve tek kalıp:** Şablon yalnız "kullanmayı planladığınız standartları açıklayın" diyor; her standart için ne
  olduğu + projede nerede kullanıldığı (1–2 cümle). Metin 1200–1500 karakter hedefinde.
- **Zaman kipi dürüst:** Bu raporda yapılanlar şimdiki zamanla: gereksinimler (29148, Use Case bölümünde "The system
  shall ..." biçiminde), UML diyagramları, COCO metrikleri, PEP 8, IEEE stili. Kalite (25010) ve test (29119) için
  "will be expressed / will follow": testler final döneminde yapılacak.
- **ASTM dikkatle:** RDD2022 makalesine göre Japon kılavuzunun kategorileri RDD2018/2019'da kullanıldı; RDD2020'den
  itibaren birden fazla ülkenin standartları dikkate alındı ve 4 kategori kaldı. Bu yüzden metin "sınıflarımız RDD2022'nin
  etiketleme şemasını izliyor; kategoriler ilk olarak Japon kılavuzuna göre tanımlandı; ASTM'den alınmadı" diyor. Makale
  ASTM'den hiç söz etmiyor. ASTM tarafında yalnız resmî sayfada yazanı söylüyoruz: standart görsel denetimle gözlenen
  yüzey hasarına dayanıyor, modelimizin bulduğu da görünür yüzey hasarı. "Benzer türlere karşılık geliyor" gibi bir
  eşleme çıkarımı yapılmadı (ASTM'nin hasar listesi doğrulanamadı). PCI hesaplamadığımız açıkça yazıldı: model hasarı
  bulur ama yolu puanlamaz.
- **Kendi cümlelerimiz (2026-11-12 kontrolü):** Yalnız ASTM cümlesi kaynağa ("based on the distress observed on the
  surface" / "through visual surveys") çok yakındı; anlam aynı kalacak şekilde yeniden yazıldı. Diğer cümleler zaten
  kendi cümlemiz olduğu için değiştirilmedi.
- **COCO / PASCAL VOC:** Bunlar ISO gibi resmî standart değil, alanda fiilen kullanılan ölçüm kuralları. Ana metriğimiz
  mAP50, COCO sayfasında "PASCAL VOC metric" diye geçiyor; bu, referans projeyle ve literatürle karşılaştırmayı mümkün kılıyor.
- *Anlatım:* "Gereksinimleri bu raporda 29148'e göre yazdık; kalite hedeflerini 25010'a, final testlerini 29119'a
  göre yazacağız. Diyagramlar UML 2.5.1. Sınıflarımız RDD2022'nin etiketleme şemasından; bu kategoriler ilk olarak Japon
  yol bakım kılavuzuna göre tanımlanmış, ASTM'den alınmadı. ASTM D6433 de gözle görülen yüzey hasarına dayanıyor, bizim
  model de görünür yüzey hasarını buluyor; ama biz yol puanı (PCI) hesaplamıyoruz, yalnızca hasarı buluyoruz. Doğruluğu COCO'nun mAP50 ve mAP50-95
  metrikleriyle ölçüyoruz."
