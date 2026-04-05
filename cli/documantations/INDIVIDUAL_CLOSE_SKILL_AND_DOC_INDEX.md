# Bireysel kapanış — indeks (Grafana ↔ REPL)

| Dosya | Rol |
|-------|-----|
| `GRAFANA_AI_PLATFORM_RESEARCH.md` | Grafana’nın LLM/Assistant vs HTTP API ayrımı |
| `IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md` | Kod + test + doküman kapıları |
| `CODEX_EXECUTION_PROMPT_INDIVIDUAL_CLOSE.md` | Yürütücü AI tek mesaj prompt’u |

## Skill’ler (`cli/skills/`)

| Skill | Rol |
|-------|-----|
| `agentic-grafana-llm-platform-overview` | Grafana Labs LLM ürünleri özeti; Sentinel sınırı |
| `agentic-sentinel-grafana-agent-bridge` | REPL bağlam köprüsü tasarımı ve uygulama sırası |

## Cursor yürütücü

| Dosya | Rol |
|-------|-----|
| `.cursor/skills/sentinel-individual-close-executor/SKILL.md` | Kod yazan ajan talimatı |

## Yerel doğrulama

| Dosya | Rol |
|-------|-----|
| `scripts/verify_grafana_context_repl.sh` | 7 adımlı sıralı test (pytest + `run` + bayrak kapalı); `STEP_PAUSE=1` ile adımlar arası duraklatma |
