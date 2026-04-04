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

## İskelet çalıştırma

Giriş noktası tam uygulanmadan önce bile modül iskeleti aşağıdaki gibi açılabilir:

```bash
cd sentinel-coming/cli
PYTHONPATH=src python -m sentinel_cli --help
```

`uv` kullanan akışlar için `pyproject.toml` hazırdır; ileride gerçek CLI entrypoint'i eklendiğinde `uv run python -m sentinel_cli` veya script entrypoint'i ile genişletilecektir.

## Faz 2.A çıktıları

- Paketleme ve repo yerleşimi
- Başlangıç bağımlılık ve lisans envanteri
- Tehdit modeli ve sır yönetimi belgeleri
- Onay politikası ve prompt injection guardrail özeti

Detaylı faz planı için [IMPLEMENTATION_PLAN_PHASE2.md](documantations/IMPLEMENTATION_PLAN_PHASE2.md) dosyasına bakılmalıdır.
