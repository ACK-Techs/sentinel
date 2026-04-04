---
name: agentic-tools-web-fetch-optional
description: İsteğe bağlı HTTP GET için SSRF riski, domain allowlist ve varsayılan kapalı modu tanımlarken kullan.
---

## Amaç

**Varsayılan kapalı** veya `agentic-feature-flags` arkasında. **SSRF**: iç ağ IP, metadata uçları, `file://` yasak (proje kararı). **Domain allowlist** veya kullanıcı onayı. **Boyut sınırı** ve **redirect limiti** (örn. max 5). Yanıt metni kırpılır; binary Content-Type reddedilebilir.

## Kapsam

### Dahil

- TLS doğrulama (kurumsal CA notu).
- User-Agent tanımlama (kibarlık / rate limit).

### Hariç

- Genel web tarayıcı veya JS execution.

## Kurallar

- Fetch çıktısı **doğrudan system prompt’a** ham eklenmez (`agentic-prompt-injection-guardrails`).
- `agentic-threat-model` SSRF maddesi ile hizalı.
- 403/401 durumunda retry yok (yanlış kimlik döngüsü).

## Kontrol listesi

- [ ] `169.254.169.254` testi bloklu mu?
- [ ] Redirect zinciri sınırlı mı?
- [ ] Flag kapalıyken araç registry’de yok mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Timeout | Sunucu yavaş | Limit artır veya kullanıcıya söyle |
| SSL hatası | MITM | CA yapılandırması |

## İlgili belgeler ve skill'ler

- `../agentic-feature-flags/SKILL.md`
- `../agentic-threat-model/SKILL.md`
- `../agentic-prompt-injection-guardrails/SKILL.md`
- `../agentic-llm-retries-timeouts/SKILL.md`
