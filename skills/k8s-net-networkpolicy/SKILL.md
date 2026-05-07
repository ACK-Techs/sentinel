---
name: k8s-net-networkpolicy
description: "Pod’lar arası ağ erişimini kısıtlamak, egress/ingress kuralları yazmak veya “policy ekledim, trafik niye kesildi?” sorunlarını çözmek gerektiğinde kullan. Amaç: **kime, hangi porttan, hangi yönde izin verildiğini açıkça tanımlamaktır**."
---

## Purpose
Bu skill’in çıktısı:
- Ingress/egress policy tasarımı
- PodSelector/NamespaceSelector/IPBlock seçimi
- Doğrulama: izinli ve yasaklı akışların test planı

## Workflow
- CNI desteğini doğrula:
  - Cluster gerçekten NetworkPolicy uyguluyor mu?
- Trafik matrisini çıkar:
  - Kim kiminle konuşmalı? hangi port/protocol?
- Policy’yi katmanla:
  - Önce default deny düşün.
  - Sonra gerekli allow listeleri ekle.
- Selector dikkatleri:
  - Label set’i stabil mi? namespace label’ları doğru mu?
- Egress:
  - DNS, object storage, external API erişimleri unutuluyor mu?
- Doğrulama:
  - Test pod ile hem izinli hem engelli akış dene.

## Common mistakes
- DNS egress’i unutup her şeyin “down” görünmesine neden olmak.
- Namespace selector’ın beklenenden fazla pod kapsaması.

## References
- `skills/k8s-sec-network-policies-defense`
- `skills/k8s-net-egress-control`
