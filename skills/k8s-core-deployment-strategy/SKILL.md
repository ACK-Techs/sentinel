---
name: k8s-core-deployment-strategy
description: Kubernetes Deployment için rolling update/canary stratejisi ve `maxSurge`/`maxUnavailable` ayarlarını tasarlamak veya “rollout yavaş/servis kesiliyor/kapasite yetmiyor” sorunlarını çözmek gerektiğinde kullan. Odak: **trafik sürekliliği + kapasite**.
---

## Purpose
Bu skill’in çıktısı:
- RollingUpdate parametre seti (surge/unavailable) ve kapasite gerekçesi
- Canary yaklaşımı: nasıl “az trafik → genişlet” yapılır? (k8s-native veya gateway/ingress)
- Doğrulama: rollout sırasında Ready pod sayısı ve error rate’in stabil kaldığı kanıt

## Workflow
- Kısıtları yaz:
  - Minimum kapasite (kaç replica şart?)
  - Node kapasitesi: surge için yer var mı?
  - Startup süresi: readiness geç mi geliyor?
- RollingUpdate ayarları:
  - `maxUnavailable`: kesinti toleransı (0 ise güvenli ama yavaş olabilir).
  - `maxSurge`: ekstra kapasite (cluster yerin var mı?).
- Canary planı:
  - Ayrı Deployment + label selector ile trafik bölme (ingress/service mesh/gateway).
  - Geri dönüş kriteri: error rate, latency, crashloop.
- Operasyon:
  - `progressDeadlineSeconds` ve `minReadySeconds` ayarlarını startup davranışına göre belirle.
- Doğrulama:
  - Rollout sırasında `kubectl rollout status` + pod readiness trend’i.
  - Metriklerde (5xx, latency) spike var mı?

## Common mistakes
- `maxUnavailable=0` + yetersiz cluster kapasitesi: rollout kilitlenir.
- Canary’yi “aynı service altında” kontrolsüz yapmak: iki sürüm karışır, debug zorlaşır.

## References
- `skills/k8s-core-pod-lifecycle`
- `skills/k8s-scale-hpa`
