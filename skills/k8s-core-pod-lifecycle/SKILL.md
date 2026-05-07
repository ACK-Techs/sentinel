---
name: k8s-core-pod-lifecycle
description: Kubernetes Pod yaşam döngüsünü anlamlandırmak ve probe’ları (startup/readiness/liveness) doğru tasarlamak veya “CrashLoopBackOff”, “Ready değil ama çalışıyor”, “trafik erken geliyor” gibi sorunları çözmek gerektiğinde kullan. Odak: **probe semantiği + lifecycle olayları**.
---

## Purpose
Bu skill’in çıktısı:
- Pod lifecycle teşhis çerçevesi (Pending→Running→Succeeded/Failed + restart)
- Probe tasarımı: hangi probe neyi ölçer, hangi eşikler uygundur?
- Doğrulama: `kubectl describe pod` + event’lerle probe davranışını kanıtlama

## Workflow
- Semptomu sınıflandır:
  - CrashLoopBackOff (process exit)
  - Running ama Ready değil (readiness fail)
  - Restart yok ama trafik kesiliyor (liveness yanlış)
- Probe seçimi:
  - `startupProbe`: soğuk başlangıç/DB migration gibi uzun init için.
  - `readinessProbe`: “trafik alabilir mi?” (dependency hazır mı? cache warm mı?)
  - `livenessProbe`: “process kilitlendi mi?” (çok agresif olmasın).
- Eşik tasarımı:
  - `timeoutSeconds`, `periodSeconds`, `failureThreshold` değerlerini uygulama davranışına göre seç.
  - Readiness fail = trafik kesilir; liveness fail = restart olur (risk farklı).
- Anti-pattern kontrolü:
  - Liveness’ı dependency check gibi kullanma (DB down → restart storm).
  - Readiness’ı “CPU yüksek” gibi metrikle bağlama (flap).
- Doğrulama:
  - Pod event’lerinde probe failure mesajı var mı?
  - Uygulama log’larında probe endpoint erişimi ve latency ölç.

## References
- `skills/k8s-core-events-audit`
- `skills/k8s-core-resource-requests-limits`
