---
name: agentic-feature-flags
description: Deneysel araçlar ve MCP için bayraklar; varsayılan güvenli kapalı modu tanımlarken kullan.
---

## Amaç

Deneysel özellikler **`SENTINEL_EXPERIMENTAL_*`** veya proje kararına göre isimlendirilmiş env/feature flag arkasında tutulur. **Varsayılan: güvenli kapalı** (özellikle mutating veya ağ erişimi olan araçlar). Bayrakların listesi **README veya `doctor` çıktısında** görünür olmalıdır.

## Kapsam

### Dahil

- Örnek: `SENTINEL_EXPERIMENTAL_MCP=1`, `SENTINEL_EXPERIMENTAL_WEB_FETCH=1` (isimler proje kararı).
- Bayrak dokümantasyonunun konumu (tablo dosyası veya doc bölümü).

### Hariç

- Uzaktan feature toggle servisi (yoksa belirt).

## Kurallar

- Bayrak açıkken bile production profilinde ek onay istenebilir (`agentic-approval-policy-design`).
- CI’da deneysel özellikler ayrı job veya opt-in matrix ile test edilir.
- Flag kaldırıldığında migration notu CHANGELOG’da.

## Kontrol listesi

- [ ] Her experimental flag için açıklama + risk notu var mı?
- [ ] Varsayılan değer tablosu güncel mi?
- [ ] Güvenlik incelemesi gerektiren flag’ler işaretlendi mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Kullanıcı flag’i unuttu | `--help` / doctor | Dokümantasyon linki göster |
| Flag açıkken sızıntı | Hangi özellik | Flag kapat, hook ekle |

## İlgili belgeler ve skill'ler

- `../documantations/IMPLEMENTATION_PLAN_PHASE2.md`
- `../agentic-mcp-client-config/SKILL.md`
- `../agentic-tools-web-fetch-optional/SKILL.md`
- `../agentic-threat-model/SKILL.md`
