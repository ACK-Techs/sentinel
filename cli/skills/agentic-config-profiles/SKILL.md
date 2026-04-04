---
name: agentic-config-profiles
description: cloud, local, anthropic-only gibi profillerin alan haritasını ve geçiş kurallarını tanımlarken kullan.
---

## Amaç

Profiller (örn. **`cloud`**, **`local`**, **`anthropic-only`** veya ekip adları) hangi `base_url`, model ve kimlik bilgisini seçer — harita YAML parçaları ile örneklenir. Profil seçimi: `SENTINEL_PROFILE` veya `--profile` (proje kararı). **Profil değişiminde** aynı oturumda karışık provider riski: mümkünse **yeni oturum** önerisi (`agentic-agent-multi-provider-switch`).

## Kapsam

### Dahil

- Örnek `.yaml` blokları: `profiles.cloud`, `profiles.local` benzeri yapı (kesin şema proje kararı).
- Öncelik: CLI flag > env > dosya > defaults.

### Hariç

- Çok kiracılı (multi-tenant) cloud konfigürasyonu (ayrı ADR).

## Kurallar

- `local` profilinde `127.0.0.1` / `localhost` ve IPv6 loopback farkı dokümante (`agentic-llm-openai-compatible-local`).
- Bilinmeyen profil adında anlamlı çıkış kodu ve Türkçe mesaj (`agentic-cli-user-errors`).
- Geçiş sonrası eski mesaj geçmişi adapter uyumsuzluğu yaratıyorsa kullanıcıyı uyar.

## Kontrol listesi

- [ ] Her profil için minimum env kümesi tabloda mı?
- [ ] `LLM_PROVIDERS.md` ile model/base_url sözleşmesi uyumlu mu?
- [ ] Örnek config repoda secret içermiyor mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Yanlış profil sessizce seçildi | Default profil | Explicit `SENTINEL_PROFILE` zorunlu kıl |
| Local servis yok | `curl` / sağlık | Quickstart skill’e yönlendir |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-config-layers/SKILL.md`
- `../agentic-llm-openai-compatible-remote/SKILL.md`
- `../agentic-llm-openai-compatible-local/SKILL.md`
- `../agentic-agent-multi-provider-switch/SKILL.md`
