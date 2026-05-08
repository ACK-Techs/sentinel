---
name: debug-oom-killer
description: "Linux OOM killer tarafından sonlandırılan Sentinel servis pod'larını tespit eder, kök nedeni bulur ve memory limit stratejisi üretir"
---

## Purpose
Sentinel target servisleri özellikle yük testi sırasında OOM killer kurbanı olabilir. Bu skill, hangi pod'un öldürüldüğünü, hangi process'in belleği tükettiğini ve yeni memory limit/request değerlerinin ne olması gerektiğini sistematik biçimde belirler.

## Workflow

### 1. OOM event'ini tespit et
```bash
# Kubernetes event'lerinden OOM'u bul
kubectl get events -n sentinel-target --sort-by='.lastTimestamp' | grep -i "OOMKilled\|oom"

# Pod restart sayısı yüksek olan pod'ları listele
kubectl get pods -n sentinel-target --sort-by='.status.containerStatuses[0].restartCount' | tail -10
```

### 2. Son container çıkış nedenini kontrol et
```bash
kubectl describe pod <pod-name> -n sentinel-target | grep -A5 "Last State"
# Beklenen çıktı:
#   Exit Code: 137  ← OOMKilled = 128 + 9 (SIGKILL)
#   Reason: OOMKilled
```

### 3. Node kernel log'unu oku
```bash
# OOM killer mesajını bul
kubectl debug node/<node-name> -it --image=busybox -- dmesg | grep -i "oom\|killed process" | tail -20
# veya journald üzerinden
kubectl exec -n kube-system ds/node-logger -- journalctl -k | grep "Out of memory"
```

### 4. Bellek tüketimini profille (pre-OOM)
```bash
# Prometheus'tan pod memory kullanım geçmişi
curl -s "http://prometheus.sentinel-cos.svc:9090/api/v1/query_range" \
  --data-urlencode 'query=container_memory_working_set_bytes{namespace="sentinel-target",pod=~"orders-.*"}' \
  --data-urlencode 'start=2024-01-15T09:00:00Z' \
  --data-urlencode 'end=2024-01-15T10:00:00Z' \
  --data-urlencode 'step=30s' | jq '.data.result[0].values[-10:]'
```

### 5. Memory leak analizi
```python
# FastAPI servisinde memory profiling (debug build)
import tracemalloc
tracemalloc.start()

@app.get("/admin/memory-snapshot")
def memory_snapshot():
    snapshot = tracemalloc.take_snapshot()
    top = snapshot.statistics("lineno")
    return [{"file": str(s.traceback), "size_kb": s.size / 1024} for s in top[:20]]
```

### 6. Yeni limit hesapla
```bash
# P99 bellek kullanımını al
P99=$(curl -s "http://prometheus.sentinel-cos.svc:9090/api/v1/query" \
  --data-urlencode 'query=quantile_over_time(0.99, container_memory_working_set_bytes{container="orders"}[24h])' \
  | jq -r '.data.result[0].value[1]')

# Limit = P99 * 1.3 (30% headroom)
echo "Recommended limit: $(echo "$P99 * 1.3 / 1048576" | bc)Mi"
```

### 7. Helm values güncelle
```yaml
# helm/sentinel-target/values.yaml
services:
  orders:
    resources:
      requests:
        memory: "256Mi"
      limits:
        memory: "512Mi"  # P99 * 1.3 değerini kullan
```

## Common mistakes
1. Memory `limit` artırmadan `request` artırmak — OOM olmaya devam eder, sadece scheduling değişir.
2. Python process'inde `del obj` yapıp belleğin hemen OS'e döneceğini varsaymak — `gc.collect()` + `ctypes.malloc_trim(0)` gerekebilir.
3. Redis/SQLAlchemy connection pool'unu kontrol etmemek — her connection ~1MB bellek tutar, havuz büyüklüğü OOM sebebi olabilir.
4. `target-app-load-generator` ile yük testini memory profiling olmadan yapmak — OOM sonrası trace yok, erken profil al.

## References
- `skills/target-app-load-generator`
- `skills/platform-finops-rightsizing`
- `skills/cos-resource-sizing`
