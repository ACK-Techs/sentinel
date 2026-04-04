# Sentinel CLI (Faz 2)

Bu dizin, `sentinel-coming` deposundaki **Faz 2 Agentic CLI** paketidir. Faz 1 içeriği depo kökündeki `documantations/` ve `skills/` altında kalır; Faz 2 için Python tabanlı terminal ajanı, ilgili belgeler ve `agentic-*` skill şartnameleri ise bu `cli/` ağacı içinde tutulur.

## Faz 1 ve Faz 2 ayrımı

| Faz | Konum | Amaç |
|-----|-------|------|
| Faz 1 | `sentinel-coming/documantations/`, `sentinel-coming/skills/` | COS Lite kurulumu, Juju/MicroK8s/COS operasyon bilgisi |
| Faz 2 | `sentinel-coming/cli/` | Bu yığına danışan, iyileştirme öneren ve arıza anında yönlendiren agentic CLI |

Faz 2, Faz 1'in yerine geçmez. CLI, Faz 1 belgeleri ve skill'leriyle tutarlı kalacak şekilde çalışır.

## Paket yolu

- Paket kökü: `sentinel-coming/cli/`
- Python kaynakları: `sentinel-coming/cli/src/sentinel_cli/`
- Testler: `sentinel-coming/cli/tests/`
- Faz 2 belgeleri: `sentinel-coming/cli/documantations/`
- Faz 2 skill'leri: `sentinel-coming/cli/skills/agentic-*/SKILL.md`

## sentinel-coming ile ilişki

- Bu klasör, ana deponun içinde bağımsız dağıtılabilir bir Python paketi olarak hazırlanır.
- Workspace altındaki `agentic/Pywen-dev`, `agentic/codex-main` ve `agentic/claude` yalnızca referans tasarım kaynağıdır; Sentinel CLI içine alt modül veya vendor kopya olarak eklenmez.
- Lisans ve uyarlama notları için [DEPENDENCY_LICENSES.md](documantations/DEPENDENCY_LICENSES.md) dosyasına bakılmalıdır.

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

Hızlı başlangıç için ayrıntılı bloklar: [USER_QUICKSTART_PHASE2E.md](documantations/USER_QUICKSTART_PHASE2E.md)

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

`config/sentinel.example.yaml` içindeki `mcp.servers` bölümü stdio komutu ile güncellenebilir. MCP araçları modele `mcp_<server>_<tool>` isim alanıyla girer; çağrıda mevcut **approval** politikası geçerlidir.

**Notlar (sınırlar ve beklentiler):**

- **`[mcp]` extra’sı:** PyPI’daki `mcp` paketi özelliği **açmak için kapı** olarak kullanılır; stdio üzerindeki JSON-RPC akışı istemci tarafında bu repoda uygulanır (resmi SDK transport’u zorunlu değildir).
- **Protokol sürümü:** İstemci `initialize` içinde sabit bir `protocolVersion` kullanır; sunucu farklı bir sürüm bekliyorsa ileride el sıkışma (negotiation) gerekebilir.
- **Stdout varsayımı:** Yanıtlar **satır başına tek JSON** olarak okunur; sunucu stdout’a ek log yazarsa veya karışık çıktı verirse ayrıştırma kırılabilir.

Yapılandırmada log çıktısı için `logging.json_format: true|false` kullanılır (`json` anahtarı eski dosyalar için alias olarak hâlâ kabul edilir).

## Faz 2.E notları

- Skill yazım standardı için kısa uyum özeti: [SKILL_AUTHORING_PHASE2E.md](documantations/SKILL_AUTHORING_PHASE2E.md)
- Telemetri politikası: varsayılan kapalı ve yalnız opt-in olacak şekilde [TELEMETRY_POLICY_PHASE2E.md](documantations/TELEMETRY_POLICY_PHASE2E.md)
- Deneysel bayrak iskelesi: `SENTINEL_EXPERIMENTAL_MCP=false` varsayılanı eklidir; bu turda yalnız config/env rezervasyonu olarak tutulur, yeni çalışma zamanı davranışı açmaz.

## Faz 2.A çıktıları

- Paketleme ve repo yerleşimi
- Başlangıç bağımlılık ve lisans envanteri
- Tehdit modeli ve sır yönetimi belgeleri
- Onay politikası ve prompt injection guardrail özeti

Detaylı faz planı için [IMPLEMENTATION_PLAN_PHASE2.md](documantations/IMPLEMENTATION_PLAN_PHASE2.md) dosyasına bakılmalıdır.
