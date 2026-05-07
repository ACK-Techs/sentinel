---
name: obs-otel-semantic-conventions
description: OpenTelemetry semantic conventions’ı uygulamak (http/db/rpc/messaging attribute adları, status kodları, span isimleri) veya “query yapamıyorum çünkü attribute isimleri tutarsız” sorununu düzeltmek gerektiğinde kullan. Odak: **adlandırma/alan standardı** ve sorgulanabilirliktir.
---

## Purpose
Bu skill’in çıktısı:
- Bir alan için (HTTP/DB/RPC/Messaging) canonical attribute listesi ve isimlendirme önerisi
- Span naming kuralı (ne “span adı”, ne “attribute” olmalı) ve anti-pattern’ler
- Doğrulama: Tempo/TraceQL veya backend’de attribute ile filtreleme yapılabildiğini kanıtlama

## Workflow
- Kullanım alanını seç (tek domain):
  - HTTP server/client, DB, RPC, messaging vb.
- Span adı kuralı:
  - Route/operation odaklı, düşük kardinalite (ham URL’yi span adı yapma).
- Attribute sözleşmesi:
  - Standart anahtar adlarını kullan; özel alanları namespace’le.
  - PII/secrets olabilecek alanları attribute’a koyma.
- Status ve error:
  - Error durumunda status=ERROR + hata mesajını kontrollü (maskeli) taşı.
- Uygulama planı:
  - Manuel SDK’da attribute set noktaları; auto-instrument varsa override ihtiyacı.
- Doğrulama:
  - Trace aramasında `service.name` + seçilen attribute ile filtreleme çalışıyor mu?

## Common mistakes
- Attribute adlarını “kendi key’imiz” ile uydurmak: query ve dashboard reuse bozulur.
- Yüksek kardinaliteyi attribute’a basmak (full URL, user id): maliyet ve gizlilik riski.

## References
- `skills/obs-otel-sdk-python`
- `skills/obs-otel-collector-processors`
