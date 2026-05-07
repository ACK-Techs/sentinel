---
name: obs-tempo-troubleshoot-ingest
description: “Tempo’ya trace gelmiyor” semptomunda ingestion zincirini (SDK → OTLP exporter → Collector → Tempo distributor/ingester → storage) adım adım izole etmek için kullan. Protokol uyumsuzluğu, sampling ve tenant header gibi en sık kök nedenleri hızlı ayırır.
---

## Purpose
Bu skill’in çıktısı:
- Semptom → olası neden → doğrulama adımı şeklinde kısa teşhis akışı
- Canary trace testi (tek request) ve Tempo’da arama adımı
- En sık 3 kök neden: sampling, yanlış endpoint/protokol, tenant header/ingress

## Workflow
- 0) “Trace üretiliyor mu?”
  - Uygulama SDK’sında tracer aktif mi, sampler `always_off` değil mi?
- 1) Export katmanı:
  - SDK OTLP exporter doğru endpoint’e gidiyor mu? (HTTP vs gRPC karışıklığı)
  - Collector kullanıyorsan: receiver gerçekten dinliyor mu?
- 2) Collector pipeline:
  - Batch/memory limiter yüzünden drop oluyor mu?
  - Tail sampling varsa: kurallar her şeyi elemiş olabilir.
- 3) Tempo receiver/distributor:
  - Tempo doğru protokolleri dinliyor mu? (OTLP/Jaeger/Zipkin)
  - Ingress/proxy gRPC’yi bozuyor mu?
- 4) Tenant (varsa):
  - Ingest ve query aynı tenant header’ı kullanıyor mu?
- 5) Storage:
  - Tempo “kabul ediyor” gibi ama blok yazamıyorsa storage izin/erişim sorunu olabilir.
- Canary kapanış:
  - Bilinçli canary request üret → Tempo’da service.name + kısa zaman penceresiyle ara.

## References
- `skills/obs-tempo-distributor-config`
- `skills/obs-tempo-sampling-strategy`
