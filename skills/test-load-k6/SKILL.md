---
name: test-load-k6
description: "k6 ile JavaScript tabanlı Sentinel API yük testi; threshold tanımı, scenario bazlı yük, check API ve Prometheus remote write entegrasyonu"
---

## Purpose
k6'yı kullanarak Sentinel API'sine karşı gerçekçi yük senaryoları çalıştırmak, SLO eşiklerini tanımlamak ve sonuçları Prometheus'a göndererek Grafana'da izlemek.

## Workflow

### Temel k6 Script
```javascript
// sentinel-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';

// Özel metrikler
const queryDuration = new Trend('sentinel_query_duration', true);  // ms
const queryErrors = new Counter('sentinel_query_errors');
const successRate = new Rate('sentinel_success_rate');

export const options = {
  scenarios: {
    constant_load: {
      executor: 'constant-vus',
      vus: 20,
      duration: '60s',
      tags: { scenario: 'baseline' },
    },
    ramp_up: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 50 },
        { duration: '60s', target: 50 },
        { duration: '30s', target: 0 },
      ],
      tags: { scenario: 'ramp' },
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    sentinel_success_rate: ['rate>0.99'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export function setup() {
  // Auth token al
  const res = http.post(`${BASE_URL}/api/v1/auth/token`, JSON.stringify({
    username: 'loadtest',
    password: 'loadtest123',
  }), { headers: { 'Content-Type': 'application/json' } });
  
  check(res, { 'login success': (r) => r.status === 200 });
  return { token: res.json('access_token') };
}

export default function(data) {
  const headers = {
    'Authorization': `Bearer ${data.token}`,
    'Content-Type': 'application/json',
  };
  
  // Metrik sorgusu
  const start = Date.now();
  const res = http.get(
    `${BASE_URL}/api/v1/metrics?query=up&time=now`,
    { headers, tags: { endpoint: 'metrics' } }
  );
  queryDuration.add(Date.now() - start);
  
  const ok = check(res, {
    'status 200': (r) => r.status === 200,
    'has data': (r) => r.json('status') === 'success',
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  successRate.add(ok);
  if (!ok) queryErrors.add(1);
  
  sleep(Math.random() * 1.5 + 0.5);
}
```

### Prometheus Remote Write
```javascript
// k6-prometheus.js (Prometheus'a metrik gönder)
import { check } from 'k6';
import http from 'k6/http';

export const options = {
  // k6 metrikleri Prometheus'a gönder
  ext: {
    loadimpact: {
      apm: [],
    },
  },
};
```

```bash
# Çalıştırma (Prometheus output)
K6_PROMETHEUS_RW_SERVER_URL=http://prometheus:9090/api/v1/write \
k6 run --out experimental-prometheus-rw sentinel-load-test.js \
  -e BASE_URL=http://sentinel-api:8000
```

### CI Pipeline
```yaml
# .github/workflows/load-test.yml
- name: Run k6 load test
  uses: grafana/k6-action@v0.3.1
  with:
    filename: tests/load/sentinel-load-test.js
    flags: --vus 10 --duration 30s
  env:
    BASE_URL: http://localhost:8000

- name: Check thresholds
  run: |
    # k6 non-zero exit code ile çıkar threshold'lar aşılırsa
    echo "k6 thresholds passed"
```

### HTML Rapor
```bash
k6 run sentinel-load-test.js \
  --out json=results.json \
  -e BASE_URL=http://localhost:8000

# JSON'dan özet
python3 -c "
import json
data = [json.loads(l) for l in open('results.json') if l.strip()]
durations = [d['data']['value'] for d in data if d.get('metric') == 'http_req_duration']
print(f'P95: {sorted(durations)[int(len(durations)*0.95)]:.0f}ms')
"
```

## Common mistakes
- `sleep(0)` veya sleep'siz VU döngüsü — sunucuyu spin loop'la bunaltırsın; `sleep(1)` minimum
- Threshold'ları sadece p95 ile sınırlamak — p99 ve hata oranı da tanımla
- `setup()` return değerini kullanmamak — token her VU'da ayrı alınır, gereksiz yük
- k6'yı test makinasında çalıştırmak — k6 CPU yoğun, ayrı node kullan veya k6 Cloud

## References
- `skills/test-load-locust`
- `skills/perf-p99-latency-tuning`
