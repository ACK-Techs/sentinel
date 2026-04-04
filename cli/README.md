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

## Faz 2.A çıktıları

- Paketleme ve repo yerleşimi
- Başlangıç bağımlılık ve lisans envanteri
- Tehdit modeli ve sır yönetimi belgeleri
- Onay politikası ve prompt injection guardrail özeti

Detaylı faz planı için [IMPLEMENTATION_PLAN_PHASE2.md](documantations/IMPLEMENTATION_PLAN_PHASE2.md) dosyasına bakılmalıdır.
