---
name: k8s-core-resource-requests-limits
description: Pod resource request/limit değerlerini belirlemek, QoS class etkisini anlamak veya “OOMKilled”, “CPU throttling”, “node’da yer yok” sorunlarını çözmek gerektiğinde kullan. Odak: **kaynak bütçesi + performans riski** ve doğrulamadır.
---

## Purpose
Bu skill’in çıktısı:
- Requests/limits öneri seti (başlangıç + ölçümle ayarlama yaklaşımı)
- QoS sınıfı analizi (Guaranteed/Burstable/BestEffort) ve OOM risk notları
- Doğrulama: throttling/oom metrikleri ve pod events ile “doğru ayar” kanıtı

## Workflow
- İş yükünü sınıflandır:
  - CPU-bound mı, memory-bound mı, bursty mi?
- Requests belirle:
  - Scheduling garantisi için minimum stabil değeri set et.
  - Requests yoksa cluster “BestEffort” davranışına düşer; riskleri yaz.
- Limits belirle:
  - Memory limit: OOMKilled riskini yönetir (çok düşükse sürekli restart).
  - CPU limit: throttling yaratabilir; latency-sensitive servislerde dikkat.
- QoS etkisi:
  - Requests=limits (CPU+mem) → Guaranteed.
  - Sadece requests → Burstable.
  - Hiçbiri → BestEffort.
- Doğrulama:
  - Pod events: OOMKilled var mı?
  - CPU throttling metrikleri var mı?
  - Node pressure (memory/cpu) altında davranış nasıl?

## Common mistakes
- Memory limit’i “küçük olsun” diye düşük koymak: production CrashLoop.
- CPU limit’i agresif koyup latency spike’larını “uygulama bug’ı” sanmak.

## References
- `skills/k8s-core-events-audit`
- `skills/k8s-scale-hpa`
