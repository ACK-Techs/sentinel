---
name: obs-loki-multi-tenancy
description: Loki’de tenant izolasyonu için `X-Scope-OrgID` header akışını kurmak veya “yanlış tenant logu görünüyor / hiç log gelmiyor” sorununu çözmek gerektiğinde kullan. Grafana datasource header’ı, push client header’ı ve gateway/proxy etkilerini kapsar.
---

## Purpose
Bu skill’in çıktısı:
- İstek zinciri boyunca tenant header’ının **nerede eklendiği** ve **nerede korunması gerektiği**
- Push ve Query için örnek header kullanımı (secret/tenant değerini ifşa etmeden)
- “Tenant mismatch” teşhis checklist’i

## Workflow
- Tenant modelini sabitle:
  - Tenant ID nereden geliyor? (kullanıcı, namespace, environment)
  - Tek bir kaynak seç; farklı yerlerde farklı tenant üretme.
- Push tarafı:
  - Promtail/collector veya custom push client `X-Scope-OrgID` header’ını ekliyor mu?
  - Proxy/gateway arada ise header’ı strip ediyor mu?
- Query tarafı (Grafana/CLI):
  - Grafana Loki datasource, sorgu isteklerinde tenant header’ını gönderiyor mu?
  - Aynı kullanıcı farklı tenant’lara geçecekse “datasource var/yok” stratejisini yaz.
- Güvenlik:
  - Tenant header log’lara düşmesin (proxy access log).
  - “Tenant=all” gibi bypass yapma.
- Doğrulama:
  - Canary: tenant A’ya özel bir log line push et; tenant B’den sorgulayıp görünmediğini doğrula.
  - Boş sonuç varsa önce header var mı yok mu kontrol et (Grafana query inspector / proxy log).

## Common mistakes
- Push var, query yok: Grafana tenant header göndermiyordur (veya tersi).
- Proxy header’ı drop/overwrite eder: tenant karışır.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-label-strategy`
