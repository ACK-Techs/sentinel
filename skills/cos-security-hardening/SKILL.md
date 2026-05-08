---
name: cos-security-hardening
description: "COS stack'ine TLS şifreleme, kimlik doğrulama ve NetworkPolicy izolasyonu ekleyerek üretim güvenlik gereksinimlerini karşılamak ya da güvenlik denetim bulgularına yanıt vermek gerektiğinde kullan."
---

## Purpose
Varsayılan COS kurulumu açık HTTP erişimi ve sınırlı kimlik doğrulama ile gelir. Üretim ortamı için her bileşende en az TLS + basic auth gereklidir.

## TLS

### cert-manager ile otomatik sertifika
```bash
microk8s enable cert-manager
# ClusterIssuer oluştur:
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned
spec:
  selfSigned: {}
EOF
```

Traefik için TLS entegrasyonu:
```bash
juju config traefik-k8s tls-secret-name=cos-tls
```

## Grafana kimlik doğrulama
```bash
# Admin şifresini güçlü yap:
juju run grafana-k8s/0 get-admin-password  # mevcut şifreyi öğren
juju config grafana-k8s admin-password=<güçlü-şifre>
# OIDC/OAuth (destekleniyorsa):
juju config grafana-k8s auth-providers=github
```

## Prometheus Basic Auth (scrape)
Prometheus HTTP API'ye erişimi kısıtlamak için Traefik middleware:
```yaml
apiVersion: traefik.containo.us/v1alpha1
kind: Middleware
metadata:
  name: auth
  namespace: cos
spec:
  basicAuth:
    secret: prometheus-auth-secret
```

## NetworkPolicy ile izolasyon
```bash
# Yalnızca cos namespace içi iletişim + uygulama modelinden gelen scrape:
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cos-default-deny
  namespace: cos
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
EOF
```

## Common mistakes
- TLS ekledikten sonra charm'ların birbirine HTTP ile bağlandığını kontrol etmemek — mixed-mode hata.
- Prometheus scrape'lerinde `insecure_skip_verify: true` bırakmak.

## References
- `skills/cos-bundle-overview`
- `skills/k8s-sec-tls-cert-manager`
- `skills/k8s-net-networkpolicy`
- `skills/obs-grafana-rbac`
