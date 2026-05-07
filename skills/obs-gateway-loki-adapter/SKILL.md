---
name: obs-gateway-loki-adapter
description: Observability gateway içinde Loki adapter katmanı yazmak (LogQL query, label/tenant izolasyonu, stream limitleri, yanıt formatlama) veya “gateway’den log gelmiyor/çok yavaş” sorununu çözmek gerektiğinde kullan. Odak: **Loki query semantiği + maliyet kontrolü**dür.
---

## Purpose
Bu skill’in çıktısı:
- Adapter sözleşmesi: hangi Loki query endpoint’leri, hangi parametreler forward/override ediliyor?
- Maliyet kontrolü: time range, limit, regex kısıtları, query timeout
- Doğrulama: dar selector ile hızlı sonuç + geniş sorguda güvenli hata/limit davranışı kanıtı

## Workflow
- API kapsamını seç:
  - Instant query mi, range query mi, tail benzeri endpoint mi?
- Tenant/izolasyon:
  - Tenant header’ı zorunlu mu? Upstream’e nasıl aktarılacak?
  - Cross-tenant sorgu engeli (hard fail).
- Parametre validasyonu:
  - Maks time range ve `limit` sınırı.
  - Regex kullanımında guardrail (aşırı pahalı pattern’ler).
- Yanıt formatlama:
  - Stream’leri normalize et (gerekirse); timestamp formatı tutarlı.
  - Partial result/hata modelini standartlaştır.
- Doğrulama:
  - Dar selector + kısa aralıkta 200 ve makul latency.
  - Limit aşımında deterministik error code + mesaj.

## Common mistakes
- Tail’i gateway’de açmak: sürekli bağlantı ve maliyet; genelde ayrı kanal gerekir.
- Label’ları gateway’de büyütmek: Loki kardinalitesi ve maliyet artar.

## References
- `skills/obs-gateway-rate-limiting`
- `skills/obs-gateway-retry-timeout`
