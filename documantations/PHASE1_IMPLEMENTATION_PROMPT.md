# Faz 1 — Sentinel Test Platformu: Uygulayıcı Prompt

> Bu belge, başka bir Claude Code oturumuna **olduğu gibi yapıştırılmak** üzere hazırlanmıştır.
> Yapıştıran oturum, aşağıdaki kararları **tartışmadan** uygular ve Faz 1’i bitirir.

---

## Rolün

Sen bu repo’da doğrudan kod yazan **uygulayıcı AI**’sın. Plan yapmıyor, mimari önermiyorsun;
yöneticinin verdiği kararları `test-platform/` altında **koda dönüştürüyorsun**.

Referansın: `sentinel-coming/skills/target-app-*` skill’leri. Her dosyayı yazmadan önce
ilgili skill’i oku; skill içeriğini bu belgeye kopyalamadık, **skill’e yönlendirdik**.

Çalışma dizini: `test-platform/` (repo kökünde, `sentinel-coming/` ile kardeş).

---

## Kesin kararlar (değişmez, tartışma yok)

- **Dil/Framework**: Python 3.11+, FastAPI, async SQLAlchemy, redis-py async, httpx async.
- **Gözlemlenebilirlik**: yalnızca OpenTelemetry SDK + **OTLP/gRPC push**.
- **Yasak**: `prometheus_client`, Prometheus `ServiceMonitor`, Promtail, sidecar scrape,
  cluster kurulumu (COS Faz 2’de), CLI/TUI (Faz 3’te).
- **Namespace**: `sentinel-target`. Her pod tek replica.
- **OTEL Resource attrs** (zorunlu): `service.name`, `service.version`, `deployment.environment`.
- **Collector endpoint**: `OTEL_EXPORTER_OTLP_ENDPOINT` env’den okunur. **Default yok** —
  eksikse servis fail-fast (bootstrap sırasında `sys.exit(1)`).
- **Protokol**: `OTEL_EXPORTER_OTLP_PROTOCOL=grpc` sabit.

---

## Servis topolojisi (özet)

Kaynak: `skills/target-app-service-topology` (oku — uçlar/DB şeması orada).

```
             ┌──────────┐
client ─▶    │ gateway  │ 8080   (public-ish /api/*, /health)
             └────┬─────┘
                  │ httpx
         ┌────────┼──────────┐
         ▼        ▼          ▼
     orders   payments   inventory        (internal 8080, /health, /admin/chaos)
       │         │           │
       ├──── Postgres (orders_db, payments_db, inventory_db) ────┐
       │         │           │                                    │
       └──── Redis (cache + pub/sub) ───────────────────────────┐ │
                                                                 ▼ ▼
                                                               worker
                                                        (redis queue consumer,
                                                         no HTTP ingress)
```

- **gateway**: `POST /api/orders`, `GET /api/orders/{id}`, `GET /api/inventory/{sku}`,
  `GET /health`. İç servislere httpx ile fan-out; trace propagation zorunlu.
- **orders**: sipariş CRUD; payments + inventory çağırır; Postgres + Redis cache.
- **payments**: ödeme simülasyonu; konfigüre edilebilir latency/hata. Postgres yazar.
- **inventory**: SKU stok sorgusu; Redis cache-through Postgres.
- **worker**: HTTP ingress **yok**; Redis queue (`orders.events`) dinler; side-effect işler.

---

## Repo hedef yapısı

```
test-platform/
├── libs/
│   └── observability/            # paylaşılan OTEL bootstrap + middleware
│       ├── pyproject.toml
│       └── sentinel_obs/
│           ├── __init__.py
│           ├── bootstrap.py      # init_tracing/metrics/logs
│           ├── fastapi.py        # instrument_app, request middleware
│           ├── chaos.py          # latency/error injection middleware
│           └── clients.py        # httpx/sqlalchemy/redis instrument helpers
├── services/
│   ├── gateway/
│   │   ├── app/{main.py,routes.py,clients.py,config.py}
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   ├── orders/      (aynı yapı + models.py, db.py)
│   ├── payments/    (aynı yapı)
│   ├── inventory/   (aynı yapı)
│   └── worker/      (app/main.py: redis consumer loop)
├── load/
│   ├── locustfile.py
│   └── scenarios/{steady.py,diurnal.py,flash_crowd.py,gradual_degradation.py}
├── chaos/
│   └── profiles/{healthy.yaml,slow-db.yaml,downstream-outage.yaml,
│                 memory-leak.yaml,cache-stampede.yaml,cascading.yaml}
├── k8s/
│   ├── namespace.yaml
│   ├── postgres.yaml  redis.yaml  otel-collector.yaml
│   ├── gateway.yaml   orders.yaml  payments.yaml  inventory.yaml  worker.yaml
│   ├── networkpolicy.yaml
│   └── kustomization.yaml
├── scripts/
│   ├── scenario_runner.py        # ground-truth.jsonl yazar
│   └── seed_db.py
├── docker-compose.yaml           # local dev (otel-collector stub dahil)
└── README.md
```

