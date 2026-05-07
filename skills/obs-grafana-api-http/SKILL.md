---
name: obs-grafana-api-http
description: Grafana HTTP API ile otomasyon yapmak (dashboard import/export, klasör arama, datasource yönetimi) veya “UI yerine API ile yönet” ihtiyacı olduğunda kullan. Amacı API çağrısı örnekleri ve güvenli auth kalıbı üretmektir; provisioning/GitOps ayrı skill’dir.
---

## Purpose
Bu skill’in çıktısı:
- Güvenli API kullanım kalıbı (token’ı yazmadan header şablonu)
- En sık otomasyon senaryoları için `curl` örnekleri: search → export → import
- Doğrulama: API yanıtı ve Grafana UI’da görünürlük kontrolü

## Workflow
- Bağlamı sabitle:
  - Grafana base URL (örn. `https://grafana.example`), org/tenant var mı?
  - Auth türü: service account token mı, basic auth mı?
- Güvenli auth şablonu:
  - Token değerini asla yapıştırma; `Authorization: Bearer $GRAFANA_TOKEN` gibi ENV üzerinden.
- Tipik akışlar (ihtiyaca göre seç):
  - Dashboard arama: UID/title bul.
  - Dashboard export: JSON al.
  - Dashboard import/update: folder UID ile yaz.
  - Datasource listele/oluştur: isim/UID yönetimi.
- Çakışma/drift:
  - Aynı dashboard UI’dan da değişiyorsa sürüm/UID stratejisini yaz.
- Doğrulama:
  - HTTP status + body kontrolü.
  - UI’da folder/dashboard gerçekten görünüyor mu?

## Common mistakes
- Token’ı log’lara/CI çıktısına sızdırmak.
- Import’ta UID/folder id karışıklığı yüzünden aynı dashboard’u çoğaltmak.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-grafana-provisioning`
