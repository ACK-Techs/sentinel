---
name: k8s-sec-network-policies-defense
description: Zero-trust yaklaşımıyla default-deny ağ katmanı kurmak, namespace izolasyonu tasarlamak veya savunma amaçlı policy stratejisini kademeli uygulamak gerektiğinde kullan. Amaç: **NetworkPolicy’yi tekil kural değil savunma katmanı olarak tasarlamaktır**.
---

## Purpose
Bu skill’in çıktısı:
- Default deny tabanı ve kademeli allow stratejisi
- Namespace/service sınır modellemesi
- Doğrulama: lateral movement’i sınırlayan test planı

## Workflow
- Savunma alanını tanımla:
  - Hangi namespace’ler birbirinden ayrılmalı?
- Default deny tabanı:
  - Ingress ve gerekirse egress’i kapat.
- Allow katmanları:
  - DNS, ingress controller, observability, app-to-app akışlarını tek tek aç.
- Gözlem:
  - Politika sonrası kırılan akışları hızlı teşhis edecek testler tanımla.
- Doğrulama:
  - İzinli ve yasaklı çapraz namespace erişimlerini dene.

## Common mistakes
- “Bir iki allow policy yazarım yeter” yaklaşımı: savunma modeli oluşmaz.
- Observability ve health probe akışlarını unutmak.

## References
- `skills/k8s-net-networkpolicy`
- `skills/k8s-net-egress-control`
