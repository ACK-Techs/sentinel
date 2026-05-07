---
name: obs-otel-prometheus-receiver
description: Mevcut Prometheus scrape yapılandırmalarını OpenTelemetry Collector `prometheus` receiver ile “bridge” etmek (scrape → OTLP pipeline → remote_write/OTLP exporter) veya “scrape çalışıyor ama downstream’e gitmiyor” sorununu çözmek gerektiğinde kullan. Prometheus server değil; **Collector içinde scrape** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Prometheus receiver scrape_config iskeleti (targets, relabel, interval) ve pipeline’a bağlama
- Prometheus→OTel dönüşüm riskleri (label mapping, histograms) için notlar
- Doğrulama: receiver accepted + exporter sent metrikleriyle uçtan uca kanıt

## Workflow
- Bridge gerekçesini yaz:
  - Tek collector üzerinden normalize/route mu istiyorsun, yoksa Prometheus yeterli mi?
- Scrape konfigürasyonu:
  - Var olan `scrape_configs`’ten taşınacak job’ları seç.
  - Relabel ile hedef set’i daralt; kardinaliteyi patlatma.
- Dönüşüm/işleme:
  - Resource attribute’lara map ihtiyacı var mı? (service.name/env)
  - Histogram dönüşümü bekleniyor mu?
- Export:
  - Remote_write mı, OTLP metrics mi? Backend beklentisini sabitle.
- Doğrulama:
  - Collector telemetry: scrape edilen seri sayısı ve exporter sent.
  - Backend’de `up` benzeri sinyal veya beklenen metrik adı görünüyor mu?

## Common mistakes
- Prometheus receiver’ı gateway’de “her şeyi scrape et” diye açmak: scaling zorlaşır.
- Relabel/filter olmadan scrape: kardinalite maliyeti artar.

## References
- `skills/obs-prometheus-scrape-config`
- `skills/obs-otel-collector-exporters`
