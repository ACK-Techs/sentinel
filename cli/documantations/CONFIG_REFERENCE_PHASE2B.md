# Faz 2.B Config Katmanlari ve Env Referansi

Bu belge, Faz 2.B icin config merge sirasini ve public env sozlesmesini sabitler.

## Merge sirasi

Tek dogru sira:

1. Varsayilanlar (`AppConfig`)
2. YAML config dosyasi (`--config` veya `SENTINEL_CONFIG`)
3. Ortam degiskenleri
4. CLI bayraklari

Liste alanlarinda strateji `replace` olarak secildi. Ornek: `http.retry.retryable_status_codes` daha yuksek oncelikli katmanda tum listeyi degistirir; append yapilmaz.

## Public env tablosu

| Degisken | Anlam | Ornek | Zorunlu mu | Not |
|----------|-------|-------|------------|-----|
| `SENTINEL_CONFIG` | Config dosyasi yolu | `./config/sentinel.example.yaml` | Hayir | CLI `--config` daha ustun |
| `SENTINEL_PROFILE` | Aktif profil | `local` | Hayir | Varsayilan `local` |
| `SENTINEL_OPENAI_BASE_URL` | Cloud OpenAI uyumlu base URL | `https://api.example.com/v1` | Cloud icin genelde evet | `OPENAI_BASE_URL` uzerinde proje onceligi kazanir |
| `OPENAI_BASE_URL` | Fallback OpenAI base URL | `https://api.openai.com/v1` | Hayir | `SENTINEL_OPENAI_BASE_URL` yoksa okunur |
| `SENTINEL_API_KEY` | Cloud OpenAI uyumlu API key | `sentinel_api_key_placeholder` | Cloud icin evet | Secret, loglanmaz |
| `SENTINEL_MODEL` | Cloud model etiketi | `provider-model-placeholder` | Hayir | `profiles.cloud.model` uzerine yazar |
| `SENTINEL_LOCAL_BASE_URL` | Lokal OpenAI uyumlu base URL | `http://127.0.0.1:11434/v1` | Local icin evet | `127.0.0.1` tercih edilir |
| `SENTINEL_LOCAL_MODEL` | Lokal model etiketi | `local_model_placeholder` | Local icin evet | |
| `SENTINEL_LOCAL_TIMEOUT_SEC` | Lokal profile ozel timeout | `120` | Hayir | `profiles.local.timeout_sec` uzerine yazar |
| `ANTHROPIC_API_KEY` | Anthropic API key | `anthropic_api_key_placeholder` | Anthropic icin evet | Secret, loglanmaz |
| `SENTINEL_ANTHROPIC_MODEL` | Anthropic model etiketi | `anthropic_model_placeholder` | Hayir | |
| `SENTINEL_HTTP_CONNECT_TIMEOUT_SEC` | HTTP connect timeout | `10` | Hayir | Tum provider'lara ortak |
| `SENTINEL_HTTP_TIMEOUT_SEC` | HTTP read timeout | `120` | Hayir | Tum provider'lara ortak |
| `SENTINEL_HTTP_MAX_RETRIES` | Maksimum retry sayisi | `3` | Hayir | 401/403 icin retry yok |
| `SENTINEL_HTTP_RETRY_STATUSES` | Retry edilecek HTTP kod listesi | `429,500,502,503,504` | Hayir | Virgulle ayrilir, liste replace olur |
| `SENTINEL_CONTEXT_WINDOW_TOKENS` | Heuristik context limiti | `32000` | Hayir | |
| `SENTINEL_CONTEXT_WARN_AT` | Uyari esigi | `0.85` | Hayir | 0-1 arasi |
| `SENTINEL_CONTEXT_STRATEGY` | Context stratejisi | `truncate` | Hayir | `warn` veya `truncate` |
| `SENTINEL_LOG_LEVEL` | JSON log seviyesi | `INFO` | Hayir | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `SENTINEL_MAX_TURNS` | Ajan maksimum tur sayisi | `6` | Hayir | Faz 2.C ajan dongusu |
| `SENTINEL_AUTO_APPROVE` | Riskli tool'lar icin auto onay | `false` | Hayir | `true` ise mutating aksiyonlar sorulmadan gider |
| `SENTINEL_SESSION_DIR` | Oturum dosya dizini | `./.sentinel/sessions` | Hayir | JSON session dosyalari |
| `SENTINEL_TRAJECTORY_DIR` | Trajectory dizini | `./.sentinel/trajectories` | Hayir | JSONL trajectory |
| `SENTINEL_TRAJECTORY_ENABLED` | Trajectory kaydi | `false` | Hayir | Varsayilan kapali |

## Profil notu

- `cloud`: OpenAI uyumlu uzak HTTP
- `local`: OpenAI uyumlu lokal HTTP
- `anthropic`: Anthropic Messages API

Bilinmeyen profilde CLI `ConfigError` ile anlamli hata verir.
