---
name: target-app-k8s-manifests
description: k8s/ Kustomize base — sentinel-target namespace; Deployment/Service/ConfigMap/NetworkPolicy; Postgres + Redis tek-replica.
---

## Purpose
Test platformunun tüm bileşenlerini `sentinel-target` namespace'i altında tekrar-edilebilir şekilde deploy etmek. **Prometheus ServiceMonitor yok**, sadece OTEL env'leri. NetworkPolicy ile `/admin/*` dış trafiğe kapalı.

## When to Use
- İlk kurulum (`kubectl apply -k k8s/base`).
- Yeni overlay (staging, chaos-heavy) oluştururken.
- Resource limit, replica sayısı veya OTEL endpoint değiştirirken.

## Contract / Interface
Klasör:
```
k8s/
  base/
    namespace.yaml
    kustomization.yaml
    gateway/{deployment,service,configmap}.yaml
    orders/...
    payments/...
    inventory/...
    worker/{deployment,configmap}.yaml
    postgres/{statefulset,service,secret}.yaml
    redis/{statefulset,service}.yaml
    networkpolicy-admin.yaml
    networkpolicy-default.yaml
  overlays/
    dev/       staging/
```
Namespace: `sentinel-target` (labels: `sentinel.io/role=target`).

Her servis Deployment:
- `replicas: 1` (Faz-1).
- Resources: `requests{cpu:50m, memory:64Mi}`, `limits{cpu:100m, memory:128Mi}`.
- ProbeSet: `livenessProbe: /health` (period 10s), `readinessProbe: /health` (period 5s).
- Env (zorunlu):
  - `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector.sentinel.svc.cluster.local:4317`
  - `OTEL_SERVICE_NAME=<name>`
  - `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=$(DEPLOYMENT_ENV),service.namespace=sentinel-target`
  - `DEPLOYMENT_ENV=dev`
- ConfigMap `<svc>-chaos` → `/etc/chaos/profile.yaml` mount.

Postgres: StatefulSet 1 replica, PVC 5Gi, secret `postgres-credentials`.
Redis: StatefulSet 1 replica, AOF off (test yeterli).

NetworkPolicy:
- `default-deny-ingress` (namespace-wide).
- `allow-intra-namespace` (pods in ns ↔ pods in ns).
- `allow-gateway-ingress` (yalnız gateway pod'una 8000).
- `deny-admin-external`: `/admin/*` pattern Policy L4 değil, uygulama-seviyesinde de enforce edilir; L4'te ise load & scenario-runner pod'larına `admin`-port açılmaz (ayrı port yaklaşımı tercih edilebilir).

## Implementation Notes
- **Prometheus ServiceMonitor, PodMonitor, ScrapeConfig hiçbir manifest'te yok.**
- OTEL collector bu repo'da **değil** — `sentinel` namespace'inde Sentinel tarafından yönetilir; sadece DNS adı referans edilir.
- Gateway Service `type: ClusterIP`; dış erişim için `Ingress` (ayrı overlay) veya `port-forward`.
- ConfigMap değişimi pod restart'a yol açmaz; chaos reload endpoint'i kullanılır (`target-app-chaos-api` skill).
- PodSecurity: `restricted` profile; `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`.

## Anti-patterns
1. `prometheus.io/scrape: "true"` annotation koymak — Faz-1'de anlamsız, yanıltıcı.
2. Resource limit koymamak — chaos `cpu_burn` node'u yiyebilir.
3. `OTEL_EXPORTER_OTLP_ENDPOINT`'i her pod'da hardcode etmek — ConfigMap + envFrom ile paylaşılmalı.
4. Postgres secret'ı manifest'e düz yazmak — Sealed Secrets veya en azından ayrı `.gitignore`'lu overlay kullan.
5. NetworkPolicy yok sayıp "k8s default allow" üzerinden gitmek — `/admin` dış dünyaya açık kalır.

## Example Snippet
```yaml
# k8s/base/orders/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: orders, namespace: sentinel-target}
spec:
  replicas: 1
  selector: {matchLabels: {app: orders}}
  template:
    metadata: {labels: {app: orders}}
    spec:
      securityContext: {runAsNonRoot: true, runAsUser: 10001}
      containers:
      - name: orders
        image: ghcr.io/sentinel/orders:0.3.1
        ports: [{containerPort: 8000}]
        envFrom:
        - configMapRef: {name: otel-shared-env}
        env:
        - {name: OTEL_SERVICE_NAME, value: orders}
        - {name: DB_URL, valueFrom: {secretKeyRef: {name: postgres-credentials, key: url}}}
        resources:
          requests: {cpu: 50m, memory: 64Mi}
          limits:   {cpu: 100m, memory: 128Mi}
        livenessProbe:  {httpGet: {path: /health, port: 8000}, periodSeconds: 10}
        readinessProbe: {httpGet: {path: /health, port: 8000}, periodSeconds: 5}
        volumeMounts:
        - {name: chaos, mountPath: /etc/chaos}
      volumes:
      - name: chaos
        configMap: {name: orders-chaos}
```
