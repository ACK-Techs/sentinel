---
name: obs-loki-pattern-detection
description: Loki’de “hangi hata mesajları kümeleniyor / en çok hangi pattern’ler var?” gibi tekrar eden log şablonlarını çıkarmak veya anomaliye giden yeni pattern’i tespit etmek gerektiğinde kullan. Regex ile tek tek aramak yerine pattern odaklı analiz üretir.
---

## Purpose
Bu skill’in çıktısı:
- İncelenecek kapsam için pattern odaklı sorgu(lar) ve beklenen çıktı yorumu
- “Top N pattern” yaklaşımıyla gürültüyü azaltma (aynı hatanın varyantlarını tekleştirme)
- Yanıltıcı kümeleri engellemek için normalizasyon önerisi (ID/path gibi dinamik parçalar)

## Workflow
- Kapsamı daralt:
  - Stream selector: `{app="...", namespace="..."}` gibi
  - Zaman aralığı: “incident penceresi” (örn. son 30–120 dk)
- “Pattern” çıkarma hedefini seç:
  - Hata kümeleri: `level=error` veya “panic/exception”
  - Yeni pattern: baseline dönemle karşılaştırma (önceki gün/hafta)
- Normalizasyon kuralı yaz (en kritik kısım):
  - Dinamik ID, UUID, request id, path param’ları pattern’i bozar; bunları line içinde maskelenebilir hale getir.
  - Eğer log JSON ise, önce parse edip sabit field’ları kullan.
- Çıktıyı yorumla:
  - En üst pattern’ler hangi bileşene işaret ediyor?
  - Aynı pattern farklı label’larda mı çoğalıyor? (deployment/zone)
- Doğrulama:
  - Seçilen top pattern için LogQL ile örnek satırlar çek; gerçekten aynı kök sebep mi?

## Common mistakes
- Dinamik alanları normalize etmeden pattern çıkarmak: “her satır ayrı pattern” olur.
- Label set’i çok geniş: pattern analizi gürültüye boğulur.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-query-logql`
- `skills/obs-loki-structured-metadata`
