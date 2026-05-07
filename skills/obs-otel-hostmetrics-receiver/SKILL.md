---
name: obs-otel-hostmetrics-receiver
description: OpenTelemetry Collector `hostmetrics` receiver ile node seviyesinde CPU/memory/disk/network metriklerini toplamak veya “host metrics eksik/yanlış/çok pahalı” sorunlarını çözmek gerektiğinde kullan. Node exporter değil; **Collector hostmetrics ölçüm seti ve frekansı** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- `hostmetrics` receiver için metric set seçimi (cpu/memory/filesystem/network/process) ve interval önerisi
- Kardinalite ve maliyet kontrolü (process metrics, mount point patlaması)
- Doğrulama: backend’de 2–3 kritik host metriğinin görünürlük kanıtı

## Workflow
- Yerleşimi belirle:
  - DaemonSet/agent modeli (her node) hedeflenir.
- Metric set seç:
  - Başlangıç: cpu + memory + filesystem + network.
  - `process`/`processes` gibi yüksek hacimli set’leri gerekçe olmadan açma.
- Interval kararı:
  - 10s çok agresif olabilir; 30s/60s çoğu host metriği için yeterli.
- Filtreleme:
  - Filesystem için tmpfs/overlay gibi mount’ları exclude et.
  - Network interface’lerini (lo, veth gürültüsü) filtreleme ihtiyacını değerlendir.
- Doğrulama:
  - Collector exporter sent artıyor mu?
  - Grafana’da CPU/memory grafiği beklenen node sayısında görünüyor mu?

## Common mistakes
- Tüm process metriklerini açmak: kardinalite ve maliyet hızla büyür.
- Filesystem mount’larını filtrelememek: binlerce seri ve anlamsız grafikleri üretir.

## References
- `skills/obs-otel-collector-pipeline`
- `skills/obs-prometheus-labels-strategy`
