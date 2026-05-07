---
name: k8s-storage-local-pv
description: Node’a bağlı yüksek performanslı local diskleri Kubernetes’e sunmak veya “disk hızlı olsun ama pod başka node’a geçemesin” trade-off’unu yönetmek gerektiğinde kullan. Amaç: **local storage’nın performans ve taşınabilirlik dengesini kurmaktır**.
---

## Purpose
Bu skill’in çıktısı:
- Local PV kullanım uygunluğu ve node affinity sonucu
- Provision/bind davranışı
- Doğrulama: pod gerçekten doğru node ve diske bağlanıyor mu?

## Workflow
- İhtiyacı belirle:
  - Düşük latency/high IOPS gerekiyor mu?
- Node bağımlılığını kabul et:
  - Pod failover başka node’a gittiğinde veri erişimi ne olacak?
- PV/PVC tasarla:
  - Node affinity ile local path’i eşleştir.
- Operasyon:
  - Disk arızası, node kaybı ve backup stratejisini not et.
- Doğrulama:
  - Pod scheduling local disk node’una mı yapılıyor?

## Common mistakes
- HA beklentisi olan servise local PV verip node failure’ı hesaba katmamak.
- Backup planı olmadan local disk’e güvenmek.

## References
- `skills/k8s-storage-pvc-pv`
- `skills/k8s-core-statefulset`
