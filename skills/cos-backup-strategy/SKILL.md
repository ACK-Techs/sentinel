---
name: cos-backup-strategy
description: "COS bileşenlerindeki kalıcı veriyi (Prometheus TSDB, Loki chunk'ları, Grafana dashboard'ları) düzenli yedeklemek ve geri yükleme prosedürünü bilmek gerektiğinde kullan."
---

## Purpose
COS bileşen verileri PVC'lerde saklanır. Juju model yedeklemesi (juju-controller-backup) Kubernetes veri içeriğini kapsamaz; ayrıca backup stratejisi gerekir.

## Prometheus TSDB yedekleme
```bash
# Anlık snapshot:
curl -X POST http://<prom-url>/api/v1/admin/tsdb/snapshot
# Çıktı: {"status":"success","data":{"name":"20241215T120000Z-...}}
# Snapshot dizini: /prometheus/snapshots/<isim>

# PVC üzerinden kopyalama:
microk8s kubectl exec -n cos prometheus-k8s-0 -- \
  tar czf - /prometheus/snapshots/<isim> | \
  ssh backup@storage 'cat > /backup/prometheus-$(date +%Y%m%d).tar.gz'
```

## Loki chunk yedekleme
```bash
# Object storage backend kullanılıyorsa cloud tarafında yönetilir
# filesystem backend (hostpath):
microk8s kubectl exec -n cos loki-k8s-0 -- \
  tar czf - /loki/chunks | \
  ssh backup@storage 'cat > /backup/loki-$(date +%Y%m%d).tar.gz'
```

## Grafana dashboard yedekleme
```bash
# Dashboard export API:
curl -u admin:<password> http://<grafana-url>/api/dashboards/home | jq .
# Tüm dashboard'ları döngüyle yedekle:
for uid in $(curl -u admin:<pw> http://<grafana>/api/search | jq -r '.[].uid'); do
  curl -u admin:<pw> http://<grafana>/api/dashboards/uid/$uid > dashboard-$uid.json
done
```

## Velero ile PVC yedekleme
```bash
velero backup create cos-backup --include-namespaces=cos
velero restore create --from-backup cos-backup
```

## Common mistakes
- Yalnızca Juju controller yedekleyip Prometheus/Loki verisini atlamak.
- Prometheus admin API `/tsdb/snapshot` için `--web.enable-admin-api` flag'inin açık olduğunu kontrol etmemek.

## References
- `skills/cos-bundle-overview`
- `skills/juju-controller-backup`
- `skills/k8s-storage-backup-velero`
