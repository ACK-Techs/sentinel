# Sentinel CLI (Faz 4)

Bu dizin, `sentinel-coming` deposundaki **Sentinel CLI** paketidir. Faz 1 içeriği depo kökündeki `documantations/` ve `skills/` altında kalır; Faz 2 ile kurulan Python tabanlı terminal ajanı Faz 3’te iç kullanım için sertleştirilir.

İlk okuma için: [ARCHITECTURE_AGENTIC_CLI.md](documantations/ARCHITECTURE_AGENTIC_CLI.md), [LLM_PROVIDERS.md](documantations/LLM_PROVIDERS.md), [PHASE3_SKILL_AND_DOC_INDEX.md](documantations/PHASE3_SKILL_AND_DOC_INDEX.md), [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md).

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
export SENTINEL_OPENAI_BASE_URL=https://api.example.com/v1
export SENTINEL_API_KEY=sentinel_api_key_placeholder
export SENTINEL_MODEL=provider-model-placeholder

python -m sentinel_cli doctor --profile cloud
python -m sentinel_cli run --profile cloud "Grafana durumunu ozetle"
```

Gemini'yi mevcut OpenAI-uyumlu `cloud` yolu üzerinden denemek için kısa örnek:

```bash
cd sentinel-coming/cli
source .venv/bin/activate

export SENTINEL_PROFILE=cloud
export SENTINEL_OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
export SENTINEL_API_KEY=gemini_api_key_placeholder
export SENTINEL_MODEL=gemini-2.5-flash

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
export SENTINEL_LOCAL_MODEL=local_model_placeholder

python -m sentinel_cli doctor --profile local
python -m sentinel_cli run --profile local "Prometheus sagligini kontrol et"
```

Env adlari `LLM_PROVIDERS.md` ile hizalidir; gerçek secret değerleri repoya yazılmamalıdır.

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

Detaylı faz planları: [Faz 2](documantations/IMPLEMENTATION_PLAN_PHASE2.md), [Faz 3](documantations/IMPLEMENTATION_PLAN_PHASE3.md), [Faz 4](documantations/IMPLEMENTATION_PLAN_PHASE4.md). Yol haritası özeti: [ROADMAP_PHASE3_5.md](documantations/ROADMAP_PHASE3_5.md).

Geliştirici: [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md). Faz 3 env ve indeks: [ENV_FLAGS_PHASE3.md](documantations/ENV_FLAGS_PHASE3.md), [PHASE3_SKILL_AND_DOC_INDEX.md](documantations/PHASE3_SKILL_AND_DOC_INDEX.md). Faz 3’ü ajanla tek oturumda işlemek için: [CODEX_EXECUTION_PROMPT_PHASE3.md](documantations/CODEX_EXECUTION_PROMPT_PHASE3.md).

Faz 4 (Grafana / observability bağlantısı): [PHASE4_SKILL_AND_DOC_INDEX.md](documantations/PHASE4_SKILL_AND_DOC_INDEX.md), [PHASE4_MANAGER_HANDOFF.md](documantations/PHASE4_MANAGER_HANDOFF.md), [GRAFANA_HTTP_PHASE4.md](documantations/GRAFANA_HTTP_PHASE4.md), canlı stack doğrulama notu: [PHASE4_REAL_STACK_VERIFY.md](documantations/PHASE4_REAL_STACK_VERIFY.md). Tek oturum prompt: [CODEX_EXECUTION_PROMPT_PHASE4.md](documantations/CODEX_EXECUTION_PROMPT_PHASE4.md). Canlı test öncesi mimari + test genişletme: [PRE_LIVE_VALIDATION_HANDOFF.md](documantations/PRE_LIVE_VALIDATION_HANDOFF.md).

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

Canli stack dogrulamasi sonucu veya atlama notu su dosyada tutulur: [PHASE4_REAL_STACK_VERIFY.md](documantations/PHASE4_REAL_STACK_VERIFY.md). Faz 4 HTTP sozlesmesi ve env detaylari: [GRAFANA_HTTP_PHASE4.md](documantations/GRAFANA_HTTP_PHASE4.md).
