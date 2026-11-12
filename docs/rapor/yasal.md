# Legal Consequences — Taslak (ara rapor)

> **Durum:** Taslak; Word raporuna henüz eklenmedi. Şablon: "Realistic Constraints and Conditions → Legal
> Consequences (midterm)", en az 1000 karakter (hedef 1200–1500). Her iddia resmî / birincil kaynakta doğrulandı
> (sondaki Kaynak Kontrol Tablosu); hukuki yorum yok, yalnız "kaynak ne diyor, biz ne yapıyoruz / yapacağız".
> Kaynak stili IEEE; numaralar **geçici**: [1]–[19] literatür, [20]–[28] standartlar, yeni kaynaklar [29]–[37].
> Bu dosyanın iki kopyası var ve her zaman aynı olmalı: `docs/rapor/ozel/yasal.md` (git dışı) ve
> `docs/rapor/yasal.md` (git'te). Türkçe açıklama: `docs/rapor/ozel/yasal-turkce.md`.

<!-- LEGAL-START -->
### Legal Consequences

**Dataset.** The figshare record of RDD2022 gives its license as CC BY 4.0 [36], [37], while the README of its GitHub repository gives CC BY-SA 4.0 [29], [30]. We follow the stricter terms: the dataset is credited in this report and in our repository, and adapted data, if shared, will carry the same license, as CC BY-SA requires [29]. Our converted YOLO-format copy was uploaded to Kaggle as a private dataset and is not publicly available.

**Software.** Ultralytics YOLO is licensed under AGPL-3.0 [32]. Under Section 13 of this license, people who use a modified version remotely over a network must be given a way to obtain its source code [31]. Our code is kept in a public repository, and its license will be chosen to be compatible with AGPL-3.0. Since the reference project [19] carries no license, copyright law gives others no permission to copy or build on its code [33]; we only studied it and wrote our own code.

**Personal data.** Road images may show faces and license plates. Turkish Law No. 6698 counts any information that can be linked to a specific person as personal data [34], and the GDPR [35] regulates the processing of personal data in the EU; part of the images was collected in the Czech Republic. The planned camera mode will process frames without storing them.

**Responsibility.** The system is designed as a decision-support tool: it marks possible damage, and the final decision stays with a human inspector.
<!-- LEGAL-END -->

## REFERENCES (yeni kaynaklar; [19] literatür taramasında)

[29] Creative Commons, "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0), legal code." [Online]. Available: https://creativecommons.org/licenses/by-sa/4.0/legalcode.en (accessed Nov. 11, 2026).

[30] Sekimoto Lab (sekilab), "RoadDamageDetector," GitHub repository (README: License). [Online]. Available: https://github.com/sekilab/RoadDamageDetector (accessed Nov. 11, 2026).

[31] Free Software Foundation, "GNU Affero General Public License," Version 3, Nov. 19, 2007. [Online]. Available: https://www.gnu.org/licenses/agpl-3.0.html (accessed Nov. 11, 2026).

[32] Ultralytics, "Ultralytics licensing." [Online]. Available: https://www.ultralytics.com/license (accessed Nov. 11, 2026).

[33] GitHub, "Licensing a repository," GitHub Docs. [Online]. Available: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository (accessed Nov. 11, 2026).

[34] *Kişisel Verilerin Korunması Kanunu* [Personal Data Protection Law], Law No. 6698, Resmî Gazete no. 29677, Apr. 7, 2016. [Online]. Available: https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6698&MevzuatTur=1&MevzuatTertip=5

[35] *Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation)*, CELEX 32016R0679, Apr. 27, 2016. [Online]. Available: https://op.europa.eu/en/publication-detail/-/publication/3e485e15-11bd-11e6-ba9a-01aa75ed71a1

[36] D. Arya *et al.*, "RDD2022 - The multi-national Road Damage Dataset released through CRDDC'2022," figshare, Dataset, 2022, doi: 10.6084/m9.figshare.21431547.

[37] Creative Commons, "Attribution 4.0 International (CC BY 4.0), legal code." [Online]. Available: https://creativecommons.org/licenses/by/4.0/legalcode.en (accessed Nov. 11, 2026).
<!-- REF-END -->

---

## Kaynak Kontrol Tablosu

