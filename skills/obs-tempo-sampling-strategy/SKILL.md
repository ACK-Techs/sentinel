---
name: obs-tempo-sampling-strategy
description: Trace sampling stratejisi belirlemek (head vs tail) veya OpenTelemetry Collector’da tail-sampling kuralı yazmak gerektiğinde kullan. “Neden bazı trace’ler yok?”, “sadece hatalı/yavaş istekleri sakla”, “maliyet düşür” gibi sampling odaklı konular için.
---

## Purpose
Bu skill’in çıktısı:
- Head vs tail sampling seçimi ve gerekçesi (fidelity vs maliyet vs gecikme)
- Tail sampling için kural fikri (ör. error status, latency threshold, route allowlist)
- Sampling yüzünden “trace yok” semptomunu teşhis etmek için kontrol listesi

## Workflow
- Hedefi netleştir:
  - Amaç “genel görünürlük” mü (örnekleme düşük ama temsilî), yoksa “sadece kötü istekler” mi?
- Seçim:
  - **Head sampling**: SDK tarafında hızlı karar; düşük maliyet; ama “kötü trace’i kaçırma” riski.
  - **Tail sampling**: tüm trace’i görüp karar verir; error/slow odaklı iyi; ama collector kaynak + gecikme maliyeti var.
- Tail sampling kuralı tasarla:
  - “Mutlaka sakla”: `status=ERROR` veya `http.status_code>=500`
  - “Yavaş sakla”: duration > eşik
  - “Geri kalanı düşük oranla”: baseline sample rate
  - Kardinalite tuzağı: route/path kuralını normalize et (dinamik path ile kural yazma).
- Doğrulama:
  - Canary error ve canary success request üret; error trace’in geldiğini, success’in sample rate’e uyduğunu kontrol et.
- “Trace yok” teşhisi:
  - Sampling mi, export pipeline mı, tempo ingest mi? (katmanı ayır)
  - SDK tarafında sampler kapalı mı? (always_off) yanlış mı?

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
