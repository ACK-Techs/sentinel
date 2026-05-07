---
name: obs-gateway-auth-token
description: Observability gateway’de token tabanlı kimlik doğrulama ve header doğrulama mantığını kurmak (bearer token, tenant header, allow/deny) veya “unauthorized/forbidden” hatalarını teşhis etmek gerektiğinde kullan. Odak: **authn/authz kontratı** ve loglanabilir doğrulama adımlarıdır.
---

## Purpose
Bu skill’in çıktısı:
- Gateway auth kontratı: hangi header’lar zorunlu, token nereden doğrulanır, tenant nasıl çıkarılır?
- Güvenlik checklist’i: token sızıntısı, replay, log maskleme, rota bazlı yetki
- Doğrulama: 3 senaryo ile kanıt (geçerli token, geçersiz token, eksik tenant)

## Workflow
- Kontratı yaz:
  - İstemci hangi header’ları gönderir? (`Authorization`, `X-Scope-OrgID` benzeri tenant)
  - Token formatı (JWT vs opaque) ve doğrulama kaynağı (JWKS, introspection, static).
- Doğrulama mantığı:
  - Signature/expiry kontrolü (JWT ise).
  - Tenant binding: token içindeki claim ile header tenant uyuşmalı mı?
- Yetkilendirme:
  - Hangi backend’lere erişim var? (metrics/logs/traces ayrı)
  - Rate limit ve quota ile birlikte düşün.
- Observability:
  - Auth kararını audit log’a yaz (token değil, token id/subject).
  - Hata yanıtlarını tutarlı yap (401 vs 403).
- Doğrulama:
  - Geçerli token → 200.
  - Geçersiz/expired token → 401.
  - Tenant mismatch → 403.

## Common mistakes
- Token’ı log’lamak: kalıcı sızıntı.
- Tenant header’ını “client söyledi” diye kabul etmek: cross-tenant veri sızıntısı.

## References
- `skills/obs-gateway-rate-limiting`
- `skills/obs-gateway-error-model`