Not: EUR-Lex otomatik erişimde boş yanıt (HTTP 202) verdi; GDPR'ın künyesi AB Yayın Ofisi (op.europa.eu) kayıt
sayfasından doğrulandı, madde metni okunamadı. KVKK'nın Türkçe metni mevzuat.gov.tr PDF'inden okundu. figshare sayfası
otomatik erişime 403 verdi; lisans alanı kullanıcı tarafından elle okundu (2026-11-11), künye ve lisans ayrıca DOI kayıt
kuruluşu DataCite'ın kaydından (`https://api.datacite.org/dois/10.6084/m9.figshare.21431547`) doğrulandı.
**Kaynaklar çelişiyor:** figshare kaydı CC BY 4.0, GitHub README'si CC BY-SA 4.0 → metinde ikisi de yazıldı, daha katı
olana (CC BY-SA: atıf + aynı lisansla paylaşım) uyduğumuz söylendi.

| # | Kaynak | Link | Metindeki iddia | Kaynaktan birebir kısa alıntı | Durum |
|---|---|---|---|---|---|
| 29 | CC BY-SA 4.0 legal code + deed | https://creativecommons.org/licenses/by-sa/4.0/legalcode.en · https://creativecommons.org/licenses/by-sa/4.0/ | README'nin verdiği lisans; CC BY-SA uyarlanmış materyalin aynı lisansla paylaşılmasını istiyor (uyduğumuz daha katı koşul) | §3(a)(1): "If You Share the Licensed Material (including in modified form), You must:" · §3(a)(1)(A)(i): "identification of the creator(s) of the Licensed Material" · §3(a)(1)(C): "indicate the Licensed Material is licensed under this Public License" · §3(b)(1): "The Adapter's License You apply must be a Creative Commons license with the same License Elements" · §1 "Share means to provide material to the public by any means or process that requires permission under the Licensed Rights" · deed: "you must distribute your contributions under the same license as the original." | Doğru |
| 30 | RDD2022 resmî deposu sekilab/RoadDamageDetector, README (RDD2022 makalesi [4] s. 2 bu depoyu veri adresi olarak veriyor) | https://github.com/sekilab/RoadDamageDetector | Veri setinin GitHub deposundaki README CC BY-SA 4.0 diyor | README "# License" (README `gh api` ile doğrudan okundu): "Images on this dataset are available under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)." · RDD2022 PDF: "The RDD2022 data can be accessed at the GitHub repository: https://github.com/sekilab/RoadDamageDetector" | Doğru (alıntı). Deponun MIT lisansı kod için. **Dikkat:** "# License" bölümü README'nin sonunda, "Road Damage Dataset 2018" bölümünden sonra, genel bir üst başlık; RDD2022'ye özel bir lisans cümlesi değil. RDD2022'nin kendi kaydı [36] farklı lisans veriyor (çelişki) |
| 36 | figshare kaydı: D. Arya vd. (20 yazar), "RDD2022 - The multi-national Road Damage Dataset released through CRDDC'2022", figshare, Dataset, 2022 (oluşturma 2022-10-29, güncelleme 2023-05-30), DOI 10.6084/m9.figshare.21431547 | https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547 · https://doi.org/10.6084/m9.figshare.21431547 · DataCite: https://api.datacite.org/dois/10.6084/m9.figshare.21431547 | RDD2022'nin figshare kaydı CC BY 4.0 diyor | Sayfa LICENCE alanı (kullanıcı, elle): "CC BY 4.0" · DataCite rightsList: "Creative Commons Attribution 4.0 International", rightsIdentifier "cc-by-4.0" · sekilab README'si bu kaydı gösteriyor: "The RDD2022 data released through CRDDC is now also available on FigShare Repository!" | Doğru (kullanıcı + DataCite). Künye DataCite'tan: ilk yazar Arya, Deeksha; yayıncı figshare; yıl 2022 |
| 37 | CC BY 4.0 legal code | https://creativecommons.org/licenses/by/4.0/legalcode.en | CC BY de paylaşırken atıf ve lisansı belirtmeyi istiyor; ShareAlike koşulu yok | §3(a)(1): "If You Share the Licensed Material (including in modified form), You must:" · "identification of the creator(s) of the Licensed Material" · "indicate the Licensed Material is licensed under this Public License" · Metinde "ShareAlike" geçmiyor (sayfa metni arandı) | Doğru |
| 31 | GNU AGPL v3 (19 Kasım 2007), Madde 13 | https://www.gnu.org/licenses/agpl-3.0.html | Değiştirilmiş sürümle ağ üzerinden etkileşen kullanıcılara kaynak kod sunulmalı | "Version 3, 19 November 2007" · §13: "your modified version must prominently offer all users interacting with it remotely through a computer network" … "an opportunity to receive the Corresponding Source of your version" | Doğru |
| 32 | Ultralytics lisans sayfası | https://www.ultralytics.com/license | Ultralytics YOLO AGPL-3.0 lisanslı | "comfortable open-sourcing your entire project under AGPL-3.0" · "you must either:" "Open-source your entire project under AGPL-3.0, or" "Obtain an Ultralytics Enterprise License." · yerel paket bilgisi: `ultralytics` License-Expression `AGPL-3.0` | Doğru. Enterprise ayrıntısı metne konmadı (gereksiz) |
| 33 | GitHub Docs, "Licensing a repository" | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository | Lisans yoksa varsayılan telif geçerli, kod yeniden kullanılamaz | "without a license, the default copyright laws apply, meaning that you retain all rights to your source code" · "no one may reproduce, distribute, or create derivative works from your work" | Doğru |
| 34 | 6698 sayılı Kişisel Verilerin Korunması Kanunu (kabul 24/3/2016; RG 7/4/2016, sayı 29677) | https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6698&MevzuatTur=1&MevzuatTertip=5 · PDF: https://www.mevzuat.gov.tr/MevzuatMetin/1.5.6698.pdf · resmî İngilizce çeviri: https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law | Kimliği belirli/belirlenebilir kişiye ilişkin her bilgi kişisel veri | Madde 3(1)(d): "Kişisel veri: Kimliği belirli veya belirlenebilir gerçek kişiye ilişkin her türlü bilgiyi" · Madde 1(1): "kişisel verilerin işlenmesinde başta özel hayatın gizliliği olmak üzere kişilerin temel hak ve özgürlüklerini korumak" · KVKK çevirisi: "any information relating to an identified or identifiable natural person" | Doğru |
| 35 | Regulation (EU) 2016/679 (GDPR), 27 Nisan 2016 | https://op.europa.eu/en/publication-detail/-/publication/3e485e15-11bd-11e6-ba9a-01aa75ed71a1 | AB'de kişisel verilerin işlenmesini düzenliyor | Başlık: "Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016" "on the protection of natural persons with regard to the processing of personal data and on the free movement of such data" "and repealing Directive 95/46/EC (General Data Protection Regulation) (Text with EEA relevance)" · "Published: 2016-04-27" | Künye doğru; **madde metni (Md. 4(1) tanımı) doğrulanamadı** → metinde tanım verilmedi, yalnız başlıktaki kapsam |
| 19 | Referans proje oracl4/RoadDamageDetection | yerel `reference/RoadDamageDetection-main/` | LICENSE dosyası yok | (dosya listesinde LICENSE yok; CLAUDE.md, kararlar.md 2026-10-15) | Doğru |
| — | Kendi bilgilerimiz | README.md, kararlar.md 2026-10-18 | Veri setine README'de atıf; YOLO kopyası Kaggle'da private | README: "Atıf: Arya, Maeda, Sekimoto vd. …" · kararlar: "private dataset olarak yüklenir" | Doğru. README.md, CLAUDE.md ve plan.md'deki lisans satırları çelişkiyi gösterecek şekilde güncellendi (kararlar.md 2026-11-11) |

