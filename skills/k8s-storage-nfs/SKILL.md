---
name: k8s-storage-nfs
description: NFS tabanlı paylaşımlı depolama sunmak, RWX ihtiyaçlarını karşılamak veya “aynı volume’ü birden çok pod paylaşmalı” senaryosunu yönetmek gerektiğinde kullan. Amaç: **NFS’in kullanım kolaylığı ile performans/single-point-of-failure riskini birlikte değerlendirmektir**.
---

## Purpose
Bu skill’in çıktısı:
- NFS mount/provision yaklaşımı
- RWX senaryosu ve performans beklentisi
- Doğrulama: çoklu pod erişimi ve izin/mount sağlığı

## Workflow
- Kullanım gerekçesi:
  - Gerçekten paylaşımlı yazma gerekiyor mu?
- Sunucu/provisioner:
  - Var olan NFS share mi, dynamic provisioner mı?
- Performans ve kilit davranışı:
  - Çok yoğun küçük IO için uygun mu?
- İzinler:
  - UID/GID, root squash, path ownership.
- Doğrulama:
  - İki pod aynı dosyayı okuyup/yazabiliyor mu?

## Common mistakes
- NFS’i database storage için varsayılan çözüm sanmak.
- Permission modelini planlamadan mount etmek.

## References
- `skills/k8s-storage-storageclass`
- `skills/k8s-storage-pvc-pv`
