---
name: k8s-storage-pvc-pv
description: PersistentVolumeClaim/PersistentVolume ilişkisini tasarlamak, access mode/reclaim policy seçmek veya “pod storage’ya bağlanamıyor” sorununu çözmek gerektiğinde kullan. Amaç: **uygulamanın depolama ihtiyacını doğru volume modeliyle eşleştirmektir**.
---

## Purpose
Bu skill’in çıktısı:
- PVC/PV ilişki şeması ve access mode kararı
- Reclaim policy ve yaşam döngüsü notu
- Doğrulama: bind durumu ve pod mount kanıtı

## Workflow
- İhtiyacı sabitle:
  - Kalıcı veri mi, paylaşımlı erişim mi, tek node performansı mı?
- PVC tasarla:
  - Boyut, access mode, storage class.
- PV boyutu:
  - Statik provision mı, dinamik provision mı?
  - Reclaim policy `Delete` mi `Retain` mi?
- Bağlanma kontrolü:
  - PVC `Bound` mu? event’lerde neden bekliyor?
- Doğrulama:
  - Pod mount ediyor mu, dosya yazıp restart sonrası veri kalıyor mu?

## Common mistakes
- `ReadWriteMany` beklentisi olup altyapının sadece `ReadWriteOnce` desteklemesi.
- Reclaim policy’yi düşünmeden veri silmek.

## References
- `skills/k8s-storage-storageclass`
- `skills/k8s-storage-data-migration`
