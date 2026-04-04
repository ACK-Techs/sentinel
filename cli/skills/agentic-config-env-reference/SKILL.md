---
name: agentic-config-env-reference
description: Tüm ortam değişkenlerinin anlam, örnek ve zorunluluk tablosunu tek yerde tutmak için kullan; LLM_PROVIDERS ile birebir hizala.
---

## Amaç

**Tek tablo**: değişken adı | anlam | örnek değer | zorunlu mu | notlar. İçerik **`../documantations/LLM_PROVIDERS.md`** ile **çelişmez**; profil seçimi (`SENTINEL_PROFILE`), log seviyesi (`SENTINEL_LOG_LEVEL` veya proje kararı), config dosya yolu (`SENTINEL_CONFIG` veya proje kararı) tabloda yer alır.

## Kapsam

### Dahil

- Remote OpenAI-uyumlu: `SENTINEL_OPENAI_BASE_URL` / `OPENAI_BASE_URL`, `SENTINEL_API_KEY`, `SENTINEL_MODEL` (öncelik çakışması proje README’sinde sabitlenir).
- Local: `SENTINEL_LOCAL_BASE_URL`, `SENTINEL_LOCAL_MODEL`, `SENTINEL_LOCAL_TIMEOUT_SEC`.
- Anthropic: `ANTHROPIC_API_KEY`, `SENTINEL_ANTHROPIC_MODEL`.

### Hariç

- Üçüncü parti SaaS’e özel tüm olası env’ler (belgede yoksa “proje kararı gerektirir”).

## Kurallar

- Tablo güncellendiğinde `LLM_PROVIDERS.md` ile senkron PR tek parça olmalı.
- Placeholder örnekler gerçek anahtar içermez.
- Çakışan isimler (örn. `OPENAI_BASE_URL` vs `SENTINEL_OPENAI_BASE_URL`) için **kazanma sırası** tek cümle ile yazılır.

## Kontrol listesi

- [ ] Her public env için dokümantasyon satırı var mı?
- [ ] `agentic-config-layers` sırası ile uyumlu mu?
- [ ] CI’da kullanılan env alt kümesi işaretlendi mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Değişken okunmuyor | Typo / profil bloğu | Tablo + `doctor` komutu (planlanan) |
| LLM_PROVIDERS ile çelişki | İki dosyayı diff | Tek kaynak seç veya cross-link |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-config-layers/SKILL.md`
- `../agentic-config-profiles/SKILL.md`
- `../agentic-cli-user-errors/SKILL.md`
