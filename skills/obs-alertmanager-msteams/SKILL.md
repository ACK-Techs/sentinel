---
name: obs-alertmanager-msteams
description: Alertmanager’dan Microsoft Teams’e bildirim göndermek ve Adaptive Card içeriğini “okunabilir + aksiyon alınabilir” hale getirmek gerektiğinde kullan. Odak: Teams webhook, kart alanları, linkler ve delivery hata modları.
---

## Purpose
Bu skill’in çıktısı:
- Teams receiver/webhook entegrasyon planı (webhook URL maskeli)
- Adaptive Card içerik şablonu: başlık/özet/alert listesi/linkler
- Doğrulama: test alert’i ile Teams’te kart render ve linklerin çalışması

## Workflow
- Kanal ve gürültü politikasını belirle:
  - Page mı notify mı? Teams genelde notify; page için ayrı kanal kullan.
- Secret hijyen:
  - Teams webhook URL’sini config’e düz yazma; secret store/ENV ile yönet.
- Kart içeriği:
  - Başlık: severity + service + durum.
  - Gövde: ilk 3–5 alert özeti + “+N more”.
  - Linkler: runbook, dashboard, silence.
- Hata modu:
  - 4xx: webhook/format hatası.
  - 429: rate limit; grouping’i güçlendir.
- Doğrulama:
  - Test alert’i ile kartı gönder; render bozuluyor mu kontrol et.

## Common mistakes
- Teams’i page kanalı gibi kullanmak: rate limit ve gürültü.
- Uzun label dump’ı: kart taşar, okunmaz olur.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
- `skills/obs-alertmanager-receivers`
