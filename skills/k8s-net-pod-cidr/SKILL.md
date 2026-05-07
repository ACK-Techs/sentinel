---
name: k8s-net-pod-cidr
description: "Pod CIDR ve Service CIDR planlamak, ağ aralığı çakışmalarını önlemek veya “VPN/LAN ile cluster ağı çatışıyor” sorunlarını çözmek gerektiğinde kullan. Amaç: **cluster adres alanını kurulumdan önce doğru seçmektir**."
---

## Purpose
Bu skill’in çıktısı:
- Pod/Service CIDR planı ve ayrım gerekçesi
- Mevcut LAN/VPN/cloud ağlarıyla çakışma analizi
- Doğrulama: route ve connectivity kontrolü

## Workflow
- Mevcut ağları topla:
  - Ev/ofis LAN, VPN, cloud VPC, başka cluster CIDR’leri.
- CIDR seç:
  - Pod ve Service aralıkları birbirinden ve dış ağlardan ayrık olsun.
- Büyüme payı:
  - Node/pod sayısına göre yeterli blok seç.
- Teknoloji etkisi:
  - CNI ve kube-proxy davranışına göre route planını değerlendir.
- Doğrulama:
  - Pod IP’leri ve Service IP’leri beklenen bloktan geliyor mu?
  - VPN açıkken erişim kırılıyor mu?

## Common mistakes
- “Şimdilik rastgele 10.x seçelim” yaklaşımı: ileride çakışma çıkar.
- Service CIDR’yi unutmak.

## References
- `skills/k8s-net-ipv6-dual-stack`
- `skills/k8s-net-calico-flannel`
