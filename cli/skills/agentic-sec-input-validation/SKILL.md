---
name: agentic-sec-input-validation
description: Agent çalışma zamanı güvenliğini artırmak, saldırı yüzeyini daraltmak ve operasyonel güvenlik kontrollerini uygulanabilir adımlara çevirmek gerektiğinde kullan.
---

## Güvenlik amacı
`agentic-sec-input-validation`, agentin çalışma serbestliğini daraltıp zarar ihtimalini azaltmak için tasarlanır. Güvenlik kontrolü yalnızca "engelle" yaklaşımı değildir; denetlenebilir log, açık hata mesajı ve sürdürülebilir operasyon da gerektirir.

## Tehditten kontrole geçiş
- **Varlık tanımı:** hangi veri/araç kritik ve hangi kanaldan sızabilir?
- **Sınır koyma:** tool policy, input validator, output sanitizer ve ağ/işletim sistemi kısıtlarını katmanlı uygula.
- **Kanıt üretme:** audit trail ve olay kimlikleriyle her kritik eylemi izlenebilir yap.
- **Kurtarma:** credential rotation, rate limit veya izole mod gibi hızlı yanıt mekanizmalarını hazır tut.

## Sentinel pratik akış
- Prompt ve tool katmanını ayrı güvenlik kontrolleriyle değerlendir.
- `--verbose` modunda bile secret içeriği maskeli tut.
- CI içinde güvenlik kontrolünü "uyarı" değil "gate" seviyesine taşı.

## Dikkat noktaları
- Sadece LLM çıktısına güvenip komut çalıştırma.
- Audit log üretip bütünlük (tamper) sağlamama.
- Container sandbox var diye uygulama seviyesinde doğrulamayı atlama.

## Skill-spesifik kararlar
- Input validationda uzunluk, karakter seti ve schema kontrollerini katmanli yap. Komut satiri argumanlarini shell-safe normalize et.

## Referanslar
- `cli/skills/agentic-threat-model/SKILL.md`
- `cli/skills/agentic-sandbox-hardening-reference/SKILL.md`
- `cli/skills/agentic-secrets-handling/SKILL.md`
- `cli/documantations/archive/THREAT_MODEL_PHASE2A.md`
