---
name: obs-otel-collector-scaling
description: OpenTelemetry Collector’ı yatay ölçeklemek (agent/gateway ayrımı, sharding, load balancing) veya “tek collector CPU’da boğuluyor / kuyruk doluyor” sorununu çözmek gerektiğinde kullan. Odak: throughput, backpressure ve deterministik shard stratejisidir.
---

## Purpose
Bu skill’in çıktısı:
- Ölçekleme planı: agent vs gateway rol dağılımı + hangi sinyal nerede toplanır
- Sharding stratejisi (service/tenant/hash) ve risk analizi (hot shard, order)
- Doğrulama: ölçek sonrası dropped/queue metriklerinde iyileşme kanıtı

## Workflow
- Darboğazı kanıtla:
  - CPU/RAM, queue size, exporter retry, dropped counts (telemetry).
- Mimariyi seç:
  - Agent: node’a yakın ingestion (logs/host metrics).
  - Gateway: central fan-in + routing + auth.
- Sharding kararı:
  - Hash key: `service.name` veya tenant gibi stabil alan.
  - Hot shard riskini değerlendir (tek servis çok trafik).
- Load balancing:
  - OTLP için LB exporter/receiver desenini seç; sticky ihtiyacını yaz (tail sampling varsa).
- Doğrulama:
  - P95 ingest latency, dropped ve queue metriği düşüyor mu?

## Common mistakes
- Tail sampling varken stateless LB yapmak: trace parçalanabilir.
- “Sadece replica artır” yaklaşımı: shard yoksa aynı problem tekrar eder.

## References
- `skills/obs-otel-sampling-config`
- `skills/obs-gateway-rate-limiting`
