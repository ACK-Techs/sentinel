---
name: k8s-scale-cluster-autoscaler
description: "Node sayısını iş yüküne göre artırıp azaltmak, pending pod’lar için kapasite açmak veya “pod scale oluyor ama node gelmiyor” sorunlarını çözmek gerektiğinde kullan. Amaç: **pod autoscaling ile node autoscaling’in sınırını birleştirmektir**."
---

## Purpose
Bu skill’in çıktısı:
- Cluster Autoscaler çalışma mantığı ve node group politikası
- Scale-up/down kısıtları (PDB, local storage, taint, limits)
- Doğrulama: pending pod → yeni node → schedule zinciri

## Workflow
- Altyapı modelini belirle:
  - Hangi node group/pool’lar ölçeklenebilir?
- Scale-up nedeni:
  - Pending pod gerçekten kaynak yetersizliğinden mi bekliyor?
- Scale-down engelleri:
  - PDB, daemonset, local PV, disruption kısıtları.
- Limitler:
  - Min/max node sayısı ve maliyet etkisi.
- Doğrulama:
  - Pending pod sonrası node geliyor mu?
  - İş bitince node güvenli şekilde küçülüyor mu?

## Common mistakes
- Scheduler constraint yüzünden pending kalan pod’u “kapasite yok” sanmak.
- Local storage kullanan node’ların kolayca silinebileceğini varsaymak.

## References
- `skills/k8s-scale-hpa`
- `skills/k8s-core-pod-disruption-budget`
