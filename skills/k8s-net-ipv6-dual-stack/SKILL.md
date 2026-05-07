---
name: k8s-net-ipv6-dual-stack
description: "Kubernetes’te IPv6 veya dual-stack ağ kurmak, servis/pod CIDR planlamak veya “IPv4 çalışıyor, IPv6 neden bozuk?” sorunlarını çözmek gerektiğinde kullan. Amaç: **adresleme ve CNI/cluster uyumunu birlikte değerlendirmektir**."
---

## Purpose
Bu skill’in çıktısı:
- IPv6-only vs dual-stack kararı
- Pod/Service CIDR ve CNI uyumluluk kontrolü
- Doğrulama: pod adresleri, service resolution ve gerçek trafik testi

## Workflow
- Ortamı doğrula:
  - Altyapı, load balancer, ingress, CNI IPv6 destekli mi?
- Adres planı:
  - Pod CIDR ve Service CIDR’ler çakışmasız mı? IPv4 ile birlikte mi çalışacak?
- Uygulama etkisi:
  - App’ler listen/bind davranışında IPv6 uyumlu mu?
- DNS ve service davranışı:
  - AAAA/A kayıtları nasıl dönecek?
- Doğrulama:
  - Pod’lar iki stack de alıyor mu?
  - Service ve ingress üzerinden her iki stack’ten erişim var mı?

## Common mistakes
- Cluster dual-stack ama upstream network tek-stack: yarım kurulum olur.
- IP planını sonradan düşünmek: migration çok pahalılaşır.

## References
- `skills/k8s-net-pod-cidr`
- `skills/microk8s-install-base`
