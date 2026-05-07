---
name: k8s-storage-storageclass
description: StorageClass tanımlamak, dynamic provisioning davranışını belirlemek veya “PVC pending kalıyor / yanlış disk türü geliyor” sorunlarını çözmek gerektiğinde kullan. Amaç: **provisioning varsayımlarını açık hale getirmektir**.
---

## Purpose
Bu skill’in çıktısı:
- StorageClass parametreleri ve uygun provisioner seçimi
- `volumeBindingMode`, expansion ve default class kararı
- Doğrulama: PVC doğru sınıftan doğru davranışla oluşturuluyor mu?

## Workflow
- Altyapıyı belirle:
  - Hostpath, cloud disk, NFS, CSI, local PV?
- Class davranışını seç:
  - Default mı, özel amaçlı mı?
  - `Immediate` vs `WaitForFirstConsumer`
- Özellikler:
  - `allowVolumeExpansion`, reclaim davranışı, fsType vb.
- Sorun analizi:
  - PVC pending ise provisioner var mı, class adı doğru mu?
- Doğrulama:
  - Test PVC oluştur; binding ve pod schedule sonucu beklenen mi?

## Common mistakes
- Her şeyi default StorageClass’e bağlamak: özel workload ihtiyacı kaybolur.
- Zone farkı varken `Immediate` bind ile yanlış node seçimleri.

## References
- `skills/k8s-storage-pvc-pv`
- `skills/k8s-storage-resize`
