# Yapay Zeka Otonomi ve Hata Yönetim Protokolü

Aşağıdaki kurallar, bu depodaki dokümantasyonu kullanan **kodlayıcı yapay zekâ** (ör. Codex) için **genel prensip** olarak bağlayıcıdır; proje içi skill ve uygulama planı bunlara tabidir.

1. **Sıfır Varsayım Kuralı:** Kodlayıcı AI, eksik bir bilgi veya birden fazla seçenek içeren belirsiz bir durumla karşılaşırsa **kendi kendine karar vermez**. İşlemi **derhal durdurur**, onay ve yönlendirme için **kullanıcıya danışır**.

2. **Maksimum 2 Deneme (Fail-Safe):** Bir komut hata verirse, AI bu hatayı gidermek için **en fazla bir veya iki** düzeltme denemesi yapabilir; sonrasında aşağıdaki madde devreye girer.

3. **Derin Analiz ve Bekleme (Stop & Think):** İki denemenin ardından hata sürüyorsa AI **yeni kod veya komut denemez**. Hatayı **derinlemesine analiz eder**, olası **kök nedenleri** açıklar ve **yeni bir adım atmadan önce** kullanıcının müdahalesini veya onayını **kesinlikle bekler**.

---

# Sentinel — Proje Özeti

Bu depo, **Canonical Observability Stack (COS) Lite**’ı **MicroK8s** üzerinde **Juju** ile kurmayı, ilişkilendirmeyi ve giriş (ingress) katmanını yönetmeyi hedefleyen bir **model-tabanlı gözlemlenebilirlik** çalışma alanıdır. Amaç; metrik (Prometheus), log (Loki), uyarı (Alertmanager), pano (Grafana) ve HTTP girişi (Traefik) bileşenlerini tekrarlanabilir, sürümlenebilir ve Charmhub üzerinden tanımlı arayüzlerle ayağa kaldırmaktır.

## Vizyon

- **Tek gerçek kaynak**: Üretim benzeri kurulumda bileşen sürümleri, kanallar ve ilişkiler [Ubuntu Observability dokümantasyonu](https://documentation.ubuntu.com/observability/) ve [Charmhub `cos-lite`](https://charmhub.io/cos-lite) ile uyumlu tutulur.
- **Altyapı soyutlaması**: Juju, Kubernetes ötesinde de çalışan evrensel bir **Operator Lifecycle Manager (OLM)** olarak modelleri, ilişkileri ve yaşam döngüsünü yönetir; COS bileşenleri bu model üzerinde **charm** olarak çalışır.
- **Operasyonel netlik**: Sandbox/MicroK8s için hostPath ve MetalLB; gerektiğinde overlay’ler (`offers`, `storage-small`) ve üretimde daha dayanıklı depolama (ör. Ceph) ile genişleme yolu açık tutulur.

## Kapsam

| Alan | İçerik |
|------|--------|
| Küme | MicroK8s (tek düğüm veya POC); `dns`, `hostpath-storage`, `metallb` eklentileri |
| Orkestrasyon | Juju 3.x denetleyici, `microk8s` bulutu, ayrılmış `cos` modeli |
| Gözlem yığını | COS Lite: `prometheus-k8s`, `loki-k8s`, `alertmanager-k8s`, `grafana-k8s`, `traefik-k8s`, `catalogue-k8s` |

## Fazlar

### Faz 0 — Önkoşullar ve beceriler

- Host kaynakları: dokümantasyona uygun olarak en az **4 vCPU, 8 GiB RAM, ~40 GiB disk** (POC; üretim için artırın).
- Bu repodaki **skill** dosyaları (`skills/*/SKILL.md`) kurulum sırasını ve kuralları kod asistanına ve operatöre kısa referans olarak verir.

### Faz 1 — MicroK8s temel kurulum

- Snap ile MicroK8s, gerekli **addon**’lar: `dns`, `hostpath-storage`, `metallb` (Traefik için LoadBalancer).
- Rollout doğrulaması: CoreDNS, hostpath provisioner, MetalLB speaker.

### Faz 2 — Juju istemci ve denetleyici

- Juju snap kurulumu, `microk8s` Kubernetes bulutu olarak kayıt, **`juju bootstrap`** ile denetleyici.
- Ayrı **model**: `juju add-model cos` (veya Terraform ile eşdeğeri).

### Faz 3 — COS Lite dağıtımı

- Tercih edilen yol: **`juju deploy cos-lite --trust`** (bundle tek komutta bileşenleri ve ilişkileri kurar).
- Alternatif: bileşenleri ayrı ayrı charm olarak deploy (gelişmiş senaryolar, kanal/ölçek ince ayarı).
- Overlay: `offers-overlay.yaml` (cross-model relations), `storage-small-overlay.yaml` (ilk kurulumda depolama varsayılanları).

### Faz 4 — İlişkiler ve ingress

- Grafana ↔ Prometheus / Loki: `grafana-dashboard`, `grafana-source` benzeri entegrasyonlar bundle içinde tanımlıdır.
- Traefik: `ingress`, `ingress-per-unit`, `traefik-route`; uç noktalar için `show-proxied-endpoints` ve Catalogue.

### Faz 5 — Doğrulama ve genişletme

- `juju status --relations`, Grafana admin parolası (`get-admin-password`), isteğe bağlı alert kuralları, scrape hedefleri, TLS ve hacim değerlendirme ([Observability how-to](https://documentation.ubuntu.com/observability/how-to/)).

## Dış referanslar (güncel hat)

- [Ubuntu Observability — COS Lite on MicroK8s](https://documentation.ubuntu.com/observability/track-2/tutorial/installation/cos-lite-microk8s-sandbox/)
- [Stack variants (COS Lite vs tam COS)](https://documentation.ubuntu.com/observability/explanation/stack-variants/)
- [Juju — dağıtım yönetimi](https://documentation.ubuntu.com/juju/3.6/howto/manage-your-deployment/)
- [cos-lite-bundle (GitHub)](https://github.com/canonical/cos-lite-bundle)
- [Juju — universal operators / OLM](https://juju.is/universal-operators)

**`documantations/ARCHITECTURE_COS.md`** bileşen iletişimini şematik olarak özetler; adım adım kurulum için **`documantations/IMPLEMENTATION_PLAN.md`** kullanılır.

**Agentic CLI (ayrı iz):** Gözlemlenebilirlik yığınına danışman terminal ajanı (Faz 2) için dokümantasyon ve `agentic-*` skill şartnamesi **`cli/documantations/`** altında başlar; giriş belgesi **`cli/documantations/PROJECT_ROOT_PHASE2.md`**.
