---
name: agentic-microk8s-ops-reference
description: COS teşhisi için MicroK8s komut sırası ve addon/küme sağlığı şablonlarını verirken kullan.
---

## Amaç

Teşhis sırası önerisi: **`microk8s status`** (veya eşdeğeri) → **`kubectl get pods -A`** (MicroK8s kubeconfig ile) → **gerekli addon’lar**: `dns`, `hostpath-storage`, `metallb` (Faz 1 `PROJECT_ROOT.md` ile uyumlu). **Grup üyeliği**: kullanıcı `microk8s` grubuna ekli değilse `sudo` gerekebilir — Faz 1 `microk8s-*` skill’lerindeki uyarılar geçerlidir.

## Kapsam

### Dahil

- Düğüm hazırlığı ve kaynak kontrolü (yüksek seviye).
- Addon kapalıysa etkinleştirme yönergelerine Faz 1 skill ile yönlendirme.

### Hariç

- HA çok düğüm MicroK8s (ayrı rehber).

## Kurallar

- `kubectl` komutları doğru kubeconfig ile; genelde `microk8s kubectl ...` veya `~/.kube/config` (dokümana göre).
- Faz 1 skill’lerdeki komutlarla çelişen kısayol önerme.
- Çıktıları kullanıcıya özetle; tam log gerekiyorsa dosyaya yönlendir.

## Kontrol listesi

- [ ] Pod `CrashLoopBackOff` var mı?
- [ ] MetalLB ataması Traefik için uygun mu (`../../skills/cos-ingress-config`)?
- [ ] Disk/hostPath doldu mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| API unreachable | microk8s çalışıyor mu | `microk8s status` |
| ImagePullBackOff | Registry | Ağ / proxy |

## İlgili belgeler ve skill'ler

- `../../documantations/PROJECT_ROOT.md`
- `../../skills/microk8s-addons-dns-storage/SKILL.md`
- `../../skills/microk8s-install-base/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
- `https://documentation.ubuntu.com/observability/`