## Doğrulanamayanlar / çıkarılanlar

| Konu | Durum |
|---|---|
| GDPR Madde 4(1) "personal data" tanımı | EUR-Lex HTML ve PDF boş yanıt (202); metinde tanım yok, yalnız resmî başlıktaki kapsam |
| "Yüz ve plakalar veri setinde bulanıklaştırılmış" | **Metinden çıkarıldı.** Cümle yalnız sekilab README'sinin "# Privacy matters" bölümünde var: "based on visual inspection, when a person's face or a car license plate are clearly reflected in the image, they are blurred out." Ama bu bölüm README'nin sonunda, "Road Damage Dataset 2018" bölümünden sonra duran genel bir başlık; RDD2022'yi (Norveç, ABD, Çin verisi başka ekiplerce toplandı) kapsadığı yazmıyor. RDD2022 makalesinde (arXiv PDF) "privacy", "anonym", yüz/plaka bulanıklaştırma hiç geçmiyor (metin arandı). Bu yüzden RDD2022 için doğrulanamadı |
| "Norveç AEA üyesi, GDPR orada da geçerli" | Kaynakta doğrulanmadı ve hukuki yorum olur → metinde yalnız "part of the images was collected in the Czech Republic" (kullanıcı kararı) |
| "Hangi lisans geçerli?" | Kaynaklar çelişiyor (figshare CC BY 4.0, README CC BY-SA 4.0); hangisinin bağlayıcı olduğuna dair hukuki yorum yapılmadı, ikisi de yazıldı |
| AB Yapay Zekâ Yasası, diğer kütüphane lisansları | Kullanıcı kararıyla çıkarıldı |
| "Karar destek aracı, son karar insanda" | Kaynaksız; kendi tasarım kararımız (kullanıcı kararı) |

