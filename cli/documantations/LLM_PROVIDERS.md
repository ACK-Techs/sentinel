# LLM Sağlayıcıları: API ve Lokal Modlar (Faz 2)

Bu belge, Sentinel CLI’nin **aynı uygulama içinde** hem **uzak API** hem **lokal inference** kullanabilmesi için **yapılandırma sözleşmesini** tanımlar. Faz 2.B itibariyla env adlari `cli/.env.example` ve `archive/CONFIG_REFERENCE_PHASE2B.md` ile hizalanmistir.

## Hedef

| Mod | Tipik kullanım | Kimlik doğrulama |
|-----|----------------|------------------|
| **Remote API** | OpenAI, Anthropic, Azure OpenAI, uyumlu proxy | API key veya OAuth (ürün kararı) |
| **Local OpenAI-compatible** | Ollama, LM Studio, vLLM, llama.cpp server | Genelde yok veya yerel token |

## Profil kavramı

Önerilen model: **`SENTINEL_PROFILE`** veya `--profile` değeri `cloud`, `local`, `anthropic`, vb. Profil, hangi env blokunun okunacağını seçer. Merge sirasi: **defaults < dosya < env < CLI**.

## Uzak API (OpenAI uyumlu örnek)

Aşağıdaki değişkenler Faz 2.B koduyla hizali public sozlesmedir.

- Taban URL: `SENTINEL_OPENAI_BASE_URL` veya `OPENAI_BASE_URL` (çakışmada `SENTINEL_OPENAI_BASE_URL` kazanır)
- API key: `SENTINEL_API_KEY` veya sağlayıcıya özel `ANTHROPIC_API_KEY` vb.
- Model adı: `SENTINEL_MODEL` veya profil içi `model`

**Streaming:** Sunucu SSE veya chunk stream destekliyorsa CLI tek bir iç olay modeline (`text_delta`, `tool_call_delta`, `done`, `error`) map etmelidir.

## Gemini (OpenAI uyumlu köprü)

Gemini, bu repoda ayrı bir `ProviderKind` olmadan mevcut `cloud`/`openai` yolu üzerinden kullanılmalıdır. Google'ın resmi OpenAI compatibility dokümanında örnek `base_url` olarak `https://generativelanguage.googleapis.com/v1beta/openai/` verilir; güncel URL ve desteklenen yollar için Google dokümantasyonuna bakın.

Örnek env kombinasyonu:

- `SENTINEL_PROFILE=cloud`
- `SENTINEL_OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/`
- `SENTINEL_API_KEY=<Google AI Studio / Gemini API key>`
- `SENTINEL_MODEL=gemini-...`

`SENTINEL_OPENAI_BASE_URL` ayarlanmazsa kod `OPENAI_BASE_URL` fallback'ini de okur, ancak Gemini için proje içinde açık ve öncelikli ayar olarak `SENTINEL_OPENAI_BASE_URL` kullanılması önerilir.

Kapsam notu: Bu entegrasyon yalnız OpenAI-compatible köprü içindir. Native Gemini `generateContent` JSON şeması ve ayrı Google adapter yolu bu görevin kapsamı dışındadır.

## Lokal sunucu (OpenAI uyumlu `/v1/chat/completions`)

- `SENTINEL_LOCAL_BASE_URL` — örn. `http://127.0.0.1:11434/v1` (Ollama) veya LM Studio portu
- `SENTINEL_LOCAL_MODEL` — sunucudaki model etiketi
- Timeout: `SENTINEL_LOCAL_TIMEOUT_SEC` (önerilir; uzun üretimler için)

**Not:** Lokal sunucunun **hangi şemayı** desteklediği (tools / JSON mode) model kartına göre değişir; ajan **tool çağrısı desteklenmiyorsa** kullanıcıya veya dokümantasyona göre graceful degrade (ör. sadece metin modu) skill’de tarif edilir.

## Anthropic (doğrudan API)

- `ANTHROPIC_API_KEY`, `SENTINEL_ANTHROPIC_MODEL`
- Mesaj ve tool şeması OpenAI’dan farklıdır; mimaride **adapter katmanı** zorunludur (`ARCHITECTURE_AGENTIC_CLI.md`).

## Diger ortak env'ler

- `SENTINEL_CONFIG` — YAML config yolu
- `SENTINEL_HTTP_CONNECT_TIMEOUT_SEC`
- `SENTINEL_HTTP_TIMEOUT_SEC`
- `SENTINEL_HTTP_MAX_RETRIES`
- `SENTINEL_HTTP_RETRY_STATUSES`
- `SENTINEL_CONTEXT_WINDOW_TOKENS`
- `SENTINEL_CONTEXT_WARN_AT`
- `SENTINEL_CONTEXT_STRATEGY`

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

Tam tablo icin `archive/CONFIG_REFERENCE_PHASE2B.md` dosyasina bakin.

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
