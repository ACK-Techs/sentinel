# LLM Sağlayıcıları: API ve Lokal Modlar (Faz 2)

Bu belge, Sentinel CLI’nin **aynı uygulama içinde** hem **uzak API** hem **lokal inference** kullanabilmesi için **yapılandırma sözleşmesini** tanımlar. Gerçek env anahtar adları uygulama kodu ile birebir eşleşmelidir; burada **mantıksal isimler** verilmiştir.

## Hedef

| Mod | Tipik kullanım | Kimlik doğrulama |
|-----|----------------|------------------|
| **Remote API** | OpenAI, Anthropic, Azure OpenAI, uyumlu proxy | API key veya OAuth (ürün kararı) |
| **Local OpenAI-compatible** | Ollama, LM Studio, vLLM, llama.cpp server | Genelde yok veya yerel token |

## Profil kavramı

Önerilen model: **`SENTINEL_PROFILE`** veya `--profile` değeri `cloud`, `local`, `anthropic`, vb. Profil, hangi env blokunun okunacağını seçer; ayrıntılar ilgili skill’de (ör. `agentic-config-profiles`).

## Uzak API (OpenAI uyumlu örnek)

Aşağıdaki değişkenler **örnek sözleşmedir**; uygulama README’sinde kesin liste sabitlenmelidir.

- Taban URL: `SENTINEL_OPENAI_BASE_URL` veya `OPENAI_BASE_URL` (çakışmada proje önceliği skill’de yazılır)
- API key: `SENTINEL_API_KEY` veya sağlayıcıya özel `ANTHROPIC_API_KEY` vb.
- Model adı: `SENTINEL_MODEL` veya profil içi `model`

**Streaming:** Sunucu SSE veya chunk stream destekliyorsa CLI tek bir iç olay modeline (`text_delta`, `tool_call_delta`, `done`, `error`) map etmelidir.

## Lokal sunucu (OpenAI uyumlu `/v1/chat/completions`)

- `SENTINEL_LOCAL_BASE_URL` — örn. `http://127.0.0.1:11434/v1` (Ollama) veya LM Studio portu
- `SENTINEL_LOCAL_MODEL` — sunucudaki model etiketi
- Timeout: `SENTINEL_LOCAL_TIMEOUT_SEC` (önerilir; uzun üretimler için)

**Not:** Lokal sunucunun **hangi şemayı** desteklediği (tools / JSON mode) model kartına göre değişir; ajan **tool çağrısı desteklenmiyorsa** kullanıcıya veya dokümantasyona göre graceful degrade (ör. sadece metin modu) skill’de tarif edilir.

## Anthropic (doğrudan API)

- `ANTHROPIC_API_KEY`, `SENTINEL_ANTHROPIC_MODEL`
- Mesaj ve tool şeması OpenAI’dan farklıdır; mimaride **adapter katmanı** zorunludur (`ARCHITECTURE_AGENTIC_CLI.md`).

## Hata sınıfları (kullanıcıya yansıtma)

Önerilen ayrım:

1. **Ağ / timeout** — yeniden deneme politikası (skill: `agentic-llm-retries-timeouts`)
2. **401 / 403** — anahtar veya izin; sırları loglamadan kısa mesaj
3. **429** — oran sınırı; bekleme veya kullanıcıya bilgi
4. **5xx** — sağlayıcı hatası; sınırlı retry
5. **Lokal bağlantı reddi** — servis çalışıyor mu, port doğru mu

## Güvenlik

- API anahtarlarını **commit etmeyin**; `.env` örnek dosyasında placeholder kullanın.
- Lokal modda bile **ağa açık** sunucular (0.0.0.0) risk oluşturur; skill’de uyarı metni bulunmalıdır.

## İlgili skill’ler

Aşağıdaki kimlikler **`sentinel-coming/cli/skills/<kimlik>/SKILL.md`** yoluna karşılık gelir:

- `agentic-llm-provider-contract`
- `agentic-llm-openai-compatible-remote`
- `agentic-llm-openai-compatible-local`
- `agentic-llm-anthropic-messages`
- `agentic-llm-streaming-events`
- `agentic-llm-context-window-strategy`
- `agentic-llm-retries-timeouts`
- `agentic-config-profiles`

**Bu belge:** `cli/documantations/LLM_PROVIDERS.md` — mimari için `ARCHITECTURE_AGENTIC_CLI.md` (aynı klasör).
