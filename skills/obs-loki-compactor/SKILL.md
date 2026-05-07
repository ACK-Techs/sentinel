---
name: obs-loki-compactor
description: Loki’de retention (kaç gün saklanacak) uygulamak ve eski index/chunk verisini temizlemek için compactor davranışını anlamak/ayarlamak gerektiğinde kullan. “retention çalışmıyor”, “eski loglar silinmiyor”, “erken silindi”, “compactor ne yapar?” gibi sorular için.
---

## Purpose
Bu skill’in çıktısı:
- Retention politikasının Loki’de **hangi bileşenle** uygulandığının net açıklaması (compactor)
- “Silme”nin iki boyutu: index metadata vs chunk data (storage backend’e bağlı)
- Sorun giderme checklist’i: retention niye işlemez / niye agresif olur

## Workflow
- Önce storage modelini doğrula:
  - Filesystem vs object storage → retention uygulanabilirliği ve davranışı değişir.
- Retention hedefini yaz:
  - Kaç gün? (örn. 7/14/30)
  - Legal/compliance gereksinimi var mı? (silme geri döndürülemez olabilir)
- Compactor’ın “ne yaptığı”nı ayır:
  - Index birleştirme/temizleme
  - Retention için eski veriyi işaretleme ve silme adımları
- “Silinmiyor” teşhisi:
  - Compactor çalışıyor mu? (log/metric)
  - Retention parametresi yanlış yerde mi? (config drift)
  - Object storage erişim/izin sorunu var mı?
- “Erken siliniyor” teşhisi:
  - Saat/timestamp sorunları (log timestamp’i ileri/geri)
  - Yanlış retention süresi veya tenant/policy karışıklığı
- Doğrulama:
  - Bilerek eski bir aralık seçip query yap: retention sonrası dönmemesi beklenir.

## Warnings
- Retention ayarı “hemen siler” gibi beklenmemeli; periyodik işlemlerle etkisi gecikmeli görülür.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-storage-backend`
