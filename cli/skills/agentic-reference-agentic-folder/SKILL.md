---
name: agentic-reference-agentic-folder
description: Workspace agentic/ altındaki Codex, Pywen ve Claude kesitlerinden hangi desenin nerede öğrenileceğini tablolar ve uyarlama notları verirken kullan.
---

## Amaç

| Konu | Örnek yol (workspace) | Ne öğrenilir |
|------|------------------------|--------------|
| Rust sandbox / OTEL | `agentic/codex-main/codex-rs/linux-sandbox`, `codex-rs/otel` | Üretim sandbox ve gözlemlenebilirlik desenleri |
| Python tool registry + hooks | `agentic/Pywen-dev/pywen/tools/tool_manager.py`, `pywen/hooks/` | Araç kaydı, onay, subprocess hook |
| Çok sağlayıcılı LLM | `agentic/Pywen-dev/pywen/llm/` | Adapter ve streaming olayları |
| TS ürün kesiti | `agentic/claude/src/` (kısmi ağaç) | Telemetry/skills/shell dosya yapısı — bu kökte tam build dosyasında görülmeyebilir |

**Telif / lisans**: Üçüncü parti kod kopyalanmadan önce ilgili LICENSE dosyası okunur; türetme `../agentic-dependency-licensing/SKILL.md` ile uyumlu.

## Kapsam

### Dahil

- Desen çıkarma ve Sentinel CLI’ye uyarlanabilirlik notları.
- Hangi parçanın **doğrudan kopyalanmaması** gerektiği uyarısı.

### Hariç

- `agentic/` içeriğinin güncel sürüm garantisi (upstream değişir).

## Kurallar

- Yol örnekleri workspace’e göre; farklı checkout’ta doğrula.
- Kod hırsızlığı değil, mimari öğrenme perspektifi.
- Ürün kararı olmadan upstream bağımlılık ekleme.

## Kontrol listesi

- [ ] Kopyalanan dosya lisansı uyumlu mu?
- [ ] Uyarlama ADR veya plan maddesine işlendi mi?
- [ ] Eski yol kırıldı mı (upstream taşıma)?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Yol yok | Repo snapshot | Güncel ağaçta ara |
| Lisans çakışması | LICENSE | Hukuk / alternatif |

## İlgili belgeler ve skill'ler

- `../agentic-dependency-licensing/SKILL.md`
- `../agentic-llm-provider-contract/SKILL.md`
- `../agentic-sandbox-hardening-reference/SKILL.md`
- `../documantations/IMPLEMENTATION_PLAN_PHASE2.md`
