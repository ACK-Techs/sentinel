---
name: test-load-locust
description: "Locust ile Sentinel HTTP API yük testi; kullanıcı davranış senaryoları, stage tanımı, custom metrikler ve P95/P99 gecikme hedefleri"
---

## Purpose
Sentinel API'sinin gerçek yük altındaki performansını ölçmek; P95 gecikme, hata oranı ve RPS hedeflerine göre pass/fail kararı almak.

## Workflow

### Locustfile Yapısı
```python
# locustfile.py
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner
import json

class SentinelAPIUser(HttpUser):
    wait_time = between(0.5, 2.0)  # istekler arası bekleme
    
    def on_start(self):
        """Her kullanıcı başlangıcında auth token al"""
        resp = self.client.post("/api/v1/auth/token", json={
            "username": "loadtest",
            "password": "loadtest123"
        })
        self.token = resp.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(5)  # ağırlık 5 — en sık çağrılan
    def query_metrics(self):
        self.client.get(
            "/api/v1/metrics",
            params={"query": "up", "time": "now"},
            headers=self.headers,
            name="/api/v1/metrics [instant]"
        )
    
    @task(3)
    def query_metrics_range(self):
        self.client.get(
            "/api/v1/metrics/range",
            params={
                "query": "rate(http_requests_total[5m])",
                "start": "now-1h",
                "end": "now",
                "step": "60s"
            },
            headers=self.headers,
            name="/api/v1/metrics [range]"
        )
    
    @task(2)
    def query_logs(self):
        self.client.get(
            "/api/v1/logs",
            params={"query": '{job="sentinel"}', "limit": "50"},
            headers=self.headers,
            name="/api/v1/logs"
        )
    
    @task(1)
    def health_check(self):
        self.client.get("/health", name="/health")
```

### Load Stage Tanımı
```python
# load_stages.py — headless çalıştırma için
from locust import LoadTestShape

class SentinelLoadShape(LoadTestShape):
    """
    Aşamalı yük artışı:
    0-60s:   0→50 kullanıcı (warmup)
    60-180s: 50 kullanıcı (sabit)
    180-240s: 50→150 kullanıcı (peak)
    240-300s: 150 kullanıcı (peak hold)
    300-360s: 150→0 kullanıcı (cooldown)
    """
    stages = [
        {"duration": 60,  "users": 50,  "spawn_rate": 2},
        {"duration": 180, "users": 50,  "spawn_rate": 50},
        {"duration": 240, "users": 150, "spawn_rate": 5},
        {"duration": 300, "users": 150, "spawn_rate": 150},
        {"duration": 360, "users": 0,   "spawn_rate": 10},
    ]
    
    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None
```

### CI'da Headless Çalıştırma
```bash
# Sentinel API'ye karşı yük testi
locust \
  --headless \
  --users 100 \
  --spawn-rate 10 \
  --run-time 120s \
  --host http://sentinel-api:8000 \
  --csv results/load_test \
  --html results/report.html \
  --exit-code-on-error 1

# P95 < 500ms, hata < %1 kontrolü
python scripts/check_locust_results.py results/load_test_stats.csv \
  --p95-threshold 500 \
  --error-rate-threshold 0.01
```

### Sonuç Doğrulama Script
```python
# scripts/check_locust_results.py
import csv
import sys
import argparse

def check_results(csv_path: str, p95_ms: float, error_rate: float):
    failures = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Name"] == "Aggregated":
                actual_p95 = float(row["95%"])
                actual_error = float(row["Failure Count"]) / max(float(row["Request Count"]), 1)
                
                if actual_p95 > p95_ms:
                    failures.append(f"P95 {actual_p95}ms > eşik {p95_ms}ms")
                if actual_error > error_rate:
                    failures.append(f"Hata oranı {actual_error:.2%} > eşik {error_rate:.2%}")
    
    if failures:
        print("BAŞARISIZ:", *failures, sep="\n  ")
        sys.exit(1)
    print("Tüm eşikler geçildi")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--p95-threshold", type=float, default=500)
    parser.add_argument("--error-rate-threshold", type=float, default=0.01)
    args = parser.parse_args()
    check_results(args.csv_path, args.p95_threshold, args.error_rate_threshold)
```

## Common mistakes
- `wait_time = constant(0)` ile test yapmak — gerçekçi değil; `between(0.5, 2.0)` kullanıcı davranışını simüle eder
- Warmup aşaması olmadan hemen peak yüke çıkmak — sunucu JIT/cache warmup'ı tamamlamadan ölçüm yaparsan sonuçlar yanlış
- Authentication olmadan korumalı endpoint test etmek — 401 hataları P95'i bozar
- Tek kullanıcı tipiyle test etmek — read/write oranını gerçek kullanıma göre `@task` ağırlıklarıyla ayarla

## References
- `skills/test-load-k6`
- `skills/perf-p99-latency-tuning`
