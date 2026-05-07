---
name: k8s-core-sidecar-pattern
description: Ana container’a yardımcı bir container eklemek (log shipper, proxy, config reloader, auth helper) veya “bu işi sidecar mı ayrı servis mi yapmalı?” kararını vermek gerektiğinde kullan. Amaç: **aynı pod içi yakın yardımcı işlevleri doğru ayırmak**.
---

## Purpose
Bu skill’in çıktısı:
- Sidecar uygunluğu kararı (same lifecycle, shared network/storage gereksinimi)
- Kaynak paylaşımı ve failure coupling analizi
- Doğrulama: ana container ve sidecar birlikte çalışıyor mu, birbirini bozuyor mu?

## Workflow
- Desenin uygunluğunu test et:
  - Yardımcı işlev ana app ile aynı pod yaşam döngüsünü mü paylaşmalı?
  - Ortak localhost veya ortak volume ihtiyacı var mı?
- Sidecar rolünü netleştir:
  - Proxy, log forwarder, cert/config reloader, queue helper vb.
  - Ayrı deployment daha doğruysa sidecar’a zorlama.
- Kaynak sınırlarını koy:
  - Sidecar ana uygulamanın CPU/RAM’ini yememeli; ayrı request/limit yaz.
- Bağımlılık ilişkisi:
  - Ana container sidecar olmadan çalışabiliyor mu? readiness buna göre mi?
  - Port çakışması, file lock veya shared volume yarışı var mı?
- Doğrulama:
  - Her iki container log’u.
  - `kubectl exec` ile localhost/volume üzerinden birlikte çalışma kanıtı.

## Common mistakes
- “Her şeyi sidecar yapma” yaklaşımı: pod karmaşıklığını gereksiz artırır.
- Sidecar’ın çökmesini readiness/liveness ile ilişkilendirmemek: gizli bozulmalar olur.

## References
- `skills/k8s-core-init-containers`
- `skills/obs-loki-promtail-config`
