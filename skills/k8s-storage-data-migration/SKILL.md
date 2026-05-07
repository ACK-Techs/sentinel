---
name: k8s-storage-data-migration
description: "Bir volume’den diğerine veri taşımak, storage backend değiştirmek veya “PVC değişecek ama veri kaybolmamalı” geçişini planlamak gerektiğinde kullan. Amaç: **veri geçişini kesinti ve tutarlılık açısından güvenli yürütmektir**."
---

## Purpose
Bu skill’in çıktısı:
- Migration yöntemi seçimi (rsync, clone, snapshot restore, app-level export)
- Downtime ve consistency kararları
- Doğrulama: taşınan veri bütünlüğü ve cutover planı

## Workflow
- Veri karakterini anla:
  - Sıcak yazılan veri mi, maintenance window var mı?
- Yöntemi seç:
  - Snapshot/clone destekleniyorsa tercih.
  - Değilse geçici pod ile rsync veya app-level export/import.
- Cutover:
  - Eski volume ne zaman read-only olur? geri dönüş planı var mı?
- Doğrulama:
  - Dosya sayısı/byte, uygulama health, örnek veri kontrolü.

## Common mistakes
- Sıcak veri üzerinde rsync’i tek seferde yeterli sanmak.
- Geri dönüş planı olmadan eski volume’ü silmek.

## References
- `skills/k8s-storage-volume-snapshot`
- `skills/k8s-storage-backup-velero`
