---
name: obs-tempo-jaeger-compat
description: Jaeger istemcileri/SDK’ları veya Jaeger UI ile uyumluluk gerektiğinde Tempo’yu Jaeger receiver üzerinden ingest edecek şekilde kurmak ve “Jaeger gönderiyor ama Tempo almıyor” sorununu gidermek için kullan. OTLP yerine Jaeger protokol uyumluluğuna odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Jaeger receiver’ın ne zaman gerekli olduğuna dair karar (mevcut agent/SDK kısıtları)
- Client’ın kullanacağı endpoint/port/protocol netliği (thrift/grpc gibi)
- Canary doğrulama: Jaeger tarafında gönder → Tempo’da trace’i bul

## Workflow
- Karar:
  - Yeni enstrümantasyonda OTLP tercih edilir; ama mevcut sistem Jaeger’e kilitliyse receiver aç.
- Protokol uyumluluğu:
  - Jaeger exporter hangi protokolü kullanıyor? (agent/collector vs direct)
  - Tempo tarafında aynı receiver açık mı?
- Ağ/ingress:
  - gRPC/TCP protokolü ingress tarafından bozuluyor mu?
  - Auth/TLS gerekiyorsa secret’ları düz metin yazma.
- Doğrulama:
  - Jaeger ile canary trace üret.
  - Tempo’da service.name + kısa zaman penceresiyle trace’i ara.

## Common mistakes
- Jaeger exporter protokolü ile Tempo receiver protokolünü karıştırmak.
- Ingress’in gRPC/TCP trafiğini HTTP gibi ele alması.

## References
- `skills/obs-tempo-distributor-config`
- `skills/obs-tempo-trace-query`