## Neden böyle yazıldı (sunumda nasıl anlatılır)

- **Hukuki yorum yok:** Her cümle ya kaynağın ne dediğini ya da bizim ne yaptığımızı / yapacağımızı söylüyor.
  "Bu dağıtım sayılır mı", "AGPL bizi bağlar mı" gibi yorumlar yapılmadı.
- **Veri seti:** İki resmî kaynak farklı lisans veriyor: RDD2022'nin figshare kaydı (DOI'li veri kaydı) CC BY 4.0,
  veri setinin GitHub deposundaki README CC BY-SA 4.0. Hangisinin geçerli olduğunu yorumlamıyoruz; ikisini de yazıp
  daha katı olana uyduğumuzu söylüyoruz (CC BY-SA, CC BY'ın atıf koşuluna ek olarak aynı lisansla paylaşım istiyor).
  Kaggle için yalnız olgu: "private yüklendi, herkese açık değil".
- **Yazılım:** Ultralytics AGPL-3.0; AGPL Madde 13 ağ üzerinden kullanım koşulunu tanımlıyor. Bizim yaptığımız: kod
  public repoda, lisansı AGPL-3.0 ile uyumlu seçilecek (repoda henüz LICENSE yok; dosya şimdi eklenmedi). Referans
  projenin lisansı olmadığı için kodunu kopyalamadık.
- **Kişisel veri:** Yalnız olgu: yol görüntülerinde yüz ve plaka çıkabilir. Veri setindeki bulanıklaştırma iddiası
  RDD2022 için doğrulanamadığı için metne konmadı. KVKK tanımı Türkçe resmî metinden. GDPR yalnız resmî başlığıyla;
  madde metni doğrulanamadı. AB bağlantısı somut olgu olarak yazıldı (Çek Cumhuriyeti), Norveç/AEA yorumu yapılmadı.
  Kamera modu henüz yapılmadığı için "will process frames without storing them" (gelecek zaman).
- **Sorumluluk:** Kaynaksız tasarım kararımız; hukuki dayanak iddia edilmiyor.
- **Kendi cümlelerimiz (2026-11-12 kontrolü):** Kaynağa neredeyse birebir olan üç cümle yeniden yazıldı, anlam aynı:
  AGPL §13 ("offer all users interacting with it remotely through a computer network … Corresponding Source"), GitHub
  Docs ("the default copyright laws apply"), KVKK çevirisi ("any information relating to an identified or identifiable
  natural person"). Diğer cümleler zaten kendi cümlemiz.
- *Anlatım:* "Veri setinin lisansı iki resmî kaynakta farklı yazıyor (CC BY ve CC BY-SA); biz daha katı olana uyuyoruz:
  atıf veriyoruz, uyarlanmış veriyi paylaşırsak aynı lisansla paylaşacağız. Uyarladığımız kopyayı herkese açık paylaşmadık.
  YOLO kütüphanesi AGPL lisanslı, kodumuz zaten açık ve lisansını buna uygun seçeceğiz. Referans projenin lisansı
  olmadığı için kodunu kopyalamadık. Görüntülerde yüz ve plaka çıkabilir; bunlar KVKK'ya göre kişisel veri
  sayılabilir, bu yüzden kamera modunda kareleri saklamayacağız. Sistem karar destek aracı; son karar insanda."
