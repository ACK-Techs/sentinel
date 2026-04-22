# Changelog

Bu dosya [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) tarzına yakın tutulur; sürüm numarası `pyproject.toml` ile uyumlu olmalıdır.

## [Unreleased]

- Observability gateway bearer auth zorunlu hale getirildi; gateway artik secret-safe `401` donuyor.
- CLI log sorgulari artik Loki sorgu dizgisi uretmiyor; `service` bilgisini gateway'e tasiyor.
- Tek aktif plan dokumani `OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md` oldu; eski faz plan/handoff/prompt belgeleri kaldirildi.
- `python -m build` ile wheel ve sdist üretimi doğrulandı; temiz smoke venv içinde wheel kurulumu ve `sentinel-cli --help` / `sentinel-cli version` çalıştırıldı.
- README, iç kullanım wheel kurulumu, Faz 3 indeks bağlantıları ve telemetri yok politikası ile güncellendi.
- `ENV_FLAGS_PHASE3.md` ve `scripts/smoke_wheel.sh` ile operasyon ve doğrulama akışı netleştirildi.

## [0.1.0] — Faz 2 kapanış

- İlk yayınlanabilir iskelet: agentic CLI (`run`, `repl`, `config`, `doctor`, `version`), katmanlı config, OpenAI uyumlu ve Anthropic yolları, araçlar, MCP (stdio), testler ve CI.
