---
name: cos-ingress-troubleshoot
description: "COS bileşenlerine Traefik ingress üzerinden erişilemiyor, URL 404/502 döndürüyor veya MetalLB IP atanmadığı için external adres yok durumlarında teşhis ve çözüm adımlarını uygulamak gerektiğinde kullan."
---

## Purpose
COS ingress sorunları üç katmanda olur: MetalLB IP ataması, Traefik yönlendirmesi ve DNS/hosts çözümlemesi. Sırayı takip etmek gereksiz debug süresini engeller.

## Teşhis akışı

### 1. Traefik durumu
```bash
juju status traefik-k8s
# "active/idle" olmalı
microk8s kubectl get svc -n cos | grep traefik
# EXTERNAL-IP dolu mu?
```

### 2. MetalLB IP ataması
```bash
microk8s kubectl get svc traefik-k8s -n cos
# EXTERNAL-IP <pending> ise MetalLB sorunu
microk8s kubectl get pods -n metallb-system
microk8s kubectl describe ipaddresspool -n metallb-system
```

MetalLB pool boşaldıysa yeni aralık ekle:
```bash
# microk8s disable metallb; microk8s enable metallb:10.64.140.43-10.64.140.60
```

### 3. Traefik ingress route listesi
```bash
microk8s kubectl get ingressroutes -n cos 2>/dev/null
juju run traefik-k8s/0 show-proxied-endpoints --format=json
```

### 4. Servis bağlantısı
```bash
# Traefik pod'undan hedef servise erişim:
microk8s kubectl exec -n cos deploy/traefik-k8s -- wget -qO- http://grafana-k8s:3000/api/health
```

### 5. DNS / hosts
```bash
# /etc/hosts ekle veya DNS kaydı kontrol et:
grep grafana /etc/hosts
curl -H "Host: cos-grafana.example.com" http://<traefik-ip>
```

## Common mistakes
- MetalLB `<pending>` durumunu DNS sorunu sanmak.
- Traefik relation olmayan bir servisin ingress URL'sini beklemeye çalışmak.
- COS namespace'ini yanlış belirtmek — Juju model adıyla namespace örtüşür.

## References
- `skills/cos-bundle-overview`
- `skills/microk8s-addon-metallb`
- `skills/k8s-net-traefik-middleware`
