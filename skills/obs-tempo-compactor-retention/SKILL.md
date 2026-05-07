---
name: obs-tempo-compactor-retention
description: Tempo’da trace retention (kaç gün/saklama süresi) uygulamak ve compactor davranışını doğru anlamlandırmak gerektiğinde kullan. “retention çalışmıyor”, “eski trace silinmiyor/erken silindi”, “compactor ne yapar?” gibi saklama politikası odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Retention hedefi ve bunun Tempo’da nasıl uygulandığına dair netlik (compactor + storage)
- “Silme gecikmesi” beklentisi (anlık değil, periyodik işler)
- Retention sorunlarında kısa teşhis checklist’i (config drift, storage izinleri, clock)

## Workflow
- Retention hedefini yaz:
  - Kaç gün/saat? (maliyet ve incident ihtiyacı)
  - Legal/compliance gereksinimi var mı?
- Storage backend ile birlikte düşün:
  - Local vs object storage; izinler/lifecycle retention davranışını etkiler.
- Compactor’ın rolü:
  - Trace blok/segment yönetimi ve retention cleanup işleri.
  - İşler periyodiktir; “hemen sil” beklentisi gerçekçi değildir.
- “Silinmiyor” teşhisi:
  - Compactor çalışıyor mu? (log/metric)
  - Yanlış config yüklendi mi? (drift)
  - Storage erişim/izin sorunu var mı?
- “Erken siliniyor” teşhisi:
  - Timestamp/clock drift (özellikle collector/agent)
  - Yanlış retention süresi
- Doğrulama:
  - Bilerek eski bir zaman penceresinden trace araması yap; retention sonrası dönmemesi beklenir.

## Common mistakes
- Retention’ı sadece storage lifecycle’a bırakmak: Tempo tarafında beklentiyle uyuşmayabilir.
- Clock drift’i ihmal etmek: “çok eski/çok yeni” trace’ler elenebilir.

## References
- `skills/obs-tempo-storage-backend`
