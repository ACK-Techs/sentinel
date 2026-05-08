---
name: cos-relation-tempo-grafana
description: "Tempo charm'ını Grafana'ya datasource olarak bağlamak, trace görselleştirmesini etkinleştirmek ve Grafana Explore'da TraceQL sorgusu yapılabilir hale getirmek gerektiğinde kullan."
---

## Purpose
Tempo→Grafana relation, Juju aracılığıyla Grafana'ya otomatik Tempo datasource ekler. Manuel datasource yapılandırmasına gerek kalmaz.

## Relation kurulumu
```bash
juju switch cos
juju integrate tempo-k8s:grafana-source grafana-k8s:grafana-source
```

## Doğrulama
```bash
juju status tempo-k8s grafana-k8s
# Relation kurulduktan sonra Grafana pod'u yeniden başlayabilir (datasource reload)
```

Grafana UI'dan doğrulama:
1. Grafana → Configuration → Data Sources → Tempo görünmeli
2. Explore → Tempo datasource → TraceQL sorgusu çalıştır: `{}`

## Log-trace korelasyonu
Loki ve Tempo arasındaki derived field kurulumu Juju charm'ları tarafından otomatik yapılır — her iki relation da aktifse Grafana log satırından trace'e geçiş linki çıkar.

```bash
# Gerekli relation'lar:
juju integrate loki-k8s:grafana-source grafana-k8s:grafana-source
juju integrate tempo-k8s:grafana-source grafana-k8s:grafana-source
```

## Service graph
Tempo service graph metriklerinin Grafana'da görünmesi için:
```bash
juju integrate tempo-k8s:metrics-endpoint prometheus-k8s:metrics-endpoint
```
Prometheus artık `tempo_service_graph_request_total` metriklerini toplar; Grafana service graph paneli bu metrikleri kullanır.

## Common mistakes
- Tempo datasource eklendikten sonra Grafana'nın yeniden yüklenmesi beklenmeden sorgu denemek.
- Service graph panelini açmadan önce Prometheus→Grafana relation olmadığında metriklerin gelmediğini fark etmemek.

## References
- `skills/cos-deploy-tempo`
- `skills/cos-bundle-overview`
- `skills/obs-tempo-grafana-datasource`
