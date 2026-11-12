# Sustainable Development Goal — Taslak (ara rapor)

> **Durum:** Taslak; Word raporuna henüz eklenmedi. Şablon: "Realistic Constraints and Conditions → Sustainable
> Development Goal (midterm)", en az 1000 karakter (hedef 1200–1500). Şablon açıklaması: "Discuss the relationship
> between your project topic and the sustainable development goal you chose in section 13." (duyurudaki listede
> "section 14"). Seçim: SDG 11 (raporun sonundaki açılır listede de seçilecek).
> BM hedef metinleri resmî gösterge çerçevesinden doğrulandı ve kendi cümlelerimizle anlatıldı; katkı yalnız
> "destekler" düzeyinde. Kaynak stili IEEE; numaralar **geçici**: [1]–[19] literatür, [20]–[28] standartlar,
> [29]–[37] yasal, [38]–[40] sağlık/çevre, yeni kaynak [41].
> Bu dosyanın iki kopyası var ve her zaman aynı olmalı: `docs/rapor/ozel/sdg.md` (git dışı) ve `docs/rapor/sdg.md`
> (git'te). Türkçe açıklama: `docs/rapor/ozel/sdg-turkce.md`.

<!-- SDG-START -->
### Sustainable Development Goal

**Chosen goal.** This project is connected to SDG 11, which is about building cities and communities that are safe, open to everyone, resilient and sustainable [41]. Roads are one of the basic parts of every city: people reach work, school and public services over them, so the condition of the road surface matters to all residents.

**Main link: Target 11.2.** Among its aims for 2030, target 11.2 asks for safer road travel as part of transport systems that serve everyone [41]. Our project relates only to this road safety aim. By finding cracks and potholes in road images, the system can show municipalities where damage is and help them plan maintenance earlier. In this way it can support the target; it cannot reach the target on its own, and we have not measured any effect of the system on road safety.

**Supporting link: Target 9.1.** Target 9.1 calls for infrastructure that is of good quality, dependable and able to last [41]; frequent and inexpensive damage surveys are one practical way to help keep road networks in that state.

**Limits.** The contribution of this work is indirect. Its real value depends on whether road authorities use the detected damage in their maintenance decisions, which lies outside the scope of this project.
<!-- SDG-END -->

## REFERENCES (yeni kaynak)

[41] United Nations, "Global indicator framework for the Sustainable Development Goals and targets of the 2030 Agenda for Sustainable Development," A/RES/71/313, Annex, as refined by E/CN.3/2026/12. [Online]. Available: https://unstats.un.org/sdgs/indicators/Global-Indicator-Framework-after-2026-refinement_Eng.pdf (accessed Nov. 12, 2026).
<!-- REF-END -->

---

## Kaynak Kontrol Tablosu

Not: Hedef metinleri iki resmî BM kaynağında birebir aynı: sdgs.un.org goal sayfaları (Goal 3, 9, 11; HTTP 200) ve
BM İstatistik Bölümü'nün gösterge çerçevesi PDF'i (unstats.un.org; PDF metni yerelde pypdf ile okundu). Kaynakçaya
kullanıcı kararıyla yalnız PDF [41] girdi. Belgenin başında "A/RES/71/313 … E/CN.3/2026/12" künyeleri ve "Global
indicator framework for the Sustainable Development Goals and targets of the 2030 Agenda for Sustainable Development"
başlığı var. Kurumsal yazar "United Nations" (çerçeve BM Genel Kurulu kararının eki).

| # | Kaynak | Link | Metindeki iddia | Kaynaktan birebir alıntı | Durum |
|---|---|---|---|---|---|
| 41 | BM gösterge çerçevesi (A/RES/71/313, E/CN.3/2026/12 düzeltmesiyle) — Goal 11 | https://unstats.un.org/sdgs/indicators/Global-Indicator-Framework-after-2026-refinement_Eng.pdf · https://sdgs.un.org/goals/goal11 | SDG 11: güvenli, herkese açık, dayanıklı ve sürdürülebilir şehirler ve topluluklar | "Goal 11. Make cities and human settlements inclusive, safe, resilient and sustainable" | Doğru |
| 41 | aynı — Target 11.2 | aynı | 2030'a kadar, herkese hizmet eden ulaşım sistemlerinin bir parçası olarak daha güvenli yol yolculuğu | "11.2 By 2030, provide access to safe, affordable, accessible and sustainable transport systems for all, improving road safety, notably by expanding public transport, with special attention to the needs of those in vulnerable situations, women, children, persons with disabilities and older persons" | Doğru. Bağlantı yalnız "improving road safety"; toplu taşıma kısmı ve 11.2.1 göstergesi metne konmadı (kullanıcı kararı) |
| 41 | aynı — Target 9.1 | aynı · https://sdgs.un.org/goals/goal9 | Kaliteli, güvenilir ve dayanıklı altyapı | "9.1 Develop quality, reliable, sustainable and resilient infrastructure, including regional and transborder infrastructure, to support economic development and human well-being, with a focus on affordable and equitable access for all" | Doğru. Hedef yılı yok → metinde yıl yok |
| — | Kendi iddiamız | — | Sistem hasarın yerini gösterip bakımın daha erken planlanmasına yardım edebilir; etkisi ölçülmedi; değeri kurumların kullanımına bağlı | — | Kaynaksız; "support / help" düzeyinde, ölçüm iddiası yok |

## Doğrulanamayanlar / çıkarılanlar

| Konu | Durum |
|---|---|
| Target 3.6 ("By 2020, halve the number of global deaths and injuries from road traffic accidents") | Doğrulandı ama **çıkarıldı** (kullanıcı kararı): hedef yılı 2020, süresi geçmiş; resmî metin 2026 düzeltmeli çerçevede de 2020. Ölüm verileri Health/Environment'ta |
| sdgs.un.org Goal 11 sayfası ayrı kaynak olarak | Doğrulandı ama kaynakçaya eklenmedi; [41] tüm hedefleri veriyor (kullanıcı kararı) |
| 11.2'nin toplu taşıma kısmı ve 11.2.1 göstergesi | Projemizle ilgisi yok; bağlantıyı abartmamak için metinde yok |
| Projenin yol güvenliğine ölçülmüş etkisi | Yok; metinde açıkça "we have not measured" deniyor |

## Neden böyle yazıldı (sunumda nasıl anlatılır)

- **Şablonun isteği:** "Projenizin konusu ile seçtiğiniz hedef arasındaki ilişkiyi tartışın." Yapı: seçilen hedef →
  ana bağlantı (11.2) → destekleyici bağlantı (9.1, tek cümle) → sınır.
- **Kendi cümlelerimiz:** BM hedef metinleri birebir kopyalanmadı; anlam aynı, kelimeler ve yapı bizim (ör. "inclusive"
  → "open to everyone", "reliable … resilient" → "dependable and able to last"). Birebir metinler yalnız yukarıdaki
  tabloda.
- **Abartma yok:** 11.2'nin yalnız yol güvenliği kısmına bağlanıyoruz; sistem hedefi "destekleyebilir", tek başına
  ulaştıramaz; yol güvenliğine etkisi ölçülmedi. Değerin, sonuçları bakım kararlarında kullanan kurumlara bağlı olduğu yazıldı.
- **Tekrar yok:** Health/Environment'taki ölüm sayıları, maliyetler, erken bakım ve elle denetim cümleleri burada
  tekrar edilmedi; 3.6 da bu yüzden (ve süresi geçtiği için) çıkarıldı.
- *Anlatım:* "Seçtiğimiz hedef SDG 11, güvenli ve sürdürülebilir şehirler. Yollar şehrin temel altyapısı. Asıl
  bağlantımız 11.2'nin yol güvenliği kısmı: sistem hasarın yerini göstererek belediyelerin bakımı daha erken
  planlamasına yardım edebilir. Bu hedefi destekler, tek başına ulaştırmaz; yol güvenliğine etkisini ölçmedik. Ayrıca
  9.1'deki kaliteli ve dayanıklı altyapı hedefini de destekler."
