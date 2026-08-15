# Sentinel indirme ve kurulum kılavuzu

Bu belge üç ortamı **ayırır**. Aynı komut hepsinde işe yaramaz.

| Ortam | Stack’i kim kurar? | `sentinel install` ne yapar? |
|--------|--------------------|------------------------------|
| **1. Docker Compose** | CLI installer | Hem yığını ayağa kaldırır hem CLI’yi bağlar |
| **2. Kubernetes (Helm)** | CLI installer (mevcut kümede) | Chart’ı yükler ve CLI’yi bağlar. Küme **sizin** olmalı |
| **3. Juju / COS** | Önce `.sh` script’leri | COS’u **indirmez**. COS zaten duruyorsa adresleri bulup config yazmayı dener (bu adım henüz yarım) |

Kısa kural:

- **Compose / K8s:** önce CLI, sonra `sentinel install`.
- **COS:** önce script’ler (MicroK8s + Juju + COS), sonra CLI’yi gateway üzerinden bağlama. `sentinel install --mode cos` COS kurucusu değildir.

Ürün Pre-Alpha / lab içindir. Production TLS, secret rotation ve Windows kurulumu bu kılavuzun kapsamı dışındadır.

---

## Ortak: Sentinel CLI

Üç yolda da CLI gerekir. Kaynak ağaçtan kurulum (önerilen; PyPI yayını yok):

```bash
git clone https://github.com/caglarkc/sentinel-coming.git
cd sentinel-coming/cli
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m sentinel_cli --help
```

Yerel config şablonları:

```bash
cp config/sentinel.example.yaml config/sentinel.yaml
cp .env.example .env
```

Ajan (`run` / `repl`) için ayrıca bir LLM gerekir (cloud API anahtarı veya yerel Ollama). `obs` ve `doctor` komutları LLM olmadan da çalışır; gateway ayaktaysa telemetry okunur.

Kökteki `install.sh` TestPyPI + git fallback dener. Lab için güvenilir yol yukarıdaki `pip install -e` akışıdır.

---

## 1) Docker Compose

**Kim için:** Tek makine, Docker var, en hızlı demo.

**Ne kurulur:** Prometheus, Loki, Tempo, Grafana, Sentinel observability-gateway.

**Ne kurulmaz:** Kubernetes, Juju, COS, `test-platform` uygulama servisleri.

### Önkoşul

- Linux (veya Docker Engine çalışan bir ortam)
- Docker Compose v2 (`docker compose version`)
- Python 3.11+ ve yukarıdaki CLI kurulumu

### Kurulum

CLI sanal ortamı açıkken, çalışmak istediğiniz dizinde:

```bash
export SENTINEL_OBSERVABILITY_GATEWAY_TOKEN=lab-gateway-token
python -m sentinel_cli install --mode compose
```

Bu komut:

1. Docker’ı kontrol eder
2. Paketlenmiş Compose dosyalarını `./sentinel-compose/` altına kopyalar
3. `docker compose up -d` çalıştırır
4. Gateway / Grafana adreslerini `~/.sentinel/config.yaml` dosyasına yazar

Token vermezseniz installer lab için `lab-gateway-token` kullanır.

### Elle (installer olmadan)

```bash
cd for-download/compose
cp .env.example .env   # varsa
docker compose up -d
```

Sonra CLI’de gateway’i açın (`observability_gateway.enabled`, `base_url: http://127.0.0.1:8091`) ve aynı token’ı export edin.

### Doğrulama

```bash
python -m sentinel_cli doctor --profile local
python -m sentinel_cli obs metric 'up'
```

Beklenti: `observability_gateway.ok = true`, metric cevabında `backend: prometheus`.

---

## 2) Kubernetes (Helm)

**Kim için:** Zaten çalışan bir Kubernetes kümesi var (`kubectl` bağlamı hazır).

**Ne kurulur:** `charts/sentinel` ile Prometheus, Loki, Tempo, Grafana, `sentinel-gateway`.

**Ne kurulmaz:** MicroK8s, Juju, COS Lite. Installer küme **oluşturmaz**.

### Önkoşul

- `kubectl` (hedef kümeye bakıyor)
- `helm`
- Kümede chart bağımlılıklarını çekebilecek ağ erişimi
- Sentinel CLI (ortak bölüm)

### Kurulum (CLI installer)

```bash
export SENTINEL_OBSERVABILITY_GATEWAY_TOKEN=lab-gateway-token
python -m sentinel_cli install --mode k8s
```

Installer chart kopyalar, `helm dependency update` ve `helm upgrade --install` çalıştırır, ardından keşif ile `~/.sentinel/config.yaml` yazar.

### Kurulum (Helm doğrudan)

```bash
cd sentinel-coming
helm dependency update ./charts/sentinel
helm upgrade --install sentinel ./charts/sentinel \
  --create-namespace -n sentinel \
  --set gateway.token=lab-gateway-token
```

Ayrıntı: `charts/sentinel/README.md`.

Gateway’e makinenizden ulaşmak için Servis tipine göre port-forward veya ingress gerekir. CLI, erişilebilen gateway `base_url` olmadan `obs` çalıştırmaz.

### Doğrulama

```bash
kubectl get pods -n sentinel
python -m sentinel_cli doctor --profile local
python -m sentinel_cli obs metric 'up'
```

---

## 3) Juju / COS (MicroK8s)

**Kim için:** Canonical Observability Stack lab’i. Sıra **tersine** çalışır.

```text
1) .sh script’leri  →  MicroK8s + Juju + COS yığınını KURAR
2) Gateway + CLI    →  o yığına BAĞLAR
3) sentinel install --mode cos  →  COS indirmez (bağlama denemesi, henüz yarım)
```