---

## Uygulama sırası — 3 aşama

### Aşama 1.A — İskelet + Observability

**Hedef**: 4 FastAPI servisi + worker ayağa kalkar, OTLP’ye trace/metric/log yollar.

1. `libs/observability/` paketini yaz.
   - Skill: `skills/target-app-observability-lib`
   - Skill: `skills/target-app-fastapi-otel-bootstrap`
   - `init_telemetry(service_name, service_version)` tek giriş noktası.
   - Tracer, Meter, Logger provider’ları OTLP/gRPC exporter ile kurulur.
   - FastAPI, httpx, SQLAlchemy, redis-py instrumentor’ları devreye alınır.
2. Her servis için `app/main.py`:
   - `init_telemetry()` ilk satırda çağrılır.
   - `/health` → 200 `{"status":"ok","service":...}`.
   - Config `pydantic-settings` ile env’den (DB_URL, REDIS_URL, OTLP endpoint…).
3. `orders`, `payments`, `inventory` için async SQLAlchemy modelleri + migration (Alembic
   gerekli değil; `scripts/seed_db.py` içinde `create_all` yeterli).
4. `gateway/clients.py`: httpx.AsyncClient, timeout 2s, retries **yok** (chaos görünür kalsın).
5. `worker/app/main.py`: `redis.asyncio` ile blocking pop; her iş için manuel span.
6. Her servise `Dockerfile` (python:3.11-slim, non-root user, `uvicorn` ile start).
7. `docker-compose.yaml`:
   - postgres:15, redis:7, `otel/opentelemetry-collector-contrib` (logging exporter stub).
   - 4 servis + worker. `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317`.

**Biter**: `docker compose up` → tüm /health 200; collector loglarında spans/metrics akışı.

---

### Aşama 1.B — Chaos + Trafik

**Hedef**: Davranışı runtime’da bozabiliyor, gerçekçi yük üretebiliyoruz.

1. Chaos middleware (`libs/observability/sentinel_obs/chaos.py`):
   - Skill: `skills/target-app-chaos-api`
   - Her request öncesi **aktif profil** okunur (process-local cache).
   - Profil alanları: `latency_ms_p50`, `latency_ms_p99`, `error_rate`, `error_status`,
     `downstream_block: [service]`, `memory_leak_kb_per_req`.
   - Middleware tüm route’lara uygulanır; `/health` ve `/admin/*` **hariç**.
2. `/admin/chaos` API (her serviste):
   - `GET /admin/chaos` aktif profili döner.
   - `PUT /admin/chaos` body’den yeni profil alır (in-memory).
   - `POST /admin/chaos/reload` ConfigMap’ten dosya okur (`/etc/chaos/profile.yaml`).
3. ConfigMap-driven profiller: `chaos/profiles/*.yaml` — aşağıdaki 6 senaryo:
   `healthy`, `slow-db`, `downstream-outage`, `memory-leak`, `cache-stampede`, `cascading`.
4. Locust senaryoları (`load/scenarios/`):
   - Skill: `skills/target-app-load-generator`
   - `steady.py`: sabit RPS (örn. 50 rps, 30 dk).
   - `diurnal.py`: sinüzoidal, 10→80 rps, 2 saat.
   - `flash_crowd.py`: 20 rps baseline, 3. dk’da 5x spike 5 dk, sonra düşüş.
   - `gradual_degradation.py`: RPS sabit, hata oranı 0→%20 rampa.
5. `locustfile.py` master switch — env `SCENARIO=steady` ile seçer.

**Biter**: `PUT /admin/chaos` profil değişince p99 latency/error rate OTEL’de görünür.
Locust başlatılabilir ve seçilen senaryoya uyar.

---

### Aşama 1.C — K8s + Ground Truth

**Hedef**: kind/minikube üzerinde çalışır + her senaryo için ground-truth üretilir.

1. `k8s/` manifestleri:
   - Skill: `skills/target-app-k8s-manifests`
   - `namespace.yaml`: `sentinel-target`.
   - Her servis Deployment: `replicas: 1`, `resources.limits: {cpu: 100m, memory: 128Mi}`,
     `requests: {cpu: 50m, memory: 64Mi}`. Worker biraz daha gevşek (256Mi).
   - ConfigMap `chaos-profile` → `/etc/chaos/profile.yaml` mount.
   - Postgres/Redis StatefulSet (tek replica, `emptyDir` OK — test platformu).
   - `otel-collector` Deployment + Service (`4317/grpc`).
   - `NetworkPolicy`: `/admin/*` **sadece** namespace içi; dış trafik yalnız `gateway:8080`.
