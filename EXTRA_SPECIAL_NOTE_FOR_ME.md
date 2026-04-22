# Sentinel Extra Special Note (Personal Runbook)

Bu not, Sentinel monorepo'da COS + test-platform + observability-gateway + CLI zincirini hizli ve guvenli sekilde calistirmak icin tek sayfalik operasyon ozetidir.

## 1) Bu turda neyi tamamladik?

- Telemetry akisini `sentinel-target` local collector odagindan alip COS `otel-collector` odagina tasidik.
- test-platform servislerini COS backend'lerine (Prometheus/Loki/Tempo) veri akitacak sekilde sabitledik.
- `observability-gateway` katmanini read-only tek giris noktasi yaptik.
- CLI `doctor`, `obs metric/logs/traces` ve `run/repl` akisini gateway uzerinden canli veriyle dogruladik.
- Full smoke script'ini (`test-platform/scripts/run_cos_stack_check.sh`) uctan uca zinciri tek komutta test edecek hale getirdik.
- Local smoke script'ini (`test-platform/scripts/run_local_stack_check.sh`) ayni topolojiye hizaladik.
- CLI varsayilanlarini cloud + Gemini eksenine cektik; local Gemma fallback olarak korundu.

## 2) Mimari (hedeflenen calisma sekli)

1. test-platform servisleri telemetry'yi COS `otel-collector`'a gonderir.
2. COS stack telemetry'yi Prometheus/Loki/Tempo'da gorunur yapar.
3. `observability-gateway` sadece bu backend'leri read-only okur.
4. CLI backend'lere direkt gitmez; sadece gateway'e baglanir.
5. CLI agent (`run/repl`) gerekirse gateway tool'lari ile canli veri ceker.

## 3) Onkosullar (baslamadan once)

- Juju/COS ayakta olmali:
  - `juju status` icinde `prometheus`, `loki`, `tempo`, `otel-collector` active gorunmeli.
- MicroK8s hazir olmali:
  - `microk8s status --wait-ready` basarili olmali.
- Repo `.venv` hazir olmali:
  - `~/Desktop/sentinel/sentinel-coming/.venv/bin/python` mevcut olmali.

## 4) En hizli dogru yol (onerilen)

```bash
cd ~/Desktop/sentinel/sentinel-coming/test-platform
./scripts/run_cos_stack_check.sh
```

Bu komut tek seferde sunlari yapar:

- altyapi kontrolu
- servisleri ayaga kaldirma
- trafik uretme
- Prometheus/Loki/Tempo dogrulama
- observability-gateway dogrulama
- CLI `doctor/obs` dogrulama
- CLI `run` agent smoke dogrulama

## 5) Beklenen basarili cikti

Terminal sonunda asagidaki gibi satirlari gormelisin:

- `[cos-smoke] prometheus target_info has data`
- `[cos-smoke] prometheus orders metric has data`
- `[cos-smoke] loki has gateway logs`
- `[cos-smoke] tempo has orders traces`
- `[cos-smoke] COS smoke test passed`
- `logs=.../test-platform/runs/cos-smoke-YYYYMMDD-HHMMSS`

## 6) Smoke artefact klasoru ne icermeli?

Ornek klasor:

`test-platform/runs/cos-smoke-YYYYMMDD-HHMMSS/`

Kritik dosyalar:

- `observability-gateway.log`
- `observability-gateway-health.json`
- `observability-gateway-status.json`
- `cli-doctor.json`
- `cli-obs-metric.json`
- `cli-obs-logs.json`
- `cli-obs-traces.json`
- `cli-agent-run.json`
- `prom-target-info.json`
- `prom-orders-created.json`
- `loki-gateway.json`
- `tempo-orders.json`

## 7) Manual calistirma (smoke disinda canli kullanim)

### 7.1 Gateway'i ayaga kaldir

