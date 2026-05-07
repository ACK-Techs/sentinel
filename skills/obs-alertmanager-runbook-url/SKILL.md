---
name: obs-alertmanager-runbook-url
description: Alert bildirimlerine tutarlı bir runbook linki eklemek (annotation standardı, template’lerde gösterim) veya “bildirim var ama runbook yok/yanlış” sorununu çözmek gerektiğinde kullan. Runbook’un kendisini yazmaz; **runbook URL kontratını** kurar.
---

## Purpose
Bu skill’in çıktısı:
- Runbook URL standardı (annotation adı, format, örnek)
- Receiver/template tarafında runbook linkini görünür kılan mesaj kalıbı
- Doğrulama: örnek bir alert bildiriminde runbook linki doğru ve erişilebilir mi?

## Workflow
- Kontrat seç:
  - Annotation adı: genelde `runbook_url` (tek standardı seç).
  - URL formatı: kalıcı link (wiki, docs site, repo path).
- Üretim stratejisi:
  - Alert rule’larda manuel set.
  - Veya alertname/service’e göre otomatik generate (ama yanlış link riskini yaz).
- Template entegrasyonu:
  - Slack/Teams/webhook mesajında runbook linkini “ilk ekranda” göster.
  - Runbook yoksa “missing runbook” uyarısı ekle (isteğe bağlı).
- Doğrulama:
  - Bir test alert’i ile bildirim al; runbook linki tıklanabilir mi?
  - URL erişim izni doğru mu? (SSO/401 sürprizi)

## Common mistakes
- Runbook URL’yi opsiyonel bırakıp unutmak: en kritik anlarda “ne yapacağız?” boş kalır.
- Otomatik generate edip doğrulamamak: yanlış runbook’a yönlendirir.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
- `skills/obs-alertmanager-slack-template`
