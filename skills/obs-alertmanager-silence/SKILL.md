---
name: obs-alertmanager-silence
description: Planlı bakım/known-issue sırasında Alertmanager silence oluşturmak (matcher tasarımı, süre, sahiplik) veya API ile programatik silence yönetmek gerektiğinde kullan. Amaç “gürültüyü geçici susturmak”; inhibit/routing değil.
---

## Purpose
Bu skill’in çıktısı:
- Doğru kapsamlı silence matcher set’i (ne bastırılır / ne bastırılmaz)
- Süre ve sahiplik standardı (createdBy, comment/runbook, expire)
- Doğrulama: silence’ın hedef alert’leri gerçekten susturduğunu kontrol

## Workflow
- Bakım senaryosunu yaz:
  - Ne değişiyor? hangi servis/cluster? kaç dakika?
- Matcher tasarımı:
  - En dar kapsam: `service`, `cluster/namespace`, gerekirse `alertname`.
  - `severity=page` gibi kritik alert’leri silence dışında bırakmayı düşün (özellikle güvenlik/availability).
- Süre ve sahiplik:
  - Başlangıç/bitiş; mümkünse kısa (otomatik expire).
  - `createdBy` ve açıklayıcı comment: change ticket/PR/runbook linki.
- Programatik (opsiyonel):
  - API ile create/update/delete akışı (token’ı yazmadan).
- Doğrulama:
  - Silence listesinden etkin mi kontrol et.
  - Hedef bir alert firing olduğunda bildirim gitmediğini doğrula (ama UI’da alert görünmeye devam eder).

## Common mistakes
- Geniş regex matcher ile “çok şeyi” susturmak: körlük yaratır.
- Süresiz/uzun silence: unutulur, gerçek incident kaçırılır.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
