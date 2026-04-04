# Changelog

Bu dosya [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) tarzına yakın tutulur; sürüm numarası `pyproject.toml` ile uyumlu olmalıdır.

## [Unreleased]

- Faz 3 iç kullanım teslimatı (paket doğrulama, dokümantasyon, politika) — `IMPLEMENTATION_PLAN_PHASE3.md`.
- `python -m build` ile wheel ve sdist üretimi doğrulandı; temiz smoke venv içinde wheel kurulumu ve `sentinel-cli --help` / `sentinel-cli version` çalıştırıldı.
- README, iç kullanım wheel kurulumu, Faz 3 indeks bağlantıları ve telemetri yok politikası ile güncellendi.
- `ENV_FLAGS_PHASE3.md` ve `scripts/smoke_wheel.sh` ile operasyon ve doğrulama akışı netleştirildi.

## [0.1.0] — Faz 2 kapanış

- İlk yayınlanabilir iskelet: agentic CLI (`run`, `repl`, `config`, `doctor`, `version`), katmanlı config, OpenAI uyumlu ve Anthropic yolları, araçlar, MCP (stdio), testler ve CI.
