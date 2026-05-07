---
name: obs-gateway-openapi-spec
description: Observability gateway için OpenAPI şeması tanımlamak, adapter endpoint’lerini sözleşmeye dökmek ve client üretimini desteklemek gerektiğinde kullan. Odak: **API contract**, error model ve auth header’larının doğru ifade edilmesidir.
---

## Purpose
Bu skill’in çıktısı:
- OpenAPI’de endpoint/parametre/response şemaları (Prometheus/Loki/Tempo adapter’ları)
- Ortak bileşenler: auth header, tenant header, error model schema
- Doğrulama: spec lint + örnek client çağrısının doğru parametreleri üretebilmesi

## Workflow
- Kapsamı daralt:
  - Önce “core read API” (query/search) + health/status + auth.
- Ortak sözleşmeleri tanımla:
  - Security scheme (bearer token).
  - Tenant header parametresi (required).
  - Error model (tek yerde, tüm endpoint’ler referanslasın).
- Parametre detayları:
  - `start/end/step/limit` gibi parametrelerde format ve limitleri yaz.
  - Timeout/cancel semantiği (varsa) not et.
- Versioning:
  - `/api/v1` gibi path versiyonu; breaking change politikası.
- Doğrulama:
  - Spec’i lint et.
  - Otomatik üretilen client’ta auth ve tenant header zorunlu görünüyor mu?

## Common mistakes
- Error response’ları her endpoint’te farklı yazmak: client code karmaşası.
- Parametre limitlerini dokümante etmemek: prod’da sürpriz 400/413’ler.

## References
- `skills/obs-gateway-error-model`
- `skills/obs-gateway-auth-token`
