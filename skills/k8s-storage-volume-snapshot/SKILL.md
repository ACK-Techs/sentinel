---
name: k8s-storage-volume-snapshot
description: PVC snapshot almak, geri yüklemek veya “değişiklik öncesi geri dönüş noktası” oluşturmak gerektiğinde kullan. Amaç: **snapshot kabiliyetini storage backend gerçekliğiyle birlikte kullanmaktır**.
---

## Purpose
Bu skill’in çıktısı:
- VolumeSnapshot/VolumeSnapshotClass kullanım akışı
- Snapshot sonrası restore/clone planı
- Doğrulama: snapshot hazır ve restore edilebilir mi?

## Workflow
- Backend desteğini doğrula:
  - CSI driver snapshot destekli mi?
- Snapshot akışı:
  - Quiesce gerekiyor mu? uygulama tutarlılığı nasıl sağlanacak?
- Restore planı:
  - Aynı PVC’ye mi, yeni PVC’ye mi dönecek?
- Operasyon:
  - Retention ve maliyet etkisi.
- Doğrulama:
  - Snapshot `ReadyToUse` mu?
  - Restore edilen volume beklenen veriyi içeriyor mu?

## Common mistakes
- Storage backend desteklemeden CRD var diye snapshot çalışacak sanmak.
- App-consistency ihtiyacını atlamak.

## References
- `skills/k8s-storage-data-migration`
- `skills/k8s-storage-backup-velero`
