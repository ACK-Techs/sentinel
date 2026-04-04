# Faz 2.E Hızlı Başlangıç

Bu belge, Sentinel CLI'yi iki ana profil ile hızlıca ayağa kaldırmak için kopyala-çalıştır blokları verir. Gerçek API anahtarı yazmayın; placeholder kullanın ve değeri yerel kabuğunuzda değiştirin.

## Kurulum

```bash
cd sentinel-coming/cli
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

İsteğe bağlı MCP desteği için:

```bash
cd sentinel-coming/cli
source .venv/bin/activate
python -m pip install -e ".[dev,mcp]"
```

`uv` kullanıyorsanız:

```bash
cd sentinel-coming/cli
uv sync --extra dev
uv run python -m sentinel_cli doctor --profile local
```

## Cloud profil

```bash
cd sentinel-coming/cli
source .venv/bin/activate

export SENTINEL_PROFILE=cloud
export SENTINEL_OPENAI_BASE_URL=https://api.example.com/v1
export SENTINEL_API_KEY=sentinel_api_key_placeholder
export SENTINEL_MODEL=provider-model-placeholder

python -m sentinel_cli doctor --profile cloud
python -m sentinel_cli run --profile cloud "Grafana durumunu ozetle"
```

## Local profil

```bash
cd sentinel-coming/cli
source .venv/bin/activate

export SENTINEL_PROFILE=local
export SENTINEL_LOCAL_BASE_URL=http://127.0.0.1:11434/v1
export SENTINEL_LOCAL_MODEL=local_model_placeholder

python -m sentinel_cli doctor --profile local
python -m sentinel_cli run --profile local "Prometheus sagligini kontrol et"
```

## Mini hata tablosu

| Sorun | Ne kontrol et | Sonraki komut |
|-------|---------------|---------------|
| `ModuleNotFoundError` | Sanal ortam aktif mi, editable install yapildi mi | `python -m pip install -e ".[dev]"` |
| `401` veya auth hatasi | `SENTINEL_API_KEY` ve profil dogru mu | `python -m sentinel_cli doctor --profile cloud` |
| Lokal baglanti reddi | Lokal servis ayakta mi, port ve `base_url` dogru mu | `python -m sentinel_cli doctor --profile local` |
| Model bulunamadi | `SENTINEL_MODEL` veya `SENTINEL_LOCAL_MODEL` dogru mu | Profil env'lerini tekrar kontrol et |
| MCP gorunmuyor | `.[mcp]` kurulu mu, `mcp.enabled` ve ilgili stdio sunucusu acik mi | `python -m sentinel_cli doctor --profile local` |

## İlgili belgeler

- `LLM_PROVIDERS.md`
- `CONFIG_REFERENCE_PHASE2B.md`
- `CLI_RUNTIME_PHASE2C.md`
