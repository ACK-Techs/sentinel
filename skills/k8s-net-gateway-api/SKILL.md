---
name: k8s-net-gateway-api
description: "Kubernetes Gateway API ile L4/L7 trafik yönetimi kurmak veya Ingress’in yetmediği rota/policy ihtiyaçlarını çözmek gerektiğinde kullan. Amaç: **Gateway, Listener ve Route ayrımını doğru kurmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- GatewayClass/Gateway/HTTPRoute ilişki şeması
- Listener ve route attachment tasarımı
- Doğrulama: route gerçekten doğru gateway/listener’a bağlanıyor mu?

## Workflow
- Mimariyi ayır:
  - Altyapı ekibi Gateway’i mi yönetiyor, uygulama ekibi Route’u mu?
- Gateway tanımı:
  - Hangi listener’lar var? hostnames/TLS nerede?
- Route bağlama:
  - HTTPRoute parentRefs doğru mu?
  - Cross-namespace attachment policy gerekiyor mu?
- Gelişmiş ihtiyaç:
  - Header match, weighted backend, shared gateway gibi use-case’leri ayrı düşün.
- Doğrulama:
  - Status conditions attached/programmed mı?
  - Test isteği doğru backend’e gidiyor mu?

## Common mistakes
- Ingress düşünme modeliyle Gateway API kullanmak: role separation kaçırılır.
- Route status’a bakmadan YAML apply sonrası “bitti” sanmak.

## References
- `skills/k8s-net-ingress-controller`
- `skills/cos-ingress-config`
