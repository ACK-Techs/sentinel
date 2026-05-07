---
name: obs-alertmanager-slack-template
description: Alertmanager’dan Slack’e giden mesajların template’ini iyileştirmek (özet, grup içeriği, linkler, mention politikası) gerektiğinde kullan. Hedef “okunabilir ve aksiyon alınabilir” Slack bildirimi; routing/receiver kurulumu ayrı konudur.
---

## Purpose
Bu skill’in çıktısı:
- Slack template taslağı: başlık + kısa özet + grup içi alert listesi + linkler
- Mention stratejisi: `@channel`/user mention sadece page severity’de
- Doğrulama: örnek grouped alert mesajında bilgi yoğunluğu ve uzunluk kontrolü

## Workflow
- Mesaj hedefini tanımla:
  - Page mi notify mı? (page: kısa ve net; notify: daha fazla bağlam)
- İçerik sözleşmesi:
  - Başlık: `severity` + `service` + “kaç alert” + durum (firing/resolved).
  - Gövde: ilk 3–5 alert’i listele; fazlasını “+N more”.
  - Linkler: runbook, dashboard, silence/create linki (varsa).
- Mention politikası:
  - Mention’ı severity’ye bağla; resolved mesajlarında mention yapma.
- Gürültü kontrolü:
  - Label dump yapma; sadece karar verdiren label’ları göster.
  - Uzun annotations’ları kırp.
- Doğrulama:
  - Bir grouped alert senaryosunda mesaj çok uzun mu?
  - Slack tarafında formatting bozuluyor mu (kaçış karakterleri)?

## Common mistakes
- Her alert’te `@channel`: kısa sürede kanal “mute” edilir.
- Tüm label/annotation’ı basmak: mesaj okunmaz olur.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
- `skills/obs-alertmanager-receivers`
