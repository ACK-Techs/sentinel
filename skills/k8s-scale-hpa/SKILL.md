---
name: k8s-scale-hpa
description: Horizontal Pod Autoscaler kurmak, CPU/memory veya custom metric’e göre pod sayısını ayarlamak ya da “HPA neden scale etmiyor/zıplıyor?” sorunlarını çözmek gerektiğinde kullan. Amaç: **ölçekleme sinyalini uygulama davranışıyla eşleştirmektir**.
---

## Purpose
Bu skill’in çıktısı:
- HPA hedef metriği ve threshold seçimi
- Min/max replica ve stabilizasyon kararı
- Doğrulama: yük altında beklenen scale davranışı

## Workflow
- Sinyali seç:
  - CPU mu, memory mi, custom metric mi? gerçekten kullanıcı yükünü temsil ediyor mu?
- Limitleri koy:
  - `minReplicas`, `maxReplicas`, target utilization/value.
- Stabilite:
  - Ani zıplamaları önlemek için behavior/stabilization düşün.
- Önkoşul:
  - Metrics Server veya custom metrics pipeline hazır mı?
- Doğrulama:
  - Yük testi sırasında replica sayısı ve latency birlikte izlenmeli.

## Common mistakes
- Memory’yi her uygulama için iyi autoscaling sinyali sanmak.
- HPA’yı request/limit ayarlarından bağımsız düşünmek.

## References
- `skills/k8s-scale-custom-metrics-api`
- `skills/k8s-core-resource-requests-limits`
