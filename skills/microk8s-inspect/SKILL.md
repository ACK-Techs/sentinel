---
name: microk8s-inspect
description: "MicroK8s sorunlarını araştırmak için resmi hata raporu ve destek paketi oluşturmak, `microk8s inspect` çıktısını yorumlamak ve teşhis adımlarını uygulamak gerektiğinde kullan."
---

## Purpose
`microk8s inspect` komutu servis durumlarını, log'ları, ağ yapılandırmasını ve bilinen sorunları tek bir arşivde toplar. Canonical destek talebi ve kendi kendine teşhis için birincil araçtır.

## Temel kullanım
```bash
sudo microk8s inspect
# /var/snap/microk8s/common/ altında tarball oluşturur
# ve terminalde FAIL/WARN özetini gösterir
```

Çıktı bölümleri:
- **Service status**: kube-apiserver, kubelet, containerd durumları
- **Network**: CNI, iptables kuralları
- **Addons**: hangi addon'ların aktif olduğu
- **Known issues**: bilinen yapılandırma problemleri

## Sonuç yorumlama
```bash
# inspect tarball'ı aç ve logları incele
tar xf /var/snap/microk8s/common/inspection-report-*.tar.gz
grep -r "FAIL\|ERROR\|WARN" inspection-report-*/
```

## Özel tanılama komutları
```bash
microk8s kubectl get events --sort-by='.lastTimestamp' -A | tail -30
microk8s kubectl describe node $(hostname)
sudo journalctl -u snap.microk8s.daemon-apiserver --since "10 minutes ago"
sudo journalctl -u snap.microk8s.daemon-containerd --since "10 minutes ago"
```

## Common mistakes
- `sudo` olmadan çalıştırmak — bazı log dosyaları root gerektirir.
- Inspect yerine doğrudan Canonical destek forumuna gitmek; inspect raporu olmadan yardım almak zorlaşır.

## References
- `skills/microk8s-troubleshoot-api`
- `skills/microk8s-ip-change-recovery`
- `skills/microk8s-ha-cluster`
