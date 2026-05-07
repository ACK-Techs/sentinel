---
name: k8s-scale-node-affinity-spread
description: Pod’ları node/zone’lara dengeli yaymak, failure domain farkındalığı kurmak veya “tüm replica’lar aynı node’a yığılıyor” problemini çözmek gerektiğinde kullan. Amaç: **yerleşim tercihleri ile dağılım garantisini birlikte kurmaktır**.
---

## Purpose
Bu skill’in çıktısı:
- Node affinity ve topology spread kullanım sınırı
- Failure domain (node/zone) bazlı dağılım stratejisi
- Doğrulama: pod’lar beklenen şekilde yayılıyor mu?

## Workflow
- Hedefi ayır:
  - Belirli node özelliklerine gitmek mi, yoksa eşit dağılmak mı?
- Araç seç:
  - Node affinity: nereye gidebilir/gitmeli
  - Topology spread: nasıl dengeli dağıtılmalı
- Sertlik düzeyi:
  - Hard constraint mi, soft preference mı?
- Kapasite etkisi:
  - Aşırı sert kural scheduler’ı kilitler mi?
- Doğrulama:
  - Pod yerleşimi node/zone bazında dağılıyor mu?

## Common mistakes
- Sadece affinity yazıp spread beklemek.
- Replica sayısından daha fazla sert dağılım kuralı tanımlamak.

## References
- `skills/k8s-core-affinity-antiaffinity`
- `skills/k8s-core-taints-tolerations`
