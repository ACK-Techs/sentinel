---
name: agentic-cli-entrypoint
description: Ana CLI komut ağacı, global bayraklar, yardım metni ve çıkış kodlarını tanımlarken kullan.
---

## Amaç

Örnek komut isimleri: **`chat`** (veya tek komut), **`config`**, **`doctor`**, **`version`** — proje kararı ile sabitlenir. **Global flag’ler**: `--profile`, `--verbose`, `--config`, `--help`. Yardım metni şablonu: kısa açıklama, alt komutlar, örnekler, dokümantasyon linki. **Çıkış kodları** tablosu: `0` başarı, `1` genel hata, `2` yapılandırma/usage, `3` ağ/LLM (örnek; kesin tablo README’de).

## Kapsam

### Dahil

- Entry point adı (`pyproject.toml` console script) ile komut satırı adının eşlemesi.
- `--help` tüm alt komutlarda tutarlı.

### Hariç

- GUI veya TUI çerçevesi (ayrı karar).

## Kurallar

- `doctor` çıktısı: profil, base_url (maskeli), model, bağımlılık sürümleri önerisi.
- Hata mesajları Türkçe kısa + `--verbose` ile teknik detay (`agentic-cli-user-errors`).
- Plugin yükleme varsa güvenilir kaynak kontrolü.

## Kontrol listesi

- [ ] `--help` ve `-h` çalışıyor mu?
- [ ] Bilinmeyen alt komut anlamlı hata veriyor mu?
- [ ] Exit code CI’da assert edilebiliyor mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Komut bulunamadı | PATH / venv | Kurulum dokümanı |
| Yanlış çalışma dizini | cwd | `doctor` ile göster |

## İlgili belgeler ve skill'ler

- `../documantations/IMPLEMENTATION_PLAN_PHASE2.md`
- `../agentic-cli-repl-vs-once/SKILL.md`
- `../agentic-config-layers/SKILL.md`
- `../agentic-docs-user-quickstart/SKILL.md`
