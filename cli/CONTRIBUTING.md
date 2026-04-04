# Sentinel CLI — katkı / geliştirici notları

Kök dizin: `sentinel-coming/cli/`. Bu depo parçası **iç kullanım** odaklıdır; Faz 3 teslimatı `documantations/IMPLEMENTATION_PLAN_PHASE3.md` ile hizalanır.

## Ortam

```bash
cd sentinel-coming/cli
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

MCP ile geliştirme:

```bash
python -m pip install -e ".[dev,mcp]"
```

Wheel/sdist üretimi (Faz 3): `python -m build` — `build` paketi `[dev]` extra ile gelir.

Bağımlılık güncellerken önce küçük uyumlu aralık değişimlerini tercih edin. Yeni major sürümler, yeni ağır bağımlılıklar veya mevcut üst sınırların gevşetilmesi; `ruff`, `pytest`, wheel smoke ve CI etkisi birlikte görülmeden doğrudan birleştirilmemelidir.

## Kalite çubuğu (PR öncesi)

```bash
cd sentinel-coming/cli
source .venv/bin/activate
python -m ruff check .
python -m pytest -q
```

İsteğe bağlı: `python -m ruff format .` (projede format zorunluluğu yoksa bile tutarlılık için kullanılabilir).

## Sırlar

Gerçek API anahtarlarını repoya veya örnek dosyalara yazmayın. Ortam değişkenleri ve `.env.example` placeholder’ları `LLM_PROVIDERS.md` ile uyumludur.

## İlgili belgeler

- `documantations/IMPLEMENTATION_PLAN_PHASE2.md` — Faz 2 teslimatı
- `documantations/IMPLEMENTATION_PLAN_PHASE3.md` — Faz 3 görevleri
- `documantations/ARCHITECTURE_AGENTIC_CLI.md` — mimari özet
- `skills/agentic-docs-developer-checklist/SKILL.md` — kontrol listesi şartnamesi
