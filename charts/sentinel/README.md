# Sentinel Helm Chart

Installs Prometheus, Loki, Grafana, Tempo, and `sentinel-gateway` into an existing Kubernetes cluster.

## Quick Start

```bash
helm dependency update ./charts/sentinel
helm upgrade --install sentinel ./charts/sentinel \
  --create-namespace -n sentinel \
  --set gateway.token=<token>
```

The default Grafana admin password is `admin` for local/lab use only. Override it for any shared cluster:

```bash
helm upgrade --install sentinel ./charts/sentinel \
  --create-namespace -n sentinel \
  --set gateway.token=<token> \
  --set kube-prometheus-stack.grafana.adminPassword=<password>
```

## Values Examples

Use an existing Secret for the gateway token:

```bash
kubectl create secret generic sentinel-gateway-secret \
  -n sentinel \
  --from-literal=token=<token>

helm upgrade --install sentinel ./charts/sentinel \
  --create-namespace -n sentinel \
  --set gateway.existingSecret=sentinel-gateway-secret
```

Use a specific gateway image tag:

```bash
helm upgrade --install sentinel ./charts/sentinel \
  --create-namespace -n sentinel \
  --set gateway.token=<token> \
  --set gateway.image.tag=0.1.0
```

Disable a dependency:

```bash
helm upgrade --install sentinel ./charts/sentinel \
  --create-namespace -n sentinel \
  --set gateway.token=<token> \
  --set loki.enabled=false
```

## Discovery Compatibility

Sentinel CLI `sentinel install --mode k8s` runs this chart and then discovers service endpoints automatically.
The chart keeps service names aligned with `discovery.py` expectations:

- Prometheus: `sentinel-kube-prometheus-stack-prometheus:9090`
- Loki: `sentinel-loki:3100`
- Tempo: `sentinel-tempo:3200`
- Gateway: `sentinel-gateway:8091`

For local access:

```bash
kubectl port-forward -n sentinel svc/sentinel-kube-prometheus-stack-grafana 3000:80
kubectl port-forward -n sentinel svc/sentinel-gateway 8091:8091
```
