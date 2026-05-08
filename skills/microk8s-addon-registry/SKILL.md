---
name: microk8s-addon-registry
description: "MicroK8s'in dahili container registry addon'unu etkinleştirmek, yerel image push/pull yapmak ve private image'ları Kubernetes pod'larında kullanmak gerektiğinde kullan. Harici registry bağlantısı yerine hızlı geliştirme döngüsü için tercih edilir."
---

## Purpose
Harici Docker Hub veya registry'ye bağımlı kalmadan yerel image'ları kümeye dağıtmak; air-gap geliştirme ortamları ve CI hızlandırma için.

## Kurulum ve yapılandırma
```bash
microk8s enable registry
# Varsayılan port: 32000, depolama: 20Gi hostpath
```

Depolama boyutu özelleştirme:
```bash
microk8s enable registry:size=40Gi
```

## Image push/pull
```bash
# Local image'ı etiketle ve push et
docker tag myapp:latest localhost:32000/myapp:latest
docker push localhost:32000/myapp:latest

# Pod manifest'inde kullan
image: localhost:32000/myapp:latest
```

## Registry'ye güvensiz erişim (Docker daemon)
```json
// /etc/docker/daemon.json
{
  "insecure-registries": ["localhost:32000"]
}
```
```bash
sudo systemctl restart docker
```

## containerd mirror yapılandırması (MicroK8s)
```bash
cat /var/snap/microk8s/current/args/certs.d/localhost:32000/hosts.toml
# [host."http://localhost:32000"]
#   capabilities = ["pull", "resolve"]
```

## Common mistakes
- Başka bir host'tan registry'ye erişmeye çalışmak — varsayılan yalnızca localhost:32000 dinler.
- `imagePullPolicy: Always` ile yerel registry'nin atlanmasına yol açmak.
- Depolama dolduğunda push hatasını araştırmak; `microk8s kubectl get pvc -n container-registry` ile kontrol et.

## References
- `skills/microk8s-addons-overview`
- `skills/microk8s-container-runtime`
- `skills/microk8s-offline-install`
