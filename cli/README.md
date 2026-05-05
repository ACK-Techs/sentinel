# Sentinel CLI (Faz 4)

Bu dizin, `sentinel-coming` deposundaki **Sentinel CLI** paketidir. Faz 1 içeriği depo kökündeki `documantations/` ve `skills/` altında kalır; Faz 2 ile kurulan Python tabanlı terminal ajanı Faz 3’te iç kullanım için sertleştirilir.

İlk okuma için: [ARCHITECTURE_AGENTIC_CLI.md](documantations/ARCHITECTURE_AGENTIC_CLI.md), [LLM_PROVIDERS.md](documantations/LLM_PROVIDERS.md), [OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md](documantations/OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md), [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md).

## Faz 1 ve Faz 2 ayrımı

| Faz | Konum | Amaç |
|-----|-------|------|
| Faz 1 | `sentinel-coming/documantations/`, `sentinel-coming/skills/` | COS Lite kurulumu, Juju/MicroK8s/COS operasyon bilgisi |
| Faz 2 | `sentinel-coming/cli/` | Bu yığına danışan, iyileştirme öneren ve arıza anında yönlendiren agentic CLI |

Faz 2, Faz 1'in yerine geçmez. CLI, Faz 1 belgeleri ve skill'leriyle tutarlı kalacak şekilde çalışır. Faz 2 teslim notlarının tarihsel özeti için [documantations/archive/README.md](documantations/archive/README.md) dosyasına bakılabilir.

## Paket yolu

- Paket kökü: `sentinel-coming/cli/`
- Python kaynakları: `sentinel-coming/cli/src/sentinel_cli/`
- Testler: `sentinel-coming/cli/tests/`
- Faz 2 belgeleri: `sentinel-coming/cli/documantations/`
- Faz 2 skill'leri: `sentinel-coming/cli/skills/agentic-*/SKILL.md`

## sentinel-coming ile ilişki

- Bu klasör, ana deponun içinde bağımsız dağıtılabilir bir Python paketi olarak hazırlanır.
- Workspace altındaki `agentic/Pywen-dev`, `agentic/codex-main` ve `agentic/claude` yalnızca referans tasarım kaynağıdır; Sentinel CLI içine alt modül veya vendor kopya olarak eklenmez.
- Lisans ve uyarlama notları için [DEPENDENCY_LICENSES.md](documantations/archive/DEPENDENCY_LICENSES.md) (arşiv) dosyasına bakılmalıdır.

## CLI modları

Faz 2.C ile birlikte CLI aşağıdaki temel akışları destekleyecek şekilde genişletildi:

- `sentinel-cli run "prompt"`: tek seferlik çalıştırma
- `echo "prompt" | sentinel-cli`: pipe / non-interactive once modu
- `sentinel-cli repl`: etkileşimli REPL
- `sentinel-cli config`: efektif config özeti
- `sentinel-cli doctor`: profil ve MCP/bağımlılık durumu özeti
- `sentinel-cli obs metric '<query>'`: gateway uzerinden metric sorgusu
- `sentinel-cli obs logs --service gateway`: gateway uzerinden log sorgusu
- `sentinel-cli obs traces --service orders`: gateway uzerinden trace aramasi
- `sentinel-cli run/repl`: gerekiyorsa `obs_metric_query`, `obs_logs_query`, `obs_traces_search`, `obs_trace_get` tool'lariyla gateway uzerinden canli observability okur

Örnek:

```bash
cd sentinel-coming/cli
PYTHONPATH=src python -m sentinel_cli --help
PYTHONPATH=src python -m sentinel_cli run "Grafana durumunu ozetle"
PYTHONPATH=src python -m sentinel_cli repl
```

`uv` kullanan akışlar için `pyproject.toml` hazırdır. MCP özelliğini açmak için opsiyonel extra: `pip install -e ".[mcp]"`. Extra yokken MCP çalışmaz; `doctor` bunu açık yazar.

## Kurulum

`pyproject.toml` içindeki paket adı `sentinel-cli`, mevcut sürüm `0.1.0` ve konsol script adı `sentinel-cli` olarak kalır. En sade yerel geliştirme akışı:

```bash
cd sentinel-coming/cli
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m sentinel_cli --help
```

MCP ekstra bağımlılığı ile:

```bash
cd sentinel-coming/cli
source .venv/bin/activate
python -m pip install -e ".[dev,mcp]"
python -m sentinel_cli doctor --profile local
```

