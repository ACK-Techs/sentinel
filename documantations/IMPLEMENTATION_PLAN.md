# Yapay Zeka Otonomi ve Hata Yönetim Protokolü

Aşağıdaki kurallar, bu planı izleyen **kodlayıcı yapay zekâ** (ör. Codex) için **genel prensip** olarak bağlayıcıdır; faz tabloları ve hata sütunları bu protokolle birlikte okunmalıdır.

1. **Sıfır Varsayım Kuralı:** Kodlayıcı AI, eksik bir bilgi veya birden fazla seçenek içeren belirsiz bir durumla karşılaşırsa **kendi kendine karar vermez**. İşlemi **derhal durdurur**, onay ve yönlendirme için **kullanıcıya danışır**.

2. **Maksimum 2 Deneme (Fail-Safe):** Bir komut hata verirse, AI bu hatayı gidermek için **en fazla bir veya iki** düzeltme denemesi yapabilir; sonrasında aşağıdaki madde devreye girer.

3. **Derin Analiz ve Bekleme (Stop & Think):** İki denemenin ardından hata sürüyorsa AI **yeni kod veya komut denemez**. Hatayı **derinlemesine analiz eder**, olası **kök nedenleri** açıklar ve **yeni bir adım atmadan önce** kullanıcının müdahalesini veya onayını **kesinlikle bekler**.

---

# COS Lite Kurulumu — Adım Adım Uygulama Planı

Bu plan, `skills/*/SKILL.md` ve `documantations/` altındaki mimari özetle uyumludur. Varsayılan yol: **MicroK8s** + **Juju 3.x** + **`juju deploy cos-lite --trust`** (tek bundle; ayrı charm deploy’u gelişmiş senaryodur).

---

