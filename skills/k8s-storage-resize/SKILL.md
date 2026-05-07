---
name: k8s-storage-resize
description: "PVC kapasitesini büyütmek, online resize desteklerini anlamak veya “diski büyüttüm ama filesystem değişmedi” sorununu çözmek gerektiğinde kullan. Amaç: **storage ve filesystem katmanlarını birlikte doğrulamaktır**."
---

## Purpose
Bu skill’in çıktısı:
- Resize önkoşulları ve güvenli akış
- StorageClass expansion desteği kontrolü
- Doğrulama: PVC kapasitesi + pod içi filesystem büyümüş mü?

## Workflow
- Destek kontrolü:
  - StorageClass `allowVolumeExpansion` açık mı?
  - CSI/backend online resize destekli mi?
- Resize uygula:
  - PVC request’i büyüt; küçültme bekleme.
- Filesystem katmanı:
  - OS/filesystem genişleme otomatik mi, yeniden mount gerekir mi?
- Doğrulama:
  - PVC status kapasitesi
  - Pod içinden `df -h`

## Common mistakes
- Volume büyüyünce app’in anında daha büyük alan göreceğini varsaymak.
- Shrink desteği beklemek.

## References
- `skills/k8s-storage-storageclass`
- `skills/k8s-storage-pvc-pv`
