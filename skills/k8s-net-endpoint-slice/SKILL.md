---
name: k8s-net-endpoint-slice
description: Büyük servislerde backend endpoint ölçeklenmesini anlamak, service arkasındaki endpoint dağılımını incelemek veya “trafik bazı pod’lara gitmiyor” durumlarını çözmek gerektiğinde kullan. Amaç: **Service → EndpointSlice ilişkisinin davranışını okumaktır**.
---

## Purpose
Bu skill’in çıktısı:
- EndpointSlice’in neden var olduğu ve klasik Endpoints’ten farkı
- Service selector ile oluşan slice’ların okunması
- Doğrulama: pod üyeliği ve readiness durumunun endpoint’e yansıması

## Workflow
- Service’i doğrula:
  - Selector doğru mu? pod’lar ready mi?
- EndpointSlice oku:
  - Hangi address’ler var, ready/serving/terminating durumları ne?
- Ölçek etkisi:
  - Çok sayıda pod’da slice parçalanması normal mi?
- Sorun analizi:
  - Pod çalışıyor ama endpoint’te yoksa readiness/selector sorunu.
  - Endpoint var ama trafik yoksa kube-proxy/service path kontrolü.
- Doğrulama:
  - Service arkasındaki pod listesi ile slice üyeliği eşleşiyor mu?

## Common mistakes
- “Pod running ise service trafiği alır” varsayımı: readiness kırık olabilir.
- EndpointSlice’i hiç kontrol etmeden Ingress’i suçlamak.

## References
- `skills/k8s-net-service-types`
- `skills/k8s-core-pod-lifecycle`
