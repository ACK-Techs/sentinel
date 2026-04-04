# Ortam değişkenleri — Faz 3 özet tablosu

Kaynak: `src/sentinel_cli/config/loader.py`, `config/models.py`. Sağlayıcı odaklı ayrıntılı açıklamalar için `LLM_PROVIDERS.md`, uzaktan telemetri yok politikası için `README.md` ve `skills/agentic-faz3-no-remote-telemetry/SKILL.md`.

**Varsayılan:** Boş bırakılan çoğu değişken için uygulama içi varsayılanlar kullanılır (bkz. `AppConfig`).

| Değişken | Varsayılan | Kullanım | Risk / not |
|----------|------------|----------|------------|
| `SENTINEL_PROFILE` | `local` | `cloud` / `local` / `anthropic` seçimi | Profil uyumsuzsa bağlantı hatası |
| `SENTINEL_CONFIG` | yok | YAML config dosya yolu | Dosya yolu hassas değil; içerik sır içerebilir |
| `SENTINEL_OPENAI_BASE_URL` | `https://api.openai.com/v1` | Cloud profil OpenAI uyumlu taban URL | `OPENAI_BASE_URL` fallback olarak okunur; Gemini OpenAI-compat için `LLM_PROVIDERS.md` içindeki köprü URL örneğine bak |
| `SENTINEL_MODEL` | `provider-model-placeholder` | Cloud profil model adı | Ayrıntı `LLM_PROVIDERS.md`; Gemini için `gemini-...` modeli aynı kombinasyonla kullanılabilir |
| `SENTINEL_CLOUD_SUPPORTS_TOOLS` | (YAML varsayilan) | `cloud` profilinde `supports_tools` | `false` / `true`; Gemini OpenAI-compat ile **400** alıyorsan `false` dene |
| `SENTINEL_LOCAL_BASE_URL` | `http://127.0.0.1:11434/v1` | Local profil taban URL | Lokal servis ayakta olmalı |
| `SENTINEL_LOCAL_MODEL` | `local_model_placeholder` | Local model adı | — |
| `SENTINEL_LOCAL_TIMEOUT_SEC` | `120` | Local HTTP süre aşımı (saniye) | — |
| `SENTINEL_ANTHROPIC_MODEL` | `anthropic_model_placeholder` | Anthropic profil model adı | — |
| `SENTINEL_API_KEY` | yok | Cloud/OpenAI uyumlu API anahtarı (env adı) | **Sır**; loglama kodu maskelemeli. Gemini OpenAI-compat köprüsünde de bu env kullanılır |
| `ANTHROPIC_API_KEY` | yok | Anthropic anahtarı (env adı) | **Sır** |
| `SENTINEL_HTTP_CONNECT_TIMEOUT_SEC` | `10` | Bağlantı timeout | — |
| `SENTINEL_HTTP_TIMEOUT_SEC` | `120` | Okuma timeout | — |
| `SENTINEL_HTTP_MAX_RETRIES` | `3` | HTTP yeniden deneme | — |
| `SENTINEL_HTTP_RETRY_STATUSES` | `429,500,502,503,504` | Virgülle HTTP kodları | — |
| `SENTINEL_CONTEXT_WINDOW_TOKENS` | `32000` | Bağlam penceresi | — |
| `SENTINEL_CONTEXT_WARN_AT` | `0.85` | Uyarı oranı | — |
| `SENTINEL_CONTEXT_STRATEGY` | `truncate` | Bağlam stratejisi | — |
| `SENTINEL_LOG_LEVEL` | `INFO` | Log seviyesi | Yerel log; uzaktan telemetri değil |
| `SENTINEL_MAX_TURNS` | `6` | Ajan tur üst sınırı | Düşük değer erken keser |
| `SENTINEL_AUTO_APPROVE` | `false` | Araç onayı otomatik (true/false) | **Yüksek risk** — mutating işlemler |
| `SENTINEL_SESSION_DIR` | `./.sentinel/sessions` | Oturum dizini | Dosya sistemi |
| `SENTINEL_TRAJECTORY_DIR` | `./.sentinel/trajectories` | Trajectory dizini | Dosya sistemi |
| `SENTINEL_TRAJECTORY_ENABLED` | `false` | Trajectory açık/kapalı | Yerel kayıt |
| `SENTINEL_EXPERIMENTAL_MCP` | `false` | Deneysel MCP stdio istemcisi rezervi | Deneysel; varsayılan kapalı |

Kod değişince bu tablo **senkron** tutulmalıdır.