```bash
cd ~/Desktop/sentinel/sentinel-coming/observability-gateway
source ../.venv/bin/activate

export SENTINEL_OBSERVABILITY_GATEWAY_TOKEN=sentinel-observability-gateway-token
export SENTINEL_OBSERVABILITY_PROMETHEUS__BASE_URL=http://10.152.183.210:9090
export SENTINEL_OBSERVABILITY_LOKI__BASE_URL=http://10.152.183.93:3100
export SENTINEL_OBSERVABILITY_TEMPO__BASE_URL=http://10.152.183.132:3200

python -m uvicorn observability_gateway.main:app --host 127.0.0.1 --port 8091
```

> Not: `address already in use` alirsan 8091 portunda eski proses vardir.

### 7.2 CLI tarafini bagla

```bash
cd ~/Desktop/sentinel/sentinel-coming/cli
source .venv/bin/activate

export SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL=http://127.0.0.1:8091
export SENTINEL_OBSERVABILITY_GATEWAY_TOKEN=sentinel-observability-gateway-token
```

### 7.3 Hemen saglik kontrolu

```bash
python -m sentinel_cli doctor --profile local
python -m sentinel_cli obs metric 'app_orders_created_total'
python -m sentinel_cli obs logs --service gateway
python -m sentinel_cli obs traces --service orders
```

Beklenti:

- `doctor` icinde `observability_gateway.ok = true`
- metric sonucunda `backend: prometheus`
- logs sonucunda `backend: loki`
- traces sonucunda `backend: tempo`

### 7.4 Agent testi

```bash
python -m sentinel_cli run --profile local "orders servisinde son 10 dakikada anomali var mi?"
```

## 8) Sik gorulen problemler ve hizli cozum

### Problem A: `Gateway authentication failed`

Kontrol:

- Gateway process ayakta mi?
- CLI tarafinda token export edildi mi?
- Gateway tarafinda ayni token export edildi mi?

Cozum:

- Hem gateway hem CLI terminalinde `SENTINEL_OBSERVABILITY_GATEWAY_TOKEN` degerlerini esitle.

### Problem B: `address already in use` (8091)

Cozum:

```bash
ss -ltnp | grep 8091
pkill -f 'uvicorn observability_gateway.main:app --host 127.0.0.1 --port 8091'
ss -ltnp | grep 8091
```

Sonra gateway'i yeniden baslat.

### Problem C: Smoke bitti ama manuel `run` fail

Neden:

- `run_cos_stack_check.sh` bitince cleanup trap ile local process'leri kapatir.

Cozum:

- Gateway'i ayri terminalde kalici sekilde tekrar baslat.

### Problem D: COS backend'e erisim sorunlari

Cozum:

- `scripts/cos-microk8s-heal.sh` calistir.
- `juju status` ve `microk8s status --wait-ready` ile tekrar kontrol et.

## 9) Gunluk operasyon akisi (kisa checklist)

1. `juju status` -> COS app'ler active mi?
2. `microk8s status --wait-ready` -> cluster hazir mi?
3. `./scripts/run_cos_stack_check.sh` -> full zincir yesil mi?
4. Gerekirse gateway'i ayri terminalde ac.
5. CLI `doctor` + `obs` + `run` ile canli test yap.
6. `test-platform/runs/...` altindaki artefactlari incele.

## 10) Basarili kabul sinyalleri

- Prometheus'ta `app_orders_created_total` geliyor.
- Loki'de gateway loglari gorunuyor.
- Tempo'da orders trace'leri gorunuyor.
- Gateway health/status 200 donuyor.
- CLI `doctor/obs` dogru backend'lerden veri aliyor.
- CLI `run/repl` gateway tool kullanabiliyor.

## 11) Notlar

- Bu akista hedef "tek dogru local/topoloji"dir: CLI -> gateway -> COS backend'leri.
- test-platform smoke run klasorleri zamanla birikir; gerekirse temizlik yap.
- Gercek secret degerlerini repoya yazma; environment variable ile yonet.