`uv` tercih ediyorsanız:

```bash
cd sentinel-coming/cli
uv sync --extra dev
uv run python -m sentinel_cli doctor --profile local
uv run python -m pytest -q
```

Kurulum sonrası günlük geliştirme komutları:

```bash
cd sentinel-coming/cli
source .venv/bin/activate
python -m pytest -q
python -m ruff check .
```

Hızlı başlangıç için ayrıntılı bloklar (arşiv): [USER_QUICKSTART_PHASE2E.md](documantations/archive/USER_QUICKSTART_PHASE2E.md)

### Kurulum hazırken CLI’yi başlatma

Kurulum (`pip install -e ".[dev]"` vb.) bir kez yapıldıysa, her yeni terminal oturumunda şunlar yeterlidir:

1. `sentinel-coming/cli` dizinine geçin (`.env` ve `config/sentinel.yaml` buradan okunur).
2. Sanal ortamı açın: `source .venv/bin/activate` (Windows’ta `.venv\Scripts\activate`).

**Sürekli sohbet (REPL):** Shell’de tek başına `run` yazmayın; etkileşimli mod için mutlaka modül veya konsol script’i ile çağırın:

```bash
cd sentinel-coming/cli
source .venv/bin/activate
python -m sentinel_cli repl
```

Aynı işlev, PATH’te `sentinel-cli` varsa: `sentinel-cli repl`. Bu modda oturum açık kalır; tek komutluk çalıştırma için `python -m sentinel_cli run "..."` kullanılır.

## Yapılandırma

Repoda yalnızca **şablonlar** tutulur; gerçek değerler yerel dosyalarda kalır (commitlenmez).

| Dosya | Amaç |
|-------|------|
| `config/sentinel.example.yaml`, `.env.example` | Başkalarına / yeni klonlara tanıtım; placeholder değerler |
| `config/sentinel.yaml`, `.env` | Günlük kullanım; `.gitignore` içindedir |

İlk kurulum:

```bash
cd sentinel-coming/cli
cp config/sentinel.example.yaml config/sentinel.yaml
cp .env.example .env
# .env içinde API anahtarlarını ve SENTINEL_PROFILE vb. doldurun
```

`SENTINEL_CONFIG` için önerilen yol `./config/sentinel.yaml`dır (`.env.example` ile uyumludur).

Bellek (otomatik çıkarım, dream, MAGIC DOC), turn sonu boru hattı ve bash salt okunur modu için ortam anahtarları `documantations/ENV_FLAGS_PHASE3.md` dosyasında özetlenir; üretimde pipe/bare çalıştırmada bellek yan etkileri varsayılan olarak kapalıdır (`SENTINEL_MEMORY_ALLOW_NON_INTERACTIVE`).

Komutları **her zaman `sentinel-coming/cli` içinden** çalıştırın; CLI başlarken bu dizindeki `.env` dosyası otomatik okunur (`source .env` gerekmez). Önce doğrulama:

```bash
cd sentinel-coming/cli
source .venv/bin/activate
python -m pip install -e ".[dev]"   # bir kez / güncelleme sonrası
python -m sentinel_cli doctor --profile cloud
```

Cloud + Google Gemini (OpenAI uyumlu köprü) kullanıyorsanız, araç şeması yüzünden sık görülen HTTP 400 için `.env` içinde `SENTINEL_CLOUD_SUPPORTS_TOOLS=false` bırakın.

```bash
python -m sentinel_cli run --profile cloud "Grafana durumunu kisa ozetle"
```

Observability komutlari artik Prometheus, Loki ve Tempo adreslerini dogrudan bilmez. Bunun yerine tek baglanti noktasi olarak `observability-gateway` servisine gider.

Gateway ayarlari:

```yaml
observability_gateway:
  enabled: true
  base_url: http://127.0.0.1:8091
  timeout_sec: 10
  token_env: SENTINEL_OBSERVABILITY_GATEWAY_TOKEN
```

Env override ornekleri:

```bash
export SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL=http://127.0.0.1:8091
export SENTINEL_OBSERVABILITY_GATEWAY_TIMEOUT_SEC=10
export SENTINEL_OBSERVABILITY_GATEWAY_TOKEN_ENV=SENTINEL_OBSERVABILITY_GATEWAY_TOKEN
export SENTINEL_OBSERVABILITY_GATEWAY_TOKEN=lab-gateway-token
```

Ornek komutlar:

