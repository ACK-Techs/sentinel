---
name: obs-prometheus-api-auth
description: Prometheus HTTP API’yi (özellikle `/api/v1/query*`) güvenli şekilde erişime açmak gerektiğinde kullan. Basic auth, mTLS, reverse proxy ve “read-only erişim” modeli kurulumunda; header/credential sızıntısı ve yanlış yetkilendirme risklerini azaltmaya odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Seçilen modele göre erişim taslağı: **doğrudan Prometheus** mu, yoksa **reverse proxy/gateway** üzerinden mi?
- Auth/TLS gereksinimleri ve client çağrısı örneği (secret değerleri olmadan)
- Güvenlik kontrol listesi: “read-only”, ağ sınırı, log’larda credential maskeleme

## Workflow
- Erişim modelini seç:
  - **En güvenlisi**: Prometheus’u private tut + sadece cluster içinden eriş.
  - Dış erişim gerekiyorsa: reverse proxy veya repo’daki **observability-gateway** gibi read-only katman tercih et.
- Auth seçimi (kısıtlı hedef):
  - Basic auth: hızlı ama credential yönetimi şart (rotasyon, maskeleme).
  - mTLS: service-to-service için en güçlü; client sertifika yönetimi gerektirir.
  - Bearer token: header taşınır; log/trace’de sızma riski yüksek → maskeleme şart.
- “Read-only” kuralını uygula:
  - İzin verilen path’leri allowlist yap (`/api/v1/query`, `/api/v1/query_range`, `/api/v1/labels` vb.).
  - Admin/debug endpoint’lerini dışarı açma (ör. flags/config gibi).
- Reverse proxy üzerinden geçiriyorsan:
  - TLS termination nerede? (proxy mi, Prometheus mu)
  - Header forward/strip kuralları: `Authorization` log’lanmasın; upstream’e gerektiği kadar geçsin.
- Doğrulama:
  - Auth olmadan 401/403 bekleniyor mu?
  - Doğru kimlikle `query` çalışıyor mu?
  - Yetkisiz path’ler gerçekten engelleniyor mu?

## Common mistakes
- Token’ı curl komutunda örnekleyip ticket/Slack’e yapıştırmak (kalıcı sızıntı).
- Proxy log’larında `Authorization` header’ını maskelemeden bırakmak.

## References
- `documantations/INTEGRATION_SENTINEL_CLI_FROM_CLI_CLAUDE.md`
