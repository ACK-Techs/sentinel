---
name: test-chaos-basic
description: "Chaos Engineering temel kavramları; steady-state hipotez tanımı, Sentinel için failure injection senaryoları ve Kubernetes'te chaos test araçları (Chaos Mesh, Litmus)"
---

## Purpose
Sentinel sisteminin belirli arıza koşullarında (ağ gecikmesi, pod crash, kaynak kıtlığı) nasıl davrandığını kontrollü ortamda test etmek ve kurtarma kapasitesini ölçmek.

## Workflow

### Steady-State Hipotez Tanımı
```python
# chaos/hypothesis.py
from dataclasses import dataclass
from typing import Callable

@dataclass
class SteadyStateHypothesis:
    """Sistem normal koşullarda bu kriterleri karşılar"""
    name: str
    probes: list[Callable[[], bool]]
    
    def verify(self) -> tuple[bool, list[str]]:
        failures = []
        for probe in self.probes:
            try:
                if not probe():
                    failures.append(f"{probe.__name__} başarısız")
            except Exception as e:
                failures.append(f"{probe.__name__} exception: {e}")
        return len(failures) == 0, failures

# Sentinel steady-state kriterleri
import httpx

def prometheus_healthy() -> bool:
    r = httpx.get("http://prometheus:9090/-/healthy", timeout=5)
    return r.status_code == 200

def sentinel_api_responsive() -> bool:
    r = httpx.get("http://sentinel-api:8000/health", timeout=3)
    return r.status_code == 200 and r.json()["status"] == "healthy"

def alert_evaluation_lag_acceptable() -> bool:
    # Prometheus alert evaluation gecikmesi < 30s
    r = httpx.get(
        "http://prometheus:9090/api/v1/query",
        params={"query": "prometheus_rule_evaluation_duration_seconds > 30"},
        timeout=5
    )
    data = r.json()
    return len(data["data"]["result"]) == 0

SENTINEL_HYPOTHESIS = SteadyStateHypothesis(
    name="Sentinel normal operasyon",
    probes=[prometheus_healthy, sentinel_api_responsive, alert_evaluation_lag_acceptable]
)
```

### Chaos Mesh ile Pod Kill
```yaml
# chaos/pod-kill.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: sentinel-api-pod-kill
  namespace: sentinel
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces: [sentinel]
    labelSelectors:
      app: sentinel-api
  duration: "30s"
  scheduler:
    cron: "@every 10m"
```

### Ağ Gecikme Enjeksiyonu
```yaml
# chaos/network-delay.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: prometheus-latency
  namespace: sentinel
spec:
  action: delay
  mode: all
  selector:
    namespaces: [sentinel]
    labelSelectors:
      app: prometheus
  delay:
    latency: "500ms"
    correlation: "25"
    jitter: "100ms"
  direction: to
  duration: "60s"
```

### Chaos Test Çalıştırma Döngüsü
```python
# chaos/run_experiment.py
import time
import subprocess
import httpx

def run_chaos_experiment(hypothesis: SteadyStateHypothesis, chaos_manifest: str):
    print("=== BAŞLANGIÇ steady-state kontrolü ===")
    ok, failures = hypothesis.verify()
    if not ok:
        raise RuntimeError(f"Sistem zaten sağlıksız: {failures}")
    print("Sistem sağlıklı, chaos başlıyor...")
    
    # Chaos enjekte et
    subprocess.run(["kubectl", "apply", "-f", chaos_manifest], check=True)
    
    # Chaos sırasında izle
    monitoring_results = []
    for i in range(12):  # 60 saniye, 5s aralık
        time.sleep(5)
        ok, failures = hypothesis.verify()
        monitoring_results.append((time.time(), ok, failures))
        print(f"  t+{(i+1)*5}s: {'OK' if ok else 'BOZUK'}")
    
    # Chaos kaldır
    subprocess.run(["kubectl", "delete", "-f", chaos_manifest], check=True)
    
    # Kurtarma süresi
    time.sleep(10)
    ok, failures = hypothesis.verify()
    if not ok:
        print(f"UYARI: Sistem chaos sonrası kurtaramadı: {failures}")
    else:
        print("Sistem başarıyla kurtardı")
    
    return monitoring_results
```

### Basit Chaos Testi (Chaos Mesh olmadan)
```bash
# Manuel pod kill testi
kubectl delete pod -l app=sentinel-api -n sentinel
# Hemen health check başlat
for i in $(seq 1 12); do
  sleep 5
  curl -s http://sentinel-api:8000/health | jq .status
done
```

## Common mistakes
- Steady-state doğrulaması yapmadan chaos başlatmak — zaten bozuk sistemi test etmek anlamsız
- Production'da chaos çalıştırmak — izole staging ortamı zorunlu
- Chaos sonrası teardown yapmamak — ağ kuralları veya pod kısıtlamaları kalıcı bozulma bırakabilir
- Tek bir pod kill senaryosunu "chaos engineering" saymak — ağ, disk, CPU, bellek kısıtlamalarını da kapsayan geniş senaryo seti gerek

## References
- `skills/test-integration-real-backend`
- `skills/perf-load-shedding`