```bash
python -m sentinel_cli doctor --profile local
python -m sentinel_cli obs metric 'up'
python -m sentinel_cli obs logs --service gateway
python -m sentinel_cli obs traces --service orders
python -m sentinel_cli run --profile local "orders servisinde hata var mi bak"
```

`run` ve `repl` akisi da backend adreslerini dogrudan bilmez. Agent tarafinda kullanilan observability tool'lar sadece `observability-gateway` uzerinden calisir. Oturum baslangicinda session'a kisa bir operasyonel snapshot eklenir:

- gateway health
- configured backend listesi
- reachable backend listesi

Bu snapshot canli metric/log/trace dump'i degildir ve token/header icermez.

## Canli Lab Smoke

Gateway + CLI canli smoke akisi icin lab/local hedefli referans script:

```bash
cd sentinel-coming/test-platform
../.venv/bin/python -m pip install -e ../observability-gateway -e ../cli
./scripts/run_cos_stack_check.sh
```

Script su akisi tek seferde dener:

1. COS port-forward ve test-platform servislerini ayaga kaldirir.
2. `observability-gateway` servisini `127.0.0.1:8091` uzerinde baslatir.
3. `GET /health` ve `GET /api/v1/status` ile gateway'i dogrular.
4. `sentinel_cli doctor`, `obs metric`, `obs logs`, `obs traces` komutlarini calistirir.
5. `sentinel_cli run` yolunu scripted provider ile smoke ederek agent'in gateway tool cagirabildigini dogrular.
5. Tum ciktilari `test-platform/runs/cos-smoke-YYYYMMDD-HHMMSS/` altina kaydeder.

Canli kullanim ornekleri:

```bash
cd sentinel-coming/cli
source .venv/bin/activate
export SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL=http://127.0.0.1:8091

python -m sentinel_cli doctor --profile local
python -m sentinel_cli obs metric 'app_orders_created_total'
python -m sentinel_cli obs logs --service gateway
python -m sentinel_cli obs traces --service orders
python -m sentinel_cli run --profile local "gateway loglarinda son 5 dakikayi ozetle"
```

Run klasorunde beklenen artefactlar:

- `observability-gateway.log`
- `observability-gateway-health.json`
- `observability-gateway-status.json`
- `cli-doctor.json`
- `cli-obs-metric.json`
- `cli-obs-logs.json`
- `cli-obs-traces.json`
- `cli-agent-run.json`

## Wheel ile kurulum (iç kullanım)

Wheel kurulumu, geliştirme modundan farklı olarak paketi editable olmadan doğrular. İç kullanım için önerilen akış:

```bash
cd sentinel-coming/cli
source .venv/bin/activate
python -m build
python -m pip install dist/sentinel_cli-*.whl
sentinel-cli --help
sentinel-cli version
```

`pip install -e ".[dev]"` geliştirme sırasında kaynak ağacını doğrudan kullanır; `dist/sentinel_cli-*.whl` ile kurulum ise üretilen paketin temiz bir ortamda gerçekten açıldığını doğrulamak içindir. Tek komutla smoke almak istersen `scripts/smoke_wheel.sh` kullanılabilir.

## Hızlı başlangıç

Cloud profil örneği:

```bash
cd sentinel-coming/cli
source .venv/bin/activate

export SENTINEL_PROFILE=cloud
export SENTINEL_OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
export SENTINEL_API_KEY=<set>
export SENTINEL_MODEL=gemini-2.5-flash
export SENTINEL_CLOUD_SUPPORTS_TOOLS=false

python -m sentinel_cli doctor --profile cloud
python -m sentinel_cli run --profile cloud "Grafana durumunu ozetle"
```

Repo varsayilani artik `cloud` profili ve Gemini OpenAI-uyumlu bridge'idir. Local Gemma fallback olarak korunur.

Gemini'yi mevcut OpenAI-uyumlu `cloud` yolu üzerinden denemek için kısa örnek:

```bash
cd sentinel-coming/cli
source .venv/bin/activate

export SENTINEL_PROFILE=cloud
export SENTINEL_OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
export SENTINEL_API_KEY=<set>
export SENTINEL_MODEL=gemini-2.5-flash
export SENTINEL_CLOUD_SUPPORTS_TOOLS=false

python -m sentinel_cli doctor --profile cloud
python -m sentinel_cli run --profile cloud "Grafana durumunu kisa ozetle"
```

