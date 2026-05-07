---
name: obs-gateway-tempo-adapter
description: Observability gateway içinde Tempo adapter katmanı yazmak (TraceQL/query, trace by id, tenant izolasyonu, span detay dönüşümü) veya “trace araması gateway’de timeout oluyor / tenant karışıyor” sorunlarını çözmek gerektiğinde kullan. Odak: **trace query performansı + güvenli yanıt**tır.
---

## Purpose
Bu skill’in çıktısı:
- Adapter kapsamı: trace by ID + TraceQL arama endpoint’leri ve parametre sözleşmesi
- Performans guardrail’leri: time range, limit, search parametre kısıtları
- Doğrulama: kısa aralıkta trace bulma + yanlış tenant’ta erişim engeli kanıtı

## Workflow
- API kapsamını seç:
  - Trace ID ile get (deterministik).
  - TraceQL search (pahalı olabilir).
- Tenant ve güvenlik:
  - Tenant header zorunlu; upstream’e aktarım.
  - Trace attribute’larında PII olasılığı: response redaction ihtiyacını değerlendir.
- Parametre validasyonu:
  - Search time range limit; sonuç sayısı limit.
  - Timeout ve cancellation: client abort’ta upstream çağrıyı kes.
- Yanıt dönüşümü:
  - Gateway’in döndüğü “span detay” formatını sabitle (sadece gerekli alanlar).
  - Büyük trace’lerde pagination/partial stratejisi (varsa).
- Doğrulama:
  - Trace ID ile hızlı 200.
  - TraceQL’de limit/timeout guardrail çalışıyor mu?
  - Tenant mismatch → 403.

## Common mistakes
- TraceQL’yi guardrail’siz açmak: pahalı sorgular gateway’i kilitler.
- Tenant izolasyonunu sadece “UI” seviyesinde bırakmak: veri sızıntısı riski.

## References
- `skills/obs-gateway-auth-token`
- `skills/obs-gateway-error-model`
