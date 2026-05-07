---
name: obs-alertmanager-api
description: Alertmanager v2 HTTP API ile otomasyon yapmak (alerts/silences listeleme, silence create/expire, status/health kontrolü) gerektiğinde kullan. Hedef, güvenli `curl` kalıpları ve hata modu teşhisidir.
---

## Purpose
Bu skill’in çıktısı:
- API çağrı şablonları: status → alerts → silences (CRUD)
- Güvenli auth yaklaşımı (token’ı yazmadan ENV üzerinden)
- Doğrulama: beklenen alert/silence objesinin gerçekten oluştuğunu kontrol

## Workflow
- Baz URL ve erişim:
  - Alertmanager endpoint (ingress/internal), TLS/proxy var mı?
- Auth:
  - Varsa `Authorization: Bearer $AM_TOKEN` şeklinde kullan; token’ı metne yazma.
- Okuma akışı:
  - `status`/health ile instance çalışıyor mu?
  - `alerts` ile aktif alert’leri filtrele (label matcher).
  - `silences` ile etkin silences listesini al.
- Yazma akışı (silence):
  - En dar matcher set’iyle create.
  - Expire (end time) güncelleme veya delete senaryosu.
- Hata modu:
  - 401/403: auth.
  - 5xx: backend/HA split.
  - Timeout: ağ/DNS/proxy.
- Doğrulama:
  - Create sonrası silence ID ile getir; eşleşen alert’lerde “silenced” etkisini gözle.

## Common mistakes
- Regex matcher ile aşırı geniş silence yaratmak.
- API üzerinden yapılan silence’larda sahiplik/comment tutmamak: audit kaybı.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
- `skills/obs-alertmanager-silence`