Bu yol yalnız Google'ın OpenAI-compatible köprüsünü hedefler; native Gemini JSON API bu repo akışında kullanılmaz. Güncel URL ve model adları için [LLM_PROVIDERS.md](documantations/LLM_PROVIDERS.md) ve resmi Google dokümantasyonunu kontrol et.

Local profil örneği:

```bash
cd sentinel-coming/cli
source .venv/bin/activate

export SENTINEL_PROFILE=local
export SENTINEL_LOCAL_BASE_URL=http://127.0.0.1:11434/v1
export SENTINEL_LOCAL_MODEL=gemma4:latest

python -m sentinel_cli doctor --profile local
python -m sentinel_cli run --profile local "Prometheus sagligini kontrol et"
```

Env adlari `LLM_PROVIDERS.md` ile hizalidir; gerçek secret değerleri repoya yazılmamalıdır.

## Uctan Uca Smoke

Tek komutta tum gozlemlenebilirlik zincirini dogrulayan referans akis:

```bash
cd sentinel-coming/test-platform
./scripts/run_cos_stack_check.sh
```

Bu smoke su zinciri dogrular:

1. COS hazir
2. test-platform servisleri ayaga kalkiyor
3. telemetry COS Prometheus/Loki/Tempo'ya akiyor
4. observability-gateway bu backend'leri okuyabiliyor
5. `sentinel_cli doctor` ve `obs` komutlari canli veriye baglaniyor
6. `sentinel_cli run` scripted smoke'u gateway tool cagrisiyla calisiyor

## MCP

Faz 2.C için desteklenen transport yalnızca **`stdio`**. Kurulum ve örnek:

```bash
cd sentinel-coming/cli
python3 -m pip install -e ".[mcp]"
PYTHONPATH=src python -m sentinel_cli doctor --profile local
```

`config/sentinel.yaml` (şablondan oluşturduğunuz dosya) içindeki `mcp.servers` bölümü stdio komutu ile güncellenebilir; şablon için `sentinel.example.yaml`a bakın. MCP araçları modele `mcp_<server>_<tool>` isim alanıyla girer; çağrıda mevcut **approval** politikası geçerlidir.

Yerleşik `bash`, `write_file` ve MCP araçları sessiz “yolo” modunda çalışmaz; approval kapısı mimaride tarif edilen risk sınıflarına göre devrededir.

**Notlar (sınırlar ve beklentiler):**

- **`[mcp]` extra’sı:** PyPI’daki `mcp` paketi özelliği **açmak için kapı** olarak kullanılır; stdio üzerindeki JSON-RPC akışı istemci tarafında bu repoda uygulanır (resmi SDK transport’u zorunlu değildir).
- **Protokol sürümü:** İstemci `initialize` içinde sabit bir `protocolVersion` kullanır; sunucu farklı bir sürüm bekliyorsa ileride el sıkışma (negotiation) gerekebilir.
- **Stdout varsayımı:** Yanıtlar **satır başına tek JSON** olarak okunur; sunucu stdout’a ek log yazarsa veya karışık çıktı verirse ayrıştırma kırılabilir.

Yapılandırmada log çıktısı için `logging.json_format: true|false` kullanılır (`json` anahtarı eski dosyalar için alias olarak hâlâ kabul edilir).

## Faz 2.E notları

- Skill yazım standardı için kısa uyum özeti (arşiv): [SKILL_AUTHORING_PHASE2E.md](documantations/archive/SKILL_AUTHORING_PHASE2E.md)
- Telemetri politikası (arşiv): [TELEMETRY_POLICY_PHASE2E.md](documantations/archive/TELEMETRY_POLICY_PHASE2E.md)
- Deneysel bayrak iskelesi: `SENTINEL_EXPERIMENTAL_MCP=false` varsayılanı eklidir; bu turda yalnız config/env rezervasyonu olarak tutulur, yeni çalışma zamanı davranışı açmaz.

**Faz 3 (iç kullanım):** Uygulama şu an uzaktan kullanım analitiği veya ürün telemetrisi göndermez; yapılandırdığın LLM API çağrıları ve yerel loglar buna dahil değildir. Ayrıntı: `skills/agentic-faz3-no-remote-telemetry/SKILL.md`.

Bağımlılık güncellerken küçük ve geri döndürülebilir artışları tercih et. `pyproject.toml` içindeki major sürüm üst sınırlarını gevşetmek veya yeni ağır bağımlılık eklemek, Faz 3 kapsamında otomatik yapılacak bir iş değil; önce test, CI ve wheel smoke etkisiyle birlikte bilinçli karar olarak ele alınmalıdır.

