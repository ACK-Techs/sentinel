---
name: obs-grafana-datasource-proxy
description: Grafana’nın datasource proxy davranışını güvenli hale getirmek (auth forward, allowlist, SSRF riskleri) veya “datasource çalışıyor ama auth/header bozuluyor” sorununu çözmek gerektiğinde kullan. Özellikle reverse proxy arkasında header/policy kurgusuna odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Datasource proxy için güvenlik kontrol listesi (SSRF, ağ sınırı, header maskeleme)
- Auth forward stratejisi (hangi header geçecek / hangisi strip edilecek)
- Doğrulama: Grafana’dan datasource’a istek gidiyor mu ve yetkiler doğru mu?

## Workflow
- Tehdit modelini yaz:
  - Grafana kullanıcıları datasource üzerinden hangi ağlara erişebilir? (SSRF riski)
- Ağ sınırı:
  - Datasource URL’lerini internal allowlist’e indir (private IP/metadata endpoint erişimini engelle).
- Auth stratejisi:
  - Grafana server → datasource arasında: basic/bearer/mTLS hangisi?
  - Kullanıcı header’larını upstream’e taşımak istiyor musun? (genelde hayır; server-side credential daha güvenli)
- Header hijyen:
  - `Authorization` gibi header’ları log’larda maskele.
  - Reverse proxy kullanıyorsan hangi header’lar strip edilecek açık yaz.
- Doğrulama:
  - Grafana “Test & Save” başarılı mı?
  - Explore/query ekranında gerçek sorgu dönüyor mu?

## Common mistakes
- Datasource proxy’yi “genel HTTP proxy” gibi açmak (SSRF).
- User auth header’larını upstream’e aynen forward etmek (sızıntı ve yetki karmaşası).

## References
- `skills/cos-deploy-grafana`
- `cli/skills/agentic-troubleshoot-grafana`
