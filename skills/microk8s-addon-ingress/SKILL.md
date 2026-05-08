---
name: microk8s-addon-ingress
description: "MicroK8s'in yerleşik nginx Ingress Controller'ını etkinleştirmek, IngressClass yapılandırmasını anlamak ve COS/uygulama servislerini HTTP/HTTPS üzerinden dışarı açmak gerektiğinde kullan."
---

## Purpose
MicroK8s `ingress` addon'u nginx tabanlı bir Ingress Controller kurar. Traefik'e geçmeden önce veya basit routing için yeterlidir; COS kendi Traefik charm'ını kullanır, bu addon onun yerini tutmaz.

## Kurulum
```bash
microk8s enable ingress
# nginx-ingress-microk8s DaemonSet olarak kube-system namespace'ine kurulur
```

## Temel Ingress kaynağı
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: public   # MicroK8s'in IngressClass adı
  rules:
    - host: myapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-svc
                port:
                  number: 8080
```

## TLS termination
```yaml
spec:
  tls:
    - hosts: [myapp.local]
      secretName: myapp-tls
```
Sertifika: `cert-manager` addon veya self-signed Secret.

## Doğrulama
```bash
microk8s kubectl get ingress -A
microk8s kubectl get pods -n ingress -o wide
curl -H "Host: myapp.local" http://<node-ip>
```

## Common mistakes
- `ingressClassName` belirtmemek — MicroK8s'te varsayılan class adı `public`'tir, belirtilmezse kural uygulanmaz.
- DNS veya `/etc/hosts` olmadan `curl` denemesi yapıp "404" alıp controller hatası sanmak.
- `ingress` addon ile Juju Traefik charm'ını aynı anda aktif tutmak; port 80/443 çakışması olur.

## References
- `skills/microk8s-addons-overview`
- `skills/k8s-net-ingress-controller`
- `skills/cos-ingress-troubleshoot`
