---
name: agentic-threat-model
description: Shell, dosya, API anahtarı ve MCP gibi tehditleri STRIDE-benzeri liste ile tarayıp mitigasyon eşlerken kullan.
---

## Amaç

Ajan CLI’si için basit ama işe yarar tehdit listesi: **shell execution**, **hassas dosya sızıntısı**, **API key çalınması / log sızıntısı**, **kötü niyetli veya ele geçirilmiş MCP sunucusu**, **prompt injection** (detay için ayrı skill). Her tehdit için mitigasyon: onay kapısı, sandbox hedefi (referans), ağ kısıtı, hook. **Kabul edilen risk** alanı açıkça kaydedilmelidir.

## Kapsam

### Dahil

- Tehdit → kontrol → sahip rolü (devops / güvenlik) özeti.
- Üretim vs POC için farklı sıkılık seviyesi önerisi.

### Hariç

- Kurumsal penetration test metodolojisinin tamamı.

## Kurallar

- Shell ve mutating file işlemleri varsayılan olarak **yüksek etki** kabul edilir; `agentic-approval-policy-design` ile hizala.
- MCP: yalnız yapılandırılmış sunucular; yeni sunucu **kullanıcı onayı** (mimari belge ile uyumlu).
- Sırlar: `agentic-secrets-handling`; loglarda asla tam anahtar yazma (`agentic-cli-logging`).

## Kontrol listesi

- [ ] Her tehdit için en az bir mitigasyon atanmış mı?
- [ ] “Kabul edilen risk” maddeleri sponsor onaylı mı?
- [ ] SSRF (web fetch açıksa) `agentic-tools-web-fetch-optional` ile ele alındı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Mitigasyon yok | POC modunda gevşek policy | Üretim profilinde sandbox + onay sıkılaştır |
| MCP kaynaklı veri sızıntısı | Hangi sunucu, hangi tool | Sunucuyu devre dışı bırak, hook ekle |

## İlgili belgeler ve skill'ler

- `../documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `../agentic-approval-policy-design/SKILL.md`
- `../agentic-tools-bash-shell/SKILL.md`
- `../agentic-prompt-injection-guardrails/SKILL.md`
