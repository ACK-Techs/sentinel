---
name: agentic-llm-openai-compatible-local
description: Ollama, LM Studio, vLLM gibi yerel OpenAI uyumlu /v1 uçları için port, model ve tool desteği fallback’ini yapılandırırken kullan.
---

## Amaç

Tipik **`base_url`**: `http://127.0.0.1:11434/v1` (Ollama), LM Studio / vLLM portları üretici dokümanına göre. **`SENTINEL_LOCAL_MODEL`** sunucudaki etiket ile eşleşmeli. **Tool / function calling** desteklenmeyen modellerde **graceful degrade**: salt metin modu veya kullanıcıya “araçlar kapalı” uyarısı (`LLM_PROVIDERS.md` notu). **IPv4 loopback (`127.0.0.1`) vs IPv6 (`::1`)** ve hostname çözümlemesi dokümante edilir.

## Kapsam

### Dahil

- `SENTINEL_LOCAL_TIMEOUT_SEC` uzun üretimler için.
- Yerel servisin `0.0.0.0` üzerinde dinlemesi güvenlik uyarısı (`LLM_PROVIDERS.md`).

### Hariç

- Her lokal sunucunun kurulum rehberi (resmi sitesi).

## Kurallar

- Model listesi: örn. `curl http://127.0.0.1:11434/api/tags` (Ollama) — komut üreticiye göre güncellenir.
- Bağlantı reddi: servis ayakta mı, doğru port mu (`agentic-cli-user-errors`).
- Context penceresi küçükse `agentic-llm-context-window-strategy` ile uyum.

## Kontrol listesi

- [ ] `local` profili `agentic-config-profiles` ile seçilebiliyor mu?
- [ ] Tool’suz modelde CLI çökmeden devam ediyor mu?
- [ ] Firewall / SELinux engeli notu POC dokümanında var mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Connection refused | `ss -lntp` / servis log | Sunucuyu başlat |
| Boş yanıt | Model adı typo | Model listesini doğrula |
| Tool JSON bozuk | Model yeteneği | Metin-only moda düş |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-config-env-reference/SKILL.md`
- `../agentic-llm-context-window-strategy/SKILL.md`
- `../agentic-offline-airgap-notes/SKILL.md`
