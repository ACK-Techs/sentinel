---
name: k8s-net-service-types
description: ClusterIP, NodePort ve LoadBalancer servis tipleri arasında doğru seçimi yapmak veya “servise dışarıdan/cluster içinden neden erişemiyorum?” problemini çözmek gerektiğinde kullan. Amaç: **servis erişim modelini iş ihtiyacına göre seçmektir**.
---

## Purpose
Bu skill’in çıktısı:
- Service type seçimi ve gerekçesi
- Port/targetPort/external access modeli
- Doğrulama: pod → service → client erişim zinciri

## Workflow
- Tüketiciyi belirle:
  - Sadece cluster içi mi? dış istemci var mı? sabit IP lazım mı?
- Tip seçimi:
  - ClusterIP: internal traffic
  - NodePort: basit dış erişim / geçici test
  - LoadBalancer: gerçek dış erişim + entegrasyon
- Port eşlemesi:
  - `port`, `targetPort`, gerekiyorsa `nodePort` çakışmasız mı?
- Selector ve endpoint:
  - Service gerçekten doğru pod’lara bağlanıyor mu?
- Doğrulama:
  - Endpoints dolu mu?
  - Cluster içinden DNS ile eriş.
  - Dış erişim gerekiyorsa LB IP veya node port yolu çalışıyor mu?

## Common mistakes
- Ingress varken uygulamaya doğrudan NodePort açmak: gereksiz yüzey.
- Service var ama selector yanlış: boş endpoint.

## References
- `skills/k8s-net-ingress-controller`
- `skills/k8s-net-metallb`
