# sentinel-observability-gateway

Sentinel CLI icin tek observability giris noktasi saglayan, read-only calisan bir FastAPI servisidir. Prometheus, Loki ve Tempo'ya dogrudan HTTP ile baglanir; Grafana zorunlu degildir.

## Kapsam

- Prometheus metric sorgulari
- Loki `query_range` log sorgulari
- Tempo trace arama ve trace detay alma
- Secret-safe durum ve hata modeli
- Ortak timeout / retry ayarlari

Ilk surum kasitli olarak su alanlari kapsamaz:

- write islemleri
- alert yonetimi
- dashboard yonetimi
- LLM entegrasyonu
- Grafana datasource query katmani

## Konfigurasyon

Servis YAML dosyasi ve environment override ile calisir.

Ornek `config.yaml`:

```yaml
service_name: sentinel-observability-gateway
service_version: 0.1.0
http:
  timeout_sec: 10
  retry:
    max_attempts: 3
    backoff_base_sec: 0.5
prometheus:
  base_url: http://127.0.0.1:9090
  token_env: SENTINEL_PROMETHEUS_TOKEN
loki:
  base_url: http://127.0.0.1:3100
tempo:
  base_url: http://127.0.0.1:3200
```

Desteklenen env override formati:

```bash
export SENTINEL_OBSERVABILITY_CONFIG_PATH=./config.yaml
export SENTINEL_OBSERVABILITY_PROMETHEUS__BASE_URL=http://127.0.0.1:9090
export SENTINEL_OBSERVABILITY_PROMETHEUS__TOKEN_ENV=SENTINEL_PROMETHEUS_TOKEN
export SENTINEL_OBSERVABILITY_LOKI__BASE_URL=http://127.0.0.1:3100
export SENTINEL_OBSERVABILITY_TEMPO__BASE_URL=http://127.0.0.1:3200
export SENTINEL_OBSERVABILITY_HTTP__TIMEOUT_SEC=10
export SENTINEL_OBSERVABILITY_HTTP__RETRY__MAX_ATTEMPTS=3
```

## Calistirma

```bash
cd sentinel-coming/observability-gateway
pip install -e ".[dev]"
sentinel-observability-gateway
```

Alternatif:

```bash
uvicorn observability_gateway.main:app --host 0.0.0.0 --port 8091
```

## API

- `GET /health`
- `GET /api/v1/status`
- `POST /api/v1/metrics/query`
- `POST /api/v1/logs/query_range`
- `POST /api/v1/traces/search`
- `GET /api/v1/traces/{trace_id}`

Tum hata yanitlari su modeli kullanir:

```json
{
  "error": {
    "backend": "tempo",
    "status": 504,
    "message": "Tempo request timed out.",
    "retryable": true
  }
}
```

## Test

```bash
cd sentinel-coming/observability-gateway
python -m pytest -q
```
