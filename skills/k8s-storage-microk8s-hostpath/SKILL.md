---
name: k8s-storage-microk8s-hostpath
description: "MicroK8s’in hostpath-storage addon davranışını anlamak, default StorageClass etkisini görmek veya lab ortamında neden bu kadar “kolay” çalıştığını açıklamak gerektiğinde kullan. Amaç: **MicroK8s hostpath’in sınırlarını doğru koymaktır**."
---

## Purpose
Bu skill’in çıktısı:
- MicroK8s hostpath storage addon özet davranışı
- Default class ve node bağımı etkisi
- Doğrulama: PVC bind ve veri kalıcılığı beklentisi

## Workflow
- Ortamı doğrula:
  - Tek node mu, çok node mu?
- Addon davranışı:
  - Default StorageClass ne sağlıyor, path nerede oluşuyor?
- Sınırlar:
  - Çok node veya prod taşınabilirlik için neden uygun değil?
- Doğrulama:
  - Test PVC + pod mount
  - Node değişiminde veri beklentisi

## Common mistakes
- MicroK8s hostpath’i prod-grade shared storage sanmak.
- Default class yüzünden workload’ların fark etmeden buna bağlanması.

## References
- `skills/microk8s-addons-dns-storage`
- `skills/k8s-storage-hostpath`