2. `scripts/scenario_runner.py`:
   - Skill: `skills/target-app-ground-truth-annotator`
   - Args: `--scenario <name> --duration 30m --out ground-truth.jsonl`.
   - Akış: chaos profilini uygula (kubectl patch configmap + reload POST) →
     locust senaryosunu başlat → başlangıç/bitiş timestamp’lerini,
     beklenen semptomları, hedef servisi JSONL’e yaz →
     senaryo bitince `healthy`’e döndür.
   - JSONL şeması (örnek):
     ```json
     {"scenario":"slow-db","start":"2026-04-19T10:00:00Z","end":"...",
      "target_service":"orders","expected_symptoms":["p99_latency_spike","db_wait_time_up"],
      "ground_truth_root_cause":"postgres.query_latency"}
     ```

**Biter**: 6 senaryo tek komutla koşulabilir, `ground-truth.jsonl` birikir,
OTLP collector’e tutarlı veri akar.

---

## Referans skill’ler (kod yazmadan **önce** oku)

- `skills/target-app-repo-layout` — dosya yerleşimi kesin referans
- `skills/target-app-observability-lib` — OTEL bootstrap API’si
- `skills/target-app-fastapi-otel-bootstrap` — FastAPI entegrasyonu
- `skills/target-app-service-topology` — uçlar + DB şemaları
- `skills/target-app-chaos-api` — profil şeması + middleware semantiği
- `skills/target-app-load-generator` — Locust senaryo API’si
- `skills/target-app-k8s-manifests` — resource/limit/NetworkPolicy standardı
- `skills/target-app-ground-truth-annotator` — JSONL şeması + runner akışı

Skill mevcut değilse: **dur**, yöneticiye bildir. Uydurma.

---

## Çıktı beklentileri (Exit criteria — hepsi geçmeli)

- [ ] Her servis için `docker build` hatasız.
- [ ] `docker compose up` sonrası 5 servisin de `/health` → 200.
- [ ] Locust `steady` senaryosu çalışırken OTLP collector loglarında
      trace + metric + log (her üçü de) akışı.
- [ ] `PUT /admin/chaos` ile `slow-db` profiline geçiş sonrası p99 latency artışı OTEL’de.
- [ ] 6 senaryo (`healthy`, `slow-db`, `downstream-outage`, `memory-leak`,
      `cache-stampede`, `cascading`) `scripts/scenario_runner.py` ile koşuluyor.
- [ ] `ground-truth.jsonl` senaryo başına en az 1 satır üretiyor, şema tutarlı.
- [ ] `kubectl apply -k k8s/` kind cluster’da temiz ayağa kalkıyor.
- [ ] `NetworkPolicy` aktifken `/admin/chaos` dışarıdan erişilemiyor (kanıt: test).

---

## Kurallar (ihlal = revert)

- **Unbounded label YASAK**: `user_id`, `order_id`, `trace_id`… metric label olamaz.
  Span attribute olabilir. Cardinality patlatma.
- `/admin/*` dışa açılmaz; NetworkPolicy + cluster-internal Service.
- Tek replica, agresif limit (tipik 100m CPU / 128Mi memory).
- Secret hardcode **yok**; `env` veya K8s `Secret`.
- `OTEL_EXPORTER_OTLP_ENDPOINT` eksikse servis **fail-fast** (`sys.exit(1)`).
- Git commit’leri atomik; **aşama başına** mantıksal gruplama
  (`feat(phase1a): ...`, `feat(phase1b): ...`, `feat(phase1c): ...`).
- Her PR/commit grubu öncesi: `ruff check` + `mypy --strict` temiz.

---

## Yapma (Faz 1 kapsamı dışı)

- Prometheus scrape / pull-based metric / `prometheus_client`.
- Grafana / Loki / Tempo / COS kurulumu — **Faz 2**.
- Juju, MicroK8s setup — **Faz 2**.
- CLI, TUI, dashboard — **Faz 3**.
- Yeni mimari önerisi, plan belgesi, ADR. Yöneticiye sor; kendin yazma.
- Test platformu dışına dosya (repo kökündeki `skills/`, `docs/`… dokunma).

---

## Başlangıç adımları (bu sırayla)

1. `skills/target-app-repo-layout` oku → `test-platform/` dizin ağacını oluştur (boş dosyalar OK).
2. `libs/observability/` paketini yaz; **önce** gateway servisiyle entegre et.
3. `docker-compose.yaml` ile `otel/opentelemetry-collector-contrib` stub’ı kur
   (logging exporter). Gateway → collector akışını doğrula.
4. Sırasıyla orders → payments → inventory → worker.
5. Aşama 1.A exit kriterlerini geç, commit et.
6. Aşama 1.B (chaos + load) — commit.
7. Aşama 1.C (k8s + scenario runner) — commit.
8. Tüm exit kriterlerini checklist halinde yöneticiye raporla.

---

**Bittiğinde**: exit criteria checklist’ini doldurmuş olarak, sadece şu formatta raporla:
`Faz 1 complete. <X/Y> exit criteria passed. Blocked on: <list or none>.`
