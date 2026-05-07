---
name: k8s-net-egress-control
description: Pod’ların dış dünyaya çıkışını sınırlamak, belirli endpoint’lere izin vermek veya “internet erişimini kapattım, hangi bağımlılıklar kırılır?” sorusunu yönetmek gerektiğinde kullan. Amaç: **egress’i bilinçli allow-list mantığıyla tasarlamaktır**.
---

## Purpose
Bu skill’in çıktısı:
- Egress allow-list yaklaşımı
- DNS, package mirror, API bağımlılıkları gibi kaçırılan çıkışların listesi
- Doğrulama: izinli/engelli çıkış test planı

## Workflow
- Bağımlılıkları dök:
  - Uygulama hangi dış endpoint’lere çıkıyor? DNS? object storage? payment API?
- Kontrol seviyesini seç:
  - Namespace policy mi, dedicated egress gateway mi?
- Policy yaz:
  - Önce default deny, sonra hedef allow’lar.
  - IP tabanlı mı, namespace/service tabanlı mı?
- Operasyonel risk:
  - Paket kurulumu, time sync, telemetry export gibi gizli çıkışları unutma.
- Doğrulama:
  - Test pod ile izinli ve yasaklı bağlantıları dene.

## Common mistakes
- Sadece uygulama API’lerini düşünüp DNS’i unutmak.
- CIDR allow verip hedef servislerin IP değişimini hesaba katmamak.

## References
- `skills/k8s-net-networkpolicy`
- `skills/k8s-sec-network-policies-defense`
