---
name: k8s-scale-load-testing
description: "Kubernetes üzerinde yük testi çalıştırmak (Locust, k6), HPA'nın gerçek trafiğe yanıt verdiğini doğrulamak ya da 'HPA neden tetiklenmiyor?' sorusunu araştırmak gerektiğinde kullan."
---

## Purpose
Yük testinin çıktısı iki şeyi kanıtlamalıdır: (1) pod sayısı artan yükle birlikte ölçeklendi, (2) hedef latency/error SLO bozulmadı. Yalnızca "yük gönderdim" yetmez.

## Workflow

### Araç seçimi
- **k6** — JavaScript DSL, threshold/check ile pass/fail kapısı; CI dostu.
- **Locust** — Python, karmaşık senaryolar ve interaktif izleme için.
- İkisi de Kubernetes Job veya Deployment olarak çalıştırılabilir; dışarıdan bağlantı istemiyorsan aynı cluster'da çalıştır.

### Hazırlık
1. HPA ve Metrics Server'ın hazır olduğunu doğrula: `kubectl get hpa -A`.
2. Hedef pod'un `resources.requests` değerlerinin gerçekçi olduğundan emin ol — aksi hâlde utilization hesabı yanıltıcı çıkar.
3. Prometheus scrape aralığını ve HPA `--horizontal-pod-autoscaler-sync-period` değerini (varsayılan 15s) göz önünde bulundur; ani spike'lara tepki gecikmesi olur.

### k6 örüntüsü
```js
export const options = {
  stages: [
    { duration: '1m', target: 50 },
    { duration: '3m', target: 200 },
    { duration: '1m', target: 0 },
  ],
  thresholds: { http_req_duration: ['p95<500'] },
};
```
Cluster içinde çalıştırmak için: `kubectl run k6 --image=grafana/k6 --restart=Never -- run -`.

### Doğrulama
```bash
watch kubectl get hpa <ad> -n <namespace>
kubectl top pods -n <namespace>
```
Grafana'da aynı zaman diliminde latency + replica sayısını yan yana göster.

## Common mistakes
- Yük testini dış ağdan çalıştırıp ingress/LB gecikmesini işlemci yükü sanmak.
- minReplicas'ı 1 bırakıp scale-down gecikmesini ("HPA çalışmıyor") yanlış teşhis etmek.
- Target utilization değerini %100 koymak — ani spike'ta yetersiz kalır.

## References
- `skills/k8s-scale-hpa`
- `skills/k8s-scale-custom-metrics-api`
- `skills/test-load-k6`
- `skills/test-load-locust`
