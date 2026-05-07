---
name: obs-otel-baggage
description: OpenTelemetry Baggage ile servisler arası taşınan context anahtarlarını tasarlamak (hangi key’ler, boyut limiti, gizlilik) veya “baggage büyüdü, header şişti, PII sızıyor” gibi riskleri yönetmek gerektiğinde kullan. Trace context’ten farklı olarak **taşınan iş bağlamı** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Baggage key sözleşmesi (ör. tenant, request-origin) ve “asla koyma” listesi
- Propagation ve scrubbing planı (nerede eklenir/nerede silinir)
- Doğrulama: bir request zincirinde baggage’ın doğru taşındığı ve limitleri aşmadığı kanıtı

## Workflow
- Baggage ihtiyacını doğrula:
  - Bu bilgi trace attribute olarak mı kalmalı, yoksa downstream’e taşınmalı mı?
- Key tasarımı:
  - Az sayıda key; düşük kardinalite; açık isimlendirme (namespace).
- Gizlilik ve boyut:
  - PII/secrets yasak; header boyutu limitlerine dikkat (proxy/gateway).
- Eklenme/silinme noktaları:
  - Entry service’de set et; sınır servislerinde scrub et.
  - Collector processor ile drop/sanitize gerekiyorsa yaz.
- Doğrulama:
  - Bir request’i zincir boyunca takip et; downstream servis log/trace’inde baggage key’leri görünüyor mu?

## Common mistakes
- User id/email gibi PII’yi baggage’a koymak: her servise sızar.
- Çok fazla key taşımak: header şişer, bazı proxy’ler request’i drop eder.

## References
- `skills/obs-otel-context-propagation`
- `skills/obs-otel-collector-processors`
