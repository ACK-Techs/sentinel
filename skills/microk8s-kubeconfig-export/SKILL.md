---
name: microk8s-kubeconfig-export
description: "MicroK8s kubeconfig'ini dışa aktarmak, uzak makineden erişim için yapılandırmak, mevcut ~/.kube/config ile merge etmek ve kubectl context'leri yönetmek gerektiğinde kullan."
---

## Purpose
MicroK8s varsayılan olarak yalnızca `microk8s kubectl` ile erişim sunar. Standart `kubectl`, Helm veya Juju gibi araçların cluster'a bağlanabilmesi için kubeconfig ihraç edilmesi gerekir.

## Yerel kullanım
```bash
microk8s config > ~/.kube/config
# veya mevcut config ile merge:
microk8s config > /tmp/microk8s.yaml
KUBECONFIG=~/.kube/config:/tmp/microk8s.yaml kubectl config view --flatten > /tmp/merged.yaml
mv /tmp/merged.yaml ~/.kube/config
```

## Uzak erişim
```bash
# MicroK8s node'un IP'sini ekleyerek ihraç et
microk8s config | sed "s/127.0.0.1/<node-external-ip>/g" > remote-kubeconfig.yaml
```
Node'un 16443/tcp portunu dışarıya açmayı unutma.

## Context yönetimi
```bash
kubectl config get-contexts
kubectl config use-context microk8s
kubectl config rename-context microk8s my-dev-cluster
```

## Juju entegrasyonu
```bash
# Juju'nun MicroK8s'i cloud olarak tanıması için:
microk8s config | juju add-k8s microk8s --client
# veya
KUBECONFIG=~/.kube/config juju add-k8s microk8s
```

## Common mistakes
- `127.0.0.1` referansını değiştirmeden uzak makineye kubeconfig kopyalamak — bağlantı başarısız olur.
- `--flatten` yapmadan merge etmek; config dosyası bozulabilir.
- MicroK8s API sunucusu sertifikasının yeni IP'yi SANs olarak içermediği durumda TLS hatası almak.

## References
- `skills/microk8s-install-snap`
- `skills/microk8s-ip-change-recovery`
- `skills/juju-bootstrap-cloud`
