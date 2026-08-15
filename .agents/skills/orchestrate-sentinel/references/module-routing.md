# Module and capability routing

- CLI runtime: read `cli/README.md` and `cli/documantations/ARCHITECTURE_AGENTIC_CLI.md`; commands, agent loop, LLM adapters, tools, session, memory, config.
- Observability gateway: read `observability-gateway/README.md` and `cli/documantations/OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md`; Prometheus/Loki/Tempo, bearer token, secret-safe errors. Keep read-only.
- Test platform: read `test-platform/README.md`; gateway/orders/payments/inventory/worker, load, chaos, smoke scripts.
- Installers: read `INSTALL.md` and `cli/src/sentinel_cli/installers/`; Compose, Kubernetes Helm, COS discovery. Do not claim COS install is complete.
- Charts: read `charts/sentinel/README.md`; Helm values, gateway deployment, pod security.
- Ops lab: `scripts/` and `for-download/`; MicroK8s, Juju, COS Lite helpers.
- Skills/docs: `skills/`, `cli/skills/`, `documantations/`, `INSTALL.md`.
- Security: tokens, redaction, tool approval, prompt injection, Helm security context.
- CI: `.github/workflows/cli-ci.yml` and `gateway-image.yml`.
