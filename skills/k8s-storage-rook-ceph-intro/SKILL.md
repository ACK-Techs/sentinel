---
name: k8s-storage-rook-ceph-intro
description: "Rook-Ceph ile k8s-native dağıtık storage’a giriş yapmak, hangi use-case’lerde uygun olduğunu anlamak veya “cluster içi depolamayı kendimiz mi işletelim?” sorusunu değerlendirmek gerektiğinde kullan. Amaç: **Rook/Ceph’in operasyon maliyetini görünür kılmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- Rook-Ceph temel bileşenleri ve hangi problem için seçileceği
- Block/file/object storage modlarının kısa ayrımı
- Riskler: operasyon yükü, disk sağlık, recovery karmaşıklığı

## Workflow
- İhtiyacı doğrula:
  - Harici managed storage yok mu? RWX/RWO/objeyi tek platformda mı istiyorsun?
- Mimariyi ayır:
  - Rook operator ne yapar, Ceph cluster ne işletir?
- Operasyon riski:
  - Disk sayısı, node sayısı, network kalitesi ve backup planı.
- İlk adım:
  - POC ile başla; prod ölçeğini doğrudan hedefleme.
- Doğrulama:
  - Sağlıklı cluster + test PVC + IO doğrulaması.

## Common mistakes
- Küçük cluster’da gereksiz karmaşık storage katmanı kurmak.
- Recovery/runbook yazmadan Ceph’e güvenmek.

## References
- `skills/k8s-storage-csi-driver`
- `skills/platform-capacity-review`
