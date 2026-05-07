---
name: obs-otel-collector-processors
description: OpenTelemetry Collector’da processor’ları doğru seçmek ve doğru sıraya koymak (batch, memory_limiter, attributes, filter, transform/sampling) gerektiğinde kullan. Odak: veri hacmi/PII kontrolü ve “processor yüzünden sinyal düştü” hatalarını önlemek.
---

## Purpose
Bu skill’in çıktısı:
- Processor set’i önerisi (minimum güvenli set + ihtiyaca göre ekler)
- Sıra (ordering) kararı ve nedenleri (örn. memory_limiter erken, batch sonda)
- Doğrulama: dropped/filtered metrikleriyle etkisini ölçme

## Workflow
- Hedefi belirle:
  - Maliyet düşürmek mi (drop), zenginleştirmek mi (attrs), güvenlik mi (PII scrub), stabilite mi (memory)?
- Minimum güvenli set:
  - `memory_limiter` + `batch` (çoğu pipeline için).
- Attribute yönetimi:
  - `attributes`/`transform`: gerekli resource attribute’larını ekle/normalize et (service.name, env).
  - PII riski olan attribute’ları sil (örn. kullanıcı id/email).
- Filtreleme:
  - Gürültü loglarını veya healthcheck span’larını drop et (dar matcher ile).
  - Filtreyi önce staging’de dene; yanlış filtre “sessiz veri kaybı”dır.
- Sampling (trace):
  - Head/tail sampling ihtiyacını ayrı karar olarak yaz; yanlış sampling incident’ı görünmez kılar.
- Sıra (genel yaklaşım):
  - Koruyucular erken (memory limiter), şekillendirme ortada (attrs/filter), batch sonda.
- Doğrulama:
  - Collector telemetry’de “dropped/filtered/sent” metriklerini kontrol et.

## Common mistakes
- Filtreyi çok geniş yazmak: geri dönüşü zor veri kaybı.
- Processor ekleyip gözlemlememek: etkiyi ölçmeden prod’a çıkmak.

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