### Önkoşul

- Ubuntu benzeri Linux, `sudo`, `snap`
- Birkaç GB RAM (COS Lite lab)
- Sentinel CLI (ortak bölüm; script’lerden **sonra** da kurulabilir)

### Adım A — altyapı ve COS’u script ile kur

Repo kökünden:

```bash
cd for-download
bash prepare-env.sh
```

Bu script MicroK8s, DNS, hostpath-storage, MetalLB, Juju kurar; controller ve `cos` modelini hazırlar. COS uygulamalarını **tek başına deploy etmez**.

COS Lite bundle:

```bash
cd for-download
juju switch cos
juju deploy ./my-product-bundle.yaml
juju status
```

Tempo ve OpenTelemetry Collector ekleri:

```bash
cd for-download
bash faz1-telemetry.sh
```

Uygulamalar `active` olana kadar `juju status` ile bekleyin. Takılırsa:

```bash
sudo ./scripts/cos-microk8s-heal.sh
# veya
sudo ./scripts/cos-microk8s-start.sh
```

Traefik / Grafana / OTLP özeti:

```bash
cd for-download
bash faz4-5.sh
```

### Adım B — Sentinel’i COS’a bağla (asıl bağlama)

`sentinel install --mode cos` COS kurmaz. Preflight / install / verify adımları kodda TODO’dur; çalışan kısım keşif + config yazmadır. Lab’de güvenilir yol **elle gateway**:

Prometheus, Loki, Tempo adreslerini Juju/K8s’den alın (MetalLB / ClusterIP). Örnek iskelet:

```bash
cd observability-gateway
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

export SENTINEL_OBSERVABILITY_GATEWAY_TOKEN=sentinel-observability-gateway-token
export SENTINEL_OBSERVABILITY_PROMETHEUS__BASE_URL=http://<prometheus-ip>:9090
export SENTINEL_OBSERVABILITY_LOKI__BASE_URL=http://<loki-ip>:3100
export SENTINEL_OBSERVABILITY_TEMPO__BASE_URL=http://<tempo-ip>:3200

python -m uvicorn observability_gateway.main:app --host 127.0.0.1 --port 8091
```

Başka bir terminalde CLI:

```bash
cd cli
source .venv/bin/activate
export SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL=http://127.0.0.1:8091
export SENTINEL_OBSERVABILITY_GATEWAY_TOKEN=sentinel-observability-gateway-token
# config/sentinel.yaml içinde observability_gateway.enabled: true ve base_url aynı olmalı
# veya install wire ~/.sentinel/config.yaml yazdıysa o dosya kullanılır

python -m sentinel_cli doctor --profile local
python -m sentinel_cli obs metric 'up'
python -m sentinel_cli obs logs --service gateway
python -m sentinel_cli obs traces --service orders
```

`obs logs` / `obs traces` için `test-platform` servisleri ve telemetry akışı gerekir. Yalnız COS ayaktaysa `obs metric 'up'` daha gerçekçi bir ilk kontroldür.

İsteğe bağlı (yarım installer):

```bash
python -m sentinel_cli install --mode cos
```

Beklenti: COS kurulumu değil; mümkünse endpoint keşfi ve `~/.sentinel/config.yaml`. Kurulum adımlarında `TODO cos:preflight` / `TODO cos:install` / `TODO cos:verify` görebilirsiniz. Bu normaldir.

### Adım C — uçtan uca lab duman testi (opsiyonel)

COS + test-platform + gateway + CLI zinciri:

```bash
cd test-platform
./scripts/run_cos_stack_check.sh
```

Bu script altyapı kontrolü, servis ayağa kaldırma, trafik, Prom/Loki/Tempo, gateway ve CLI `obs` doğrulamasını tek seferde dener. Repo kökünde bir `.venv` ve hazır COS bekler. Bitince yerel gateway prosesini kapatabilir; kalıcı kullanım için Adım B’yi tekrar açın.

---

## Üç yolu karıştırmayın

| Yapmak istediğiniz | Çalıştırın | Çalıştırmayın |
|--------------------|------------|----------------|
| Laptop’ta hızlı demo | `install --mode compose` | COS script’leri, Juju |
| Kendi K8s kümeme Sentinel yığını | `install --mode k8s` veya Helm | `prepare-env.sh` (o MicroK8s+Juju kurar) |
| COS Lite lab | `prepare-env.sh` → bundle → `faz1-telemetry.sh` → gateway | COS’u `install --mode compose` ile kurmayı beklemeyin |
| CLI’yi mevcut Prom/Loki/Tempo’ya bağla | Gateway’i o URL’lerle çalıştırın | Grafana’yı tek kaynak sanmayın; CLI Grafana query atmaz |

---

## Ortak doğrulama listesi

Kurulum bitti sayılır ancak:

1. Gateway `GET /health` 200 döner (`http://127.0.0.1:8091/health` veya küme adresi)
2. `python -m sentinel_cli doctor` içinde `observability_gateway.ok` true
3. `python -m sentinel_cli obs metric 'up'` Prometheus’tan veri döner
4. Token CLI ve gateway’de aynıdır (`SENTINEL_OBSERVABILITY_GATEWAY_TOKEN`)

Ajan denemesi (LLM ayarlıysa):

```bash
python -m sentinel_cli run --profile local "observability gateway durumunu özetle"
```

---

## Bilinen sınırlar

- `sentinel install --mode cos` tam installer değildir.
- Gateway read-only’dir; alert/dashboard yazmaz.
- Compose varsayılan token’ı lab içindir.
- `test-platform` ayrı üründür; Compose/Helm observability kurulumu sipariş servislerini getirmez.
- `agentic/` klasörü referans koddur; Sentinel kurulumu değildir.
