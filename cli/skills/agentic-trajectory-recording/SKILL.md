---
name: agentic-trajectory-recording
description: Tur bazlı model ve tool kaydı, PII redaksiyonu ve opt-in politikası tanımlarken kullan.
---

## Amaç

**Tur bazlı kayıt**: model çıktısı, tool çağrıları, sonuçlar, token usage (varsa). **Opt-in** veya varsayılan kapalı (ürün kararı dokümante). **PII redaksiyonu**: e-posta, telefon, token benzeri kalıplar; kullanıcı mesajı tam kayıt opsiyonel. **Döndürme**: dosya boyutu veya gün sayısı politikası.

## Kapsam

### Dahil

- Replay veya debug için JSON şeması (iç kullanım).
- `agentic-cli-logging` ile korelasyon `session_id`.

### Hariç

- Üretim analitiği PII toplama (GDPR ayrı süreç).

## Kurallar

- Trajectory dosyası paylaşılmadan önce redaksiyon scripti önerisi.
- Secret asla düz yazılmaz (`agentic-secrets-handling`).
- OpenTelemetry ile ikili kayıt (`agentic-telemetry-optional`).

## Kontrol listesi

- [ ] Varsayılan opt-in/out ürün kararı yazılı mı?
- [ ] Redaksiyon regex’leri testli mi?
- [ ] Büyük trajectory performans etkisi ölçüldü mü?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Disk şişmesi | Rotasyon | Politikayı sıkılaştır |
| Hassas veri sızıntısı | Örnek dosya incele | Redaksiyon genişlet |

## İlgili belgeler ve skill'ler

- `../agentic-cli-logging/SKILL.md`
- `../agentic-telemetry-optional/SKILL.md`
- `../agentic-session-persistence/SKILL.md`
- `../agentic-secrets-handling/SKILL.md`