## Faz 1 — Hazırlık

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| 1.1 | Host kaynaklarını doğrula (POC: ≥4 vCPU, ≥8 GiB RAM, ≥40 GiB disk). | `documantations/PROJECT_ROOT.md` | `nproc` ≥ 4; `free -h` yeterli boş RAM; `df -h /` yeterli disk. | Kaynak yetersizse VM’yi büyüt veya kurulumu durdur; bu fazdan devam etme. |
| 1.2 | `snapd` ve kullanıcı/grup: MicroK8s için `microk8s` grubu. | `skills/microk8s-install-base` | `snap version`; gerekirse `groups` içinde `microk8s` (yoksa `sudo usermod -aG microk8s $USER` + oturum yenileme). | `permission denied` → oturumu kapat/aç veya `newgrp microk8s`. |
| 1.3 | MicroK8s snap kurulumu. | `skills/microk8s-install-base` | `microk8s status --wait-ready` çıkış kodu 0. | Snap kurulum hatası → ağ/proxy: [MicroK8s proxy](https://microk8s.io/docs/install-proxy); ardından 1.3’ü tekrarla. |

---

## Faz 2 — Altyapı (MicroK8s + Juju)

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| 2.1 | Addon’lar: `dns`, `hostpath-storage`, `metallb` (sandbox için tek IP aralığı yeterli). | `skills/microk8s-addons-dns-storage` | `microk8s status` → `dns`, `hostpath-storage`, `metallb` **enabled**; `microk8s kubectl rollout status ...` ile CoreDNS / hostpath-provisioner / metallb speaker **successfully rolled out**. | MetalLB yanlış IP → `microk8s disable metallb` sonra skill’deki `IPADDR` ile yeniden `enable`. DNS/storage not ready → rollout loglarına bak; 2.1’i tekrarla. |
| 2.2 | Juju istemcisi (snap). | `skills/juju-snap-setup` | `juju version` çalışır; kanal proje politikasıyla sabit. | Snap kanalı çakışması → `snap info juju`; gerekirse `snap refresh juju --channel=...`. |
| 2.3 | Kubernetes bulutu kaydı + **bootstrap** (örn. `juju bootstrap microk8s <controller>`). | `skills/juju-bootstrap-microk8s` | `juju controllers` ilgili controller’ı **running** gösterir; `juju status` (controller modeli) hatasız. | `add-k8s` / RBAC hataları → `microk8s status`; kubeconfig: `microk8s config`. Bootstrap yarım kaldıysa: `juju controllers` / `juju destroy-controller` (dikkat: veri siler) dokümantasyonuna göre temizle ve 2.3’ü yeniden dene. |

---

## Faz 3 — Deployment (model + COS Lite bundle)

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| 3.1 | Ayrı model: `cos`. | `skills/juju-model-cos` | `juju switch cos`; `juju models` içinde `cos` aktif. | Yanlış modeldeysen: `juju switch cos`. Model silinmişse: `juju add-model cos` ile yeniden 3.1. |
| 3.2 | Bundle deploy: `juju deploy cos-lite --trust`. | Tüm `skills/cos-deploy-*` (bundle bu charm’ları birlikte kurar: prometheus, loki, alertmanager, grafana, traefik, catalogue) | `juju status --relations` → tüm uygulamalar **active** (veya geçici **waiting** sonrası **active**); birimler **idle**; uzun süre **error**/PVC **Pending** yok. | `--trust` unutulduysa kaldır ve yeniden deploy veya `juju trust` dokümantasyonu. PVC **Pending** → `microk8s kubectl get pvc -A`; storage class / hostpath (Faz 2.1). Charm **blocked** → `juju debug-log`, ilgili uygulama `juju status` mesajı. Tamamen yeniden deneme: modeldeki uygulamaları kaldırma riski — tercihen boş `cos` modelinde tekrar 3.2. |

---

## Faz 4 — Entegrasyon (ilişkiler + ingress)

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| 4.1 | Bundle ilişkileri: Prometheus/Loki ↔ Grafana (`grafana-source`, `grafana-dashboard`). | `skills/cos-relation-prometheus-grafana`, `skills/cos-relation-loki-grafana` | `juju status --relations` tablosunda ilgili entegrasyonlar listelenir; `blocked` yok. | Eksik entegrasyon (manuel senaryoda): `juju integrate ...` uçları skill’lerdeki gibi; bundle’da nadiren — `juju resolve` / charm log. |
| 4.2 | Traefik ingress ve proxied uçlar. | `skills/cos-deploy-traefik`, `skills/cos-ingress-config` | `juju run traefik/0 show-proxied-endpoints --format=yaml` anlamlı URL; Traefik servisi LoadBalancer **EXTERNAL-IP** atanmış (veya env’e uygun). | **Gateway / LB IP yok** → MetalLB (Faz 2.1); [Traefik troubleshooting](https://documentation.ubuntu.com/observability/how-to/troubleshooting/troubleshoot-gateway-address-unavailable/). Grafana URL listede yok → `juju show-unit catalogue/0` içindeki `url` alanları (skill’deki not). |

---

## Faz 5 — Doğrulama

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| 5.1 | Grafana admin erişimi. | `skills/cos-deploy-grafana` | `juju run grafana/leader get-admin-password --model cos`; kullanıcı `admin` ile UI veya HTTPS. | Parola alınamıyorsa → `juju status` grafana birimi `active` mi; `juju run grafana/0 get-admin-password`. |
| 5.2 | Uç nokta sağlığı (örnek). | `skills/cos-ingress-config` | İlgili ingress URL’lerinde HTTP 200/302; örn. Alertmanager `/-/ready` dokümantasyondaki path ile uyumlu `curl`. | **no data** Grafana’da → [troubleshoot no data](https://documentation.ubuntu.com/observability/how-to/troubleshooting/troubleshoot-no-data-in-grafana-panels/); ilişkiler (Faz 4.1). |
| 5.3 | Genel sağlık özeti. | `documantations/ARCHITECTURE_COS.md` | `juju status --relations` son görünüm arşivlendi; izleme için `juju status --relations --watch=5s` kapatılabilir. | Sürekli **degraded** → `juju debug-log`, `microk8s kubectl get pods -A` (COS namespace/model pod’ları). |

---

## Hızlı geri sarma özeti

| Sorun | Önce kontrol et | Gerekirse |
|-------|-----------------|-----------|
| Küme hazır değil | `microk8s status`, addon rollout | Faz 2.1 |
| Juju cluster yok | `juju controllers` | Faz 2.3 |
| COS deploy takıldı | `juju status`, PVC, `juju debug-log` | Faz 3.2; storage/network |
| Ingress açılmıyor | MetalLB, Traefik LB, `show-proxied-endpoints` | Faz 2.1 + 4.2 |
| Grafana boş | İlişkiler, datasource | Faz 4.1 + 5.2 |

---

## Dış kaynak

- [COS Lite on MicroK8s](https://documentation.ubuntu.com/observability/track-2/tutorial/installation/cos-lite-microk8s-sandbox/)
