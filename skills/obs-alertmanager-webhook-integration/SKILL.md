---
name: obs-alertmanager-webhook-integration
description: Alertmanager webhook receiver ile özel bir handler’a alert göndermek (payload kontratı, retry/timeout, imza/secret doğrulama) veya “webhook 2xx dönüyor ama işlenmiyor” sorununu çözmek gerektiğinde kullan. Hedef: güvenli ve idempotent entegrasyon.
---

## Purpose
Bu skill’in çıktısı:
- Webhook receiver YAML snippet’i (timeout/retry ve secret stratejisi dahil)
- Handler tarafı için payload kontratı + idempotency anahtarı önerisi
- Doğrulama: test alert’i ile uçtan uca delivery + handler log’larında işleme kanıtı

## Workflow
- Entegrasyon hedefini tanımla:
  - Handler ne yapacak? (ticket aç, incident başlat, CMDB update)
  - 2xx response ne anlama geliyor? (kabul edildi mi işlendi mi?)
- Güvenlik:
  - Paylaşılan secret ile imza/HMAC veya header token (secret’ı config’e gömme).
  - Handler endpoint’ini internal ağda tut; allowlist uygula.
- Idempotency:
  - Aynı notification birden fazla gelebilir; `fingerprint`/group key ile idempotent işle.
- Timeout ve hata davranışı:
  - Handler yavaşsa timeout/queue ekle; Alertmanager’ın retry davranışını hesaba kat.
  - 4xx/5xx ayrımını netleştir (retry edilmeli mi?).
- Doğrulama:
  - Test alert’i gönder; handler log’unda request body ve karar görülsün (PII maskele).
  - Aynı alert tekrarlandığında duplicate işlem yapılmadığını doğrula.

## Common mistakes
- Webhook’u “exactly once” sanmak: en az bir kez teslim modeliyle tasarla.
- Secret’ı URL içine koymak: log sızıntısı.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
