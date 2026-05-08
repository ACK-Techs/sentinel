---
name: microk8s-troubleshoot-api
description: "MicroK8s API server'a bağlanamama, `connection refused`, TLS sertifika hatası, port çakışması veya kube-apiserver pod'unun başlamaması durumlarını adım adım teşhis etmek gerektiğinde kullan."
---

## Purpose
API server erişim sorunları birbirinden farklı kök nedenlerden kaynaklanır: IP değişikliği, port çakışması, sertifika süresi dolması, disk dolu, containerd başlamamış. Teşhis sırası önemlidir.

## Teşhis akışı

### 1. Temel servis durumu
```bash
microk8s status
sudo systemctl status snap.microk8s.daemon-apiserver
sudo journalctl -u snap.microk8s.daemon-apiserver --since "5 minutes ago" | tail -50
```

### 2. Port ve process kontrolü
```bash
sudo ss -tlnp | grep 16443  # API server portu
sudo ss -tlnp | grep 2380   # dqlite portu
# Port kullanımda değilse daemon başlamamış demektir
```

### 3. Disk alanı
```bash
df -h /var/snap/microk8s/
# etcd/dqlite yazamıyorsa crash loop'a girer
```

### 4. TLS sertifika geçerliliği
```bash
openssl s_client -connect 127.0.0.1:16443 2>/dev/null | openssl x509 -noout -dates
# notAfter geçmişse sertifika yenileme gerekir
```

### 5. IP değişikliği şüphesi
```bash
hostname -I  # mevcut IP
cat ~/.kube/config | grep server  # kubeconfig'deki IP
# Farklılarsa microk8s-ip-change-recovery skill'ini uygula
```

### 6. Full inspect
```bash
sudo microk8s inspect 2>&1 | grep -E "FAIL|ERROR"
```

## Common mistakes
- `microk8s kubectl` yerine yanlış `kubectl` binary kullanıp "cluster unreachable" alıp API server'ı suçlamak.
- containerd çalışmadığında API server log'larına bakmak — sıra yanlış.

## References
- `skills/microk8s-inspect`
- `skills/microk8s-ip-change-recovery`
- `skills/microk8s-ha-cluster`
