---
name: obs-alertmanager-juju-relation
description: Juju/COS ortamında Prometheus’un Alertmanager’a alert göndermesi için relation kurmak veya “relation var ama Prometheus alerts göndermiyor” sorununu çözmek gerektiğinde kullan. Hedef: charm relation üzerinden endpoint ve auth bilgisinin doğru taşınmasıdır.
---

## Purpose
Bu skill’in çıktısı:
- Juju relation adımları (hangi charm’lar, hangi endpoint) ve beklenen durumlar
- Teşhis akışı: relation → unit status → Prometheus config → Alertmanager API’de alert görünürlüğü
- Doğrulama: test alert’i ile Alertmanager UI/API’de “active alert” kanıtı

## Workflow
- Bağlam:
  - Kullanılan charm’lar: `prometheus-k8s` ve `alertmanager-k8s` (veya eşdeğer).
- Relation kur:
  - Prometheus ↔ Alertmanager relation’ını oluştur (doğru relation endpoint adıyla).
- Beklenen sonuç:
  - Prometheus config’inde Alertmanager target’ları oluşmalı.
  - Alertmanager API çalışır durumda olmalı.
- “Göndermiyor” teşhisi:
  - `juju status`: blocked/waiting var mı?
  - Prometheus tarafında Alertmanager endpoints listesi boş mu?
  - Ağ/TLS sorunları (cluster içinde erişim).
- Doğrulama:
  - Kısa bir test alert’i üret; Alertmanager’da active/firing listesinde gör.

## Common mistakes
- Yanlış relation endpoint: relation “var” görünür ama data taşınmaz.
- Alertmanager HA split brain: Prometheus yanlış instance’a gönderir.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
