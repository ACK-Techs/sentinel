---
name: agentic-microk8s-ops-reference
description: COS işletim sorunlarında MicroK8s teşhis sırası, komutlar ve yetki geri dönüşlerini özetlerken kullan.
---

## Amaç

Bu skill, COS Lite altında çalışan MicroK8s kümesi için temel işletim teşhis sırasını standartlaştırır. Amaç, cluster sağlığı, addon durumu, pod durumu ve yetki sorunlarını tutarlı komutlarla kontrol edip operatöre güvenli geri dönüş yolu vermektir.

## Kapsam

- Dahil:
- `microk8s status`, `microk8s kubectl`, addon ve pod sağlığı odaklı ilk inceleme.
- `sudo` gereksinimi, `microk8s` grup üyeliği ve izin hatası geri dönüşü.
- Faz 1 MicroK8s kurulum skill'lerine yönlendirme.
- Hariç:
- Çok düğümlü HA tasarımı veya yeni ağ topolojisi önerisi.
- Faz 1 dışında farklı Kubernetes dağıtımı için özel talimat üretme.

## Adımlar

1. Önce şunu doğrula: kullanıcı gerçekten MicroK8s üzerinde mi çalışıyor, hangi node'da komut çalıştırıyor, yetkili kullanıcı mı.
2. Küme sağlık kontrolünü çalıştır:
   - `microk8s status`
   - `microk8s inspect`
3. Pod ve namespace durumunu kontrol et:
   - `microk8s kubectl get pods -A`
   - `microk8s kubectl get svc -A`
   - `microk8s kubectl get events -A --sort-by=.lastTimestamp`
4. Gerekli addon'ları doğrula:
   - `microk8s status --wait-ready`
   - DNS ve storage için Faz 1 adımlarını `../../skills/microk8s-addons-dns-storage/SKILL.md` ile karşılaştır.
5. Traefik veya dış erişim sorunu varsa LoadBalancer veya servis IP bilgisini doğrula:
   - `microk8s kubectl get svc -A`
   - `microk8s kubectl describe svc -n <namespace> <service>`
6. Yetki hatası alırsan önce geri dönüş uygula:
   - Kullanıcı `microk8s` grubunda mı doğrula.
   - Gerekirse aynı komutu `sudo` ile yeniden dene.
   - Grup üyeliği yeni verildiyse oturumu yenilemeden sonucu kesin kabul etme.

## Kontrol listesi

- [ ] `microk8s status` çıktısında cluster sağlıklı görünüyor mu?
- [ ] Gerekli addon'lar Faz 1 beklentisiyle uyumlu mu?
- [ ] COS pod'larında `CrashLoopBackOff`, `ImagePullBackOff` veya `Pending` var mı?
- [ ] Servis ve endpoint bilgileri beklenen namespace'te görünüyor mu?
- [ ] İzin hatasında `sudo` veya grup üyeliği doğrulaması yapıldı mı?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| `microk8s status` erişim reddi | Kullanıcı `microk8s` grubunda mı | Gerekirse `sudo` ile yeniden dene, sonra oturumu yenile |
| `microk8s kubectl` bağlanamıyor | Daemon ayakta mı, socket erişimi var mı | `microk8s inspect` al ve Faz 1 kurulum adımlarına dön |
| Pod `CrashLoopBackOff` | Son olaylar ve ilgili pod logları | Bileşen bazlı ilgili troubleshoot skill'e geç |
| Servis dışarı açılmıyor | LoadBalancer/IP ataması ve ingress | `../agentic-troubleshoot-traefik-ingress/SKILL.md` |
| Depolama veya disk sorunu | `hostpath-storage`, disk doluluğu | `../../skills/microk8s-addons-dns-storage/SKILL.md` ile karşılaştır |

## İlgili belgeler ve skill'ler

- `../../documantations/PROJECT_ROOT.md`
- `../documantations/PROJECT_ROOT_PHASE2.md`
- `../../skills/microk8s-install-base/SKILL.md`
- `../../skills/microk8s-addons-dns-storage/SKILL.md`
- `../../skills/juju-bootstrap-microk8s/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
- `../agentic-troubleshoot-prometheus/SKILL.md`
- `../agentic-troubleshoot-loki/SKILL.md`
