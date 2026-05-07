---
name: k8s-storage-csi-driver
description: CSI driver kurmak, storage backend’i Kubernetes’e entegre etmek veya “PVC dynamic provision olmuyor / attach hatası var” sorunlarını çözmek gerektiğinde kullan. Amaç: **CSI bileşenlerini ve failure surface’i doğru okumaktır**.
---

## Purpose
Bu skill’in çıktısı:
- CSI driver bileşen haritası ve sorumlulukları
- Provision/attach/mount hata ayırımı
- Doğrulama: test PVC + pod mount akışı

## Workflow
- Driver bağlamı:
  - Hangi backend? block/file/object benzeri davranış?
- Bileşenleri ayır:
  - Controller tarafı provision/attach, node tarafı mount.
- Sorun sınıflandır:
  - PVC pending mi, volume attach mı, node mount mı?
- Yetki/CRD:
  - Driver CRD, sidecar version ve RBAC uyumlu mu?
- Doğrulama:
  - Test PVC `Bound`
  - Pod mount ve IO başarılı

## Common mistakes
- Backend hatasını doğrudan Kubernetes sorunu sanmak.
- CSI version uyumsuzluğunu atlamak.

## References
- `skills/k8s-storage-storageclass`
- `skills/k8s-storage-volume-snapshot`
