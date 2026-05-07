---
name: obs-alertmanager-receivers
description: Alertmanager’da receiver tanımlamak (Slack/email/webhook/PagerDuty/Opsgenie) veya “bildirim gitmiyor/format bozuk” sorununu çözmek gerektiğinde kullan. Routing değil; **delivery ve message formatı** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Seçilen kanal için receiver YAML snippet’i (secret’lar maskeli/ENV referanslı)
- Mesaj/başlık şablonu önerisi (kısa, aksiyon odaklı; runbook linkli)
- Doğrulama: test alert’i ile delivery ve template’in doğru çalıştığını kanıt

## Workflow
- Kanalı ve beklentiyi seç:
  - “Page” (7/24) mı “Notify” (iş saati) mi? Aynı receiver olmasın.
- Secret hijyen:
  - Webhook URL/token/SMTP password değerlerini dosyaya düz yazma.
  - Nereden gelecek? (K8s Secret / Juju secret / ENV) açık belirt.
- Payload tasarımı:
  - Minimum alanlar: özet, service, severity, env, fingerprint, runbook link.
  - Grup bildiriminde “kaç alert var?” bilgisini ekle.
- Hata modu teşhisi:
  - 401/403 → auth.
  - Timeout → ağ/DNS/proxy.
  - 429 → rate limit/backoff.
- Doğrulama:
  - Test alert’i ile receiver’a delivery.
  - UI/receiver log’larında template render hatası var mı kontrol et.

## Common mistakes
- Aynı receiver’ı hem page hem notify için kullanmak: yanlış zamanda yanlış kanaldan uyarı.
- Secret’ı config’e gömmek: sızıntı ve rotasyon zorluğu.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
