---
name: docs-diagram-as-code
description: "Mermaid ve PlantUML ile Sentinel altyapı ve servis diyagramlarını kod olarak oluşturur; versiyon kontrolüne uygun format"
---

## Purpose
PNG/Visio diyagramları zamanla stale kalır ve diff'lenemez. Bu skill, Sentinel'in COS altyapısını, servis topolojisini ve deployment akışlarını Mermaid veya PlantUML sözdizimi ile kodda yönetilecek şekilde tanımlar. GitHub ve MkDocs otomatik render eder.

## Workflow

### 1. Sentinel servis topolojisi (Mermaid)
```mermaid
graph TB
    subgraph "sentinel-target namespace"
        GW[gateway :8080]
        ORD[orders :8001]
        PAY[payments :8002]
        INV[inventory :8003]
        WRK[worker :8004]
    end

    subgraph "sentinel-cos namespace"
        PROM[Prometheus]
        GRAF[Grafana]
        LOKI[Loki]
        TEMPO[Tempo]
        OTEL[OTel Collector]
    end

    GW --> ORD
    ORD --> PAY
    ORD --> INV
    INV --> WRK

    GW -.->|metrics/traces/logs| OTEL
    ORD -.-> OTEL
    PAY -.-> OTEL
    INV -.-> OTEL
    OTEL --> PROM
    OTEL --> LOKI
    OTEL --> TEMPO
    PROM --> GRAF
    LOKI --> GRAF
    TEMPO --> GRAF
```

### 2. Juju relation diyagramı
```mermaid
graph LR
    PROM_CHARM[prometheus-k8s charm] -->|metrics-endpoint| APP_CHARM[target-app charm]
    LOKI_CHARM[loki-k8s charm] -->|logging| APP_CHARM
    TEMPO_CHARM[tempo-k8s charm] -->|tracing| APP_CHARM
    PROM_CHARM -->|grafana-source| GRAF_CHARM[grafana-k8s charm]
    LOKI_CHARM -->|grafana-source| GRAF_CHARM
    TEMPO_CHARM -->|grafana-source| GRAF_CHARM
```

### 3. CI/CD pipeline sequence diyagramı
```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant CI as GitHub Actions
    participant REG as Registry
    participant K8S as MicroK8s

    Dev->>GH: git push (conventional commit)
    GH->>CI: trigger workflow
    CI->>CI: lint + test + security scan
    CI->>REG: docker build & push
    CI->>K8S: helm upgrade sentinel-target
    K8S-->>CI: rollout status
    CI-->>Dev: status notification
```

### 4. Deployment state machine (PlantUML)
```plantuml
@startuml
[*] --> Pending : pod scheduled
Pending --> Init : init containers
Init --> Running : all containers ready
Running --> Error : crash / OOM
Error --> Running : restart (backoff)
Running --> Terminating : scale down / upgrade
Terminating --> [*]

Running : health probe passing
Error : restartCount++
@enduml
```

### 5. MkDocs entegrasyonu
```yaml
# mkdocs.yml
plugins:
  - mermaid2:
      version: 10.6.1
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
```

### 6. C4 modeli ile mimari katmanları
```mermaid
C4Context
    Person(user, "Son Kullanıcı", "HTTP istek yapan")
    System(sentinel_target, "Sentinel Target", "Gözlemlenebilir demo servisleri")
    System_Ext(cos, "Canonical Observability Stack", "Prometheus, Loki, Tempo, Grafana")
    System_Ext(ci, "GitHub Actions", "CI/CD pipeline")

    Rel(user, sentinel_target, "HTTP/REST")
    Rel(sentinel_target, cos, "OTLP push")
    Rel(ci, sentinel_target, "helm deploy")
```

## Common mistakes
1. Mermaid node isimlerinde özel karakter kullanmak — `[orders-service]` yerine `[orders]` kullan, tire sorun çıkarır.
2. Çok fazla detay tek diyagrama sıkıştırmak — C4 katmanlarını kullan, her katman ayrı diyagram.
3. Diyagramları `docs/images/` altına PNG olarak commit etmek — kaynak `.md` dosyasında Mermaid bloğu olarak sakla.
4. PlantUML için lokal server gerektiren setup kurmak — `plantuml.com` public server veya GitHub Action ile render.

## References
- `skills/docs-adr-workflow`
- `skills/target-app-service-topology`
- `skills/cos-bundle-overview`
