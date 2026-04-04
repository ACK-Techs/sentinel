# Önerilen CLI dizin yapısı (Faz 2)

Bu dosya **`sentinel-coming/cli/`** altında Python paketi için **önerilen** yerleşimi tanımlar. **Zorunlu değildir**; `agentic-repo-layout` skill’i ile çelişen bir karar alınırsa, sapma gerekçesi README veya ADR ile kısaca yazılmalıdır.

## Amaç

- `ARCHITECTURE_AGENTIC_CLI.md` içindeki mantıksal katmanlara **dosya düzeyinde karşılık** vermek.
- Kodlayıcı AI ve insan geliştiriciler için **tek başlangıç şeması**; `src/` düzeni `pyproject.toml` ile uyumludur.

## Önerilen ağaç

`sentinel-coming/cli/` (köke göre göreli yollar):

```
cli/
├── pyproject.toml              # paket meta, bağımlılıklar, [project.scripts] veya [tool.hatch] entry
├── README.md                   # Faz 1/2 ayrımı, kurulum, hızlı başlangıç özeti
├── .env.example                # yalnızca placeholder; gerçek anahtar yok (A.3)
├── .gitignore                  # .env, venv, cache (yoksa eklenir)
├── documantations/             # mevcut Faz 2 belgeleri (bu dosya dahil)
├── skills/                     # mevcut agentic-* skill’ler
├── src/
│   └── sentinel_cli/           # içe aktarılabilir paket adı (ürün adı kararıyla değiştirilebilir)
│       ├── __init__.py
│       ├── __main__.py         # python -m sentinel_cli
│       ├── cli/                # giriş noktası, argparse, REPL / tek komut ayrımı (C.1)
│       ├── config/             # katmanlı birleştirme, profiller (B.1–B.2)
│       ├── llm/                # sağlayıcı sözleşmesi, adapter’lar, streaming (B.3–B.7)
│       ├── agent/              # tur döngüsü, tool parse, history (C.3–C.4, C.9)
│       ├── tools/              # registry, bash, filesystem, MCP eşlemesi (C.4–C.7)
│       ├── hooks/              # pre/post tool (C.6)
│       └── session/            # oturum / trajectory (C.8)
├── tests/
│   ├── unit/                   # birim testler (E.2)
│   └── integration/            # mock LLM ile akış (E.2)
└── config/                     # isteğe bağlı: örnek YAML’lar (repo içi secret yok)
    └── sentinel.example.yaml
```

## Katman eşlemesi (mimari ↔ dizin)

| Mimari blok (`ARCHITECTURE_AGENTIC_CLI.md`) | Önerilen paket yolu |
|---------------------------------------------|---------------------|
| entrypoint, config merge, profil | `sentinel_cli/cli/`, `sentinel_cli/config/` |
| Provider registry, stream | `sentinel_cli/llm/` |
| turn loop, history, tool parse | `sentinel_cli/agent/` |
| tool registry, bash, fs, MCP, hooks, approval | `sentinel_cli/tools/`, `sentinel_cli/hooks/` (onay politikası kodu araç kapısında veya `agent/` içinde tutulabilir) |

## Notlar

- **Paket adı** (`sentinel_cli`): `pyproject.toml` içindeki proje adı ile aynı hizada tutulmalıdır; değişirse bu belgedeki yollar güncellenir.
- **Faz 1** içerikleri (`sentinel-coming/documantations/`, `sentinel-coming/skills/`) buraya taşınmaz.
- İlk sprintte alt paketler **boş veya minimal modül** ile açılabilir; Faz 2.B–C ilerledikçe doldurulur.
- Workspace `agentic/Pywen-dev` yapısı farklıdır; orası **referans**; bu ağaç Sentinel sözleşmesine göre sadeleştirilmiştir.

## İlgili belgeler

- `ARCHITECTURE_AGENTIC_CLI.md`
- `IMPLEMENTATION_PLAN_PHASE2.md`
- `../skills/agentic-repo-layout/SKILL.md`
- `../skills/agentic-packaging-pypi/SKILL.md`
