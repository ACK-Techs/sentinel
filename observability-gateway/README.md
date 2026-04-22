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

## Lab Ops Rehberi

Bu servis lab/local akis icin tek proses olarak calistirilir. Uretim dagitimi, process supervisor, TLS termination veya secret rotation bu README'nin kapsami disindadir.

En kisa local baslatma:

```bash
cd sentinel-coming/observability-gateway
export SENTINEL_OBSERVABILITY_PROMETHEUS__BASE_URL=http://127.0.0.1:9090
export SENTINEL_OBSERVABILITY_LOKI__BASE_URL=http://127.0.0.1:3100
export SENTINEL_OBSERVABILITY_TEMPO__BASE_URL=http://127.0.0.1:3200
uvicorn observability_gateway.main:app --host 127.0.0.1 --port 8091
```

Hizli dogrulama:

```bash
curl -fsS http://127.0.0.1:8091/health
curl -fsS http://127.0.0.1:8091/api/v1/status | jq .
curl -fsS -X POST http://127.0.0.1:8091/api/v1/metrics/query \
  -H 'content-type: application/json' \
  -d '{"query":"up"}' | jq .
```

Run klasoru mantigi:

- `test-platform/scripts/run_cos_stack_check.sh` calistiginda artefactlar `test-platform/runs/cos-smoke-YYYYMMDD-HHMMSS/` altina yazilir.
- Gateway logu `observability-gateway.log`, health sonucu `observability-gateway-health.json`, durum ozeti `observability-gateway-status.json` olarak kaydedilir.
- CLI smoke ciktilari ayni klasorde `cli-doctor.json`, `cli-obs-metric.json`, `cli-obs-logs.json`, `cli-obs-traces.json` adlariyla tutulur.

## Troubleshooting

- `GET /health` gecmiyor ise once proses logunu kontrol edin: `test-platform/runs/.../observability-gateway.log`
- `GET /api/v1/status` icinde backend `configured=false` gorunuyorsa ilgili `SENTINEL_OBSERVABILITY_*__BASE_URL` env degerini kontrol edin.
- Metric geliyor ama logs/traces bos ise once `test-platform/scripts/run_cos_stack_check.sh` icindeki trafik uretim adimlarinin tamamlandigini dogrulayin.
- 401/403 aliyorsaniz gateway token env ve gerekiyorsa upstream backend token env eslesmesini kontrol edin.
- Bu ilk akis sadece local port-forward ve tek proses icindir; ingress, TLS ve multi-user beklentisiyle kullanmayin.

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
