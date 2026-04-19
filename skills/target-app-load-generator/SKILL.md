---
name: target-app-load-generator
description: load/ klasörü — Locust tabanlı trafik üretici, YAML senaryolar (steady-state, diurnal, flash-crowd, gradual-degradation).
---

## Purpose
Gerçekçi ve **tekrar-edilebilir** trafik profilleri üreterek Sentinel'in baseline öğrenmesi ve anomali tespitini test etmek. Tek bir load pod'u, env ile senaryo seçer.

## When to Use
- Yeni bir chaos senaryosu için trafik altına alma gerektiğinde.
- SLO baseline'ı öğrenmek için 24 saatlik diurnal akışı çalıştırırken.
- CI smoke testinde kısa (2 dk) steady-state çalıştırırken.

## Contract / Interface
Klasör:
```
load/
  locustfile.py           # HttpUser + tasks
  scenarios/
    steady-state.yaml
    diurnal.yaml
    flash-crowd.yaml
    gradual-degradation.yaml
  Dockerfile
```
Senaryo YAML şeması:
```yaml
name: diurnal
duration_s: 86400
host: http://gateway.sentinel-target.svc:8000
stages:                  # LoadTestShape adımları
  - duration_s: 3600
    users: 10
    spawn_rate: 1
  - duration_s: 3600
    users: 200
    spawn_rate: 5
endpoints:               # task weights
  "POST /api/orders": 70
  "GET /work?ms=50": 20
  "GET /flaky": 10
```
Env: `SCENARIO=diurnal` → `scenarios/diurnal.yaml` yüklenir.

Senaryolar:
- **steady-state**: 50 user, 30 dk — baseline.
- **diurnal**: 24 saat, gündüz yüksek / gece düşük sinüsoid.
- **flash-crowd**: 5 dk steady + 2 dk 10x spike + 10 dk recovery.
- **gradual-degradation**: sabit RPS, chaos_api dışarıdan `slow-burn` profiline alınır (scenario-runner koordine eder).

## Implementation Notes
- Locust `LoadTestShape` subclass'ı YAML'den `stages` okur, `tick()` döner.
- Task weight'leri `@task(weight)` yerine YAML'den dinamik üretmek için `UserClass.tasks = {fn: weight, ...}` runtime'da atanır.
- Locust kendi OTEL'ini yayınlamaz — request sonuçları stdout + CSV; **ground-truth log** scenario-runner tarafından ayrı tutulur.
- Alternatif minimal implementasyon: `asyncio + httpx` + token-bucket; sadece senaryo basit ise.
- Load pod'u `sentinel-target` namespace'i içinde çalışır, dış ingress kullanmaz (cluster-internal gateway Service'i).

## Anti-patterns
1. Load generator'a OTEL tracer enjekte edip trace yayınlatmak — synthetic trafiği gerçekten ayırt edilemez hale getirir; ground-truth bozulur. Sadece HTTP header `X-Synthetic: 1` yeterli.
2. Farklı senaryoları **tek çalıştırmada karıştırmak** — hangi anomali hangi profile ait olduğu bulunamaz.
3. `spawn_rate`'i `users` ile aynı veya büyük tutmak — anlık ramp; diurnal baseline'ı bozar.
4. Client-side timeout'u 30 sn'ye çıkarmak — gerçek user 2-3 sn bekler; metrikler gerçekçi olmaz.
5. Docker image'da `locust` ile birlikte `opentelemetry-*` paketleri yüklemek — gereksiz bağımlılık, container size şişer.

## Example Snippet
```python
# load/locustfile.py
import os, yaml, random
from locust import HttpUser, task, LoadTestShape, events

SCENARIO = yaml.safe_load(open(f"scenarios/{os.environ['SCENARIO']}.yaml"))

class Shape(LoadTestShape):
    def tick(self):
        t = self.get_run_time()
        elapsed = 0
        for s in SCENARIO["stages"]:
            if t < elapsed + s["duration_s"]:
                return (s["users"], s["spawn_rate"])
            elapsed += s["duration_s"]
        return None

class TargetUser(HttpUser):
    host = SCENARIO["host"]
    @task
    def mixed(self):
        r = random.randint(1, sum(SCENARIO["endpoints"].values()))
        cum = 0
        for ep, w in SCENARIO["endpoints"].items():
            cum += w
            if r <= cum:
                method, path = ep.split(" ", 1)
                self.client.request(method, path, headers={"X-Synthetic": "1"},
                                    json={"sku": "A", "qty": 1, "amount": 10}
                                    if method == "POST" else None, name=ep)
                return
```
