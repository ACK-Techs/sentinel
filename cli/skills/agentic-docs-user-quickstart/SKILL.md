---
name: agentic-docs-user-quickstart
description: Son kullanıcı için cloud API ve lokal Ollama modunda beş dakikada çalıştırma adımları ve mini hata tablosu hazırlarken kullan.
---

## Amaç

**Kopyala-yapıştır blokları**: venv, kurulum, env export, ilk `chat` komutu. **Cloud**: `SENTINEL_API_KEY`, `SENTINEL_OPENAI_BASE_URL`, `SENTINEL_MODEL` (`LLM_PROVIDERS.md`). **Lokal**: `SENTINEL_LOCAL_BASE_URL` (örn. Ollama `http://127.0.0.1:11434/v1`), `SENTINEL_LOCAL_MODEL`. **Mini hata tablosu**: bağlantı reddi, 401, model bulunamadı → kontrol + komut.

## Kapsam

### Dahil

- `agentic-cli-entrypoint` komut adları ile uyumlu örnekler.
- macOS/Linux fark notu (path, shell).

### Hariç

- Kurumsal proxy özel adımları (genel yönlendirme yeterli).

## Kurallar

- Örneklerde gerçek API key yok.
- Ollama model çekme: `ollama pull <model>` resmi dokümana köprü.
- Sorun devamında `doctor` veya verbose flag öner.

## Kontrol listesi

- [ ] Temiz makinede adımlar sırayla çalışıyor mu?
- [ ] Her komut açıklama satırı ile mi?
- [ ] `LLM_PROVIDERS.md` ile env isimleri birebir mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Module not found | venv aktif mi | `pip install -e .` |
| 401 | Key | Profil ve env |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-cli-entrypoint/SKILL.md`
- `../agentic-config-env-reference/SKILL.md`
- `../agentic-cli-user-errors/SKILL.md`
