---
name: k8s-net-service-mesh-intro
description: Service mesh ihtiyacını değerlendirmek, Istio/Linkerd gibi çözümlere giriş yapmak veya “mTLS / traffic policy / observability için mesh gerekli mi?” sorusunu cevaplamak gerektiğinde kullan. Amaç: **mesh’i problem çözümü üzerinden değerlendirmektir**, moda üzerinden değil.
---

## Purpose
Bu skill’in çıktısı:
- Mesh’e gerçekten ihtiyaç olup olmadığına dair kısa karar çerçevesi
- Sidecar/data plane/control plane kavram ayrımı
- İlk benimseme riskleri: operasyon yükü, latency, debug karmaşıklığı

## Workflow
- İhtiyacı test et:
  - mTLS, traffic split, retries, policy, service identity gereksinimi var mı?
- Mesh bileşenlerini ayır:
  - Control plane ne yönetir, data plane nerede çalışır?
- Benimseme maliyeti:
  - Sidecar overhead, cert management, debug zorluğu, policy drift.
- Linkerd vs Istio gibi yönleri problem üzerinden tart:
  - Hafiflik mi, geniş özellik mi?
- Doğrulama:
  - Pilot use-case belirle; tüm cluster’a bir anda yayma.

## Common mistakes
- Sadece “observability lazım” diye mesh eklemek: OTel/ingress zaten yeterli olabilir.
- mTLS isteyip sertifika yaşam döngüsünü planlamamak.

## References
- `skills/k8s-sec-network-encryption-mtls`
- `skills/obs-tempo-service-graph`