## Faz 2.A çıktıları

- Paketleme ve repo yerleşimi
- Başlangıç bağımlılık ve lisans envanteri
- Tehdit modeli ve sır yönetimi belgeleri
- Onay politikası ve prompt injection guardrail özeti

Aktif planlama ve sonraki adım dokümanı: [OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md](documantations/OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md). Faz 2 temel teslimi için [IMPLEMENTATION_PLAN_PHASE2.md](documantations/IMPLEMENTATION_PLAN_PHASE2.md), teknik referans için [GRAFANA_HTTP_PHASE4.md](documantations/GRAFANA_HTTP_PHASE4.md) ve [GRAFANA_AI_PLATFORM_RESEARCH.md](documantations/GRAFANA_AI_PLATFORM_RESEARCH.md) korunur.

## Faz 4: Grafana baglanti dogrulamasi

Faz 4 ile `sentinel-cli doctor` mevcut profil/MCP ozetine ek olarak opsiyonel Grafana HTTP baglanti kontrolu de yapar. Ama amac dar tutulur: Grafana'ya erisiliyor mu, token reddediliyor mu, timeout mu var? Dashboard otomasyonu veya veri kaynagi kurulumunu yapmaz.

Ornek env:

```bash
cd sentinel-coming/cli
source .venv/bin/activate

export SENTINEL_GRAFANA_BASE_URL=https://grafana.example.com
export SENTINEL_GRAFANA_TOKEN=replace_me
# Opsiyonel:
# export SENTINEL_GRAFANA_TIMEOUT_SEC=5
# export SENTINEL_GRAFANA_VERIFY_SSL=false

python -m sentinel_cli doctor --profile local
```

YAML tarafinda ayni alanlar `config/sentinel.example.yaml` icindeki `grafana:` bolumunde bulunur. Secret degerleri YAML'a commit etmeyin; token'i env'de tutun.

`doctor` cikti notlari:

- `ok`: `GET /api/health` 200 dondu
- `unauthorized`: HTTP cevap veriyor ama token veya yetki reddedildi
- `timeout`: URL, TLS veya ag erisimi kontrol edilmeli
- `skipped`: `SENTINEL_GRAFANA_BASE_URL` ayarlanmadigi icin aktif test yapilmadi

Grafana erisiyor ama panellerde veri yoksa bu Faz 4 kontrolunun kapsami disindadir; datasource sirasini ve Faz 1 teshis akisini dogrulayin. Kopru skill: `skills/agentic-troubleshoot-grafana/SKILL.md`

Canli stack dogrulamasi ve bundan sonraki agent baglama adimlari [OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md](documantations/OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md) icinde tutulur. HTTP sozlesmesi ve env detaylari icin: [GRAFANA_HTTP_PHASE4.md](documantations/GRAFANA_HTTP_PHASE4.md).

## REPL + Grafana ozeti

`sentinel-cli run` ve `sentinel-cli repl`, istenirse oturum basinda Grafana baglanti durumunun secret-safe bir ozetini system prompt icine ekler. Bu ozet canli panel veya metrik akisi degildir; yalniz operasyonel baglanti durumudur.

- YAML: `agent.grafana_context_in_repl: true`
- Env override: `SENTINEL_GRAFANA_CONTEXT_IN_REPL=false`

Bu ozet session mesajlarina ayri bir `user` mesaji olarak yazilmaz; compaction davranisi bozulmasin diye oturum metadata'sinda snapshot olarak tutulur.

## Bireysel kapanis: REPL ve Grafana ozeti

`doctor` ciktisi REPL sohbetine otomatik dusmez. Grafana Labs LLM / Assistant ozellikleri Grafana UI veya Cloud katmaninda calisir; terminal ajanindan farklidir — ozet: [GRAFANA_AI_PLATFORM_RESEARCH.md](documantations/GRAFANA_AI_PLATFORM_RESEARCH.md). REPL ve ajan tarafinda gateway verisini nasil kullanacagimiz yeni planda toplanir: [OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md](documantations/OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md).

**Otomatik adim adim dogrulama:** `scripts/verify_grafana_context_repl.sh` — `cli` kokunden `./scripts/verify_grafana_context_repl.sh`. Adimlar arasinda Enter ile duraklatmak icin: `STEP_PAUSE=1 ./scripts/verify_grafana_context_repl.sh`.
