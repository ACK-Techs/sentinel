# Sentinel Coming

Sentinel Coming is a portfolio-grade observability and infrastructure automation project built around an agentic Python CLI, a read-only observability gateway, and a realistic multi-service test platform. It is designed for local labs and Kubernetes/COS-style environments where operators need a safer way to inspect metrics, logs, traces, configuration, and deployment state from one terminal workflow.

The core product is `sentinel-cli`: a Python command-line assistant that can run one-off prompts, start a REPL, inspect configuration, run health checks, install local observability stacks, and query a gateway-backed telemetry layer. The gateway keeps Prometheus, Loki, and Tempo access behind one read-only HTTP API so the CLI does not need to know every backend URL directly.

## Problem and Goals

Modern observability stacks are powerful but operationally fragmented. A developer or platform engineer often has to switch between Grafana, Prometheus, Loki, Tempo, shell commands, Kubernetes tooling, and runbooks just to understand whether a service is healthy.

This project explores a practical answer to that workflow:

- Provide a single CLI surface for agent-assisted infrastructure and observability work.
- Keep telemetry access read-only by default through a gateway service.
- Support local and cloud LLM providers through a layered configuration model.
- Preserve useful debugging context through sessions, trajectories, memory extraction, and controlled documentation updates.
- Validate the workflow against a realistic target platform with services, databases, Redis Streams, load generation, chaos profiles, Kubernetes manifests, and smoke scripts.

## Key Features

- Agentic CLI with `run`, `repl`, `config`, `doctor`, `obs`, `install`, and `version` commands.
- LLM provider support for OpenAI-compatible APIs and Anthropic, including local OpenAI-compatible endpoints such as Ollama.
- Optional MCP client integration via the `mcp` extra.
- Layered configuration from defaults, YAML files, environment variables, and CLI flags.
- Tool execution controls for bash, filesystem access, approval modes, timeouts, output limits, and read-only bash mode.
- Session persistence, trajectory recording, context-window policy, and optional turn-end memory processing.
- Read-only FastAPI observability gateway for Prometheus metrics, Loki log queries, and Tempo trace search/detail calls.
- Gateway-backed CLI observability commands: `obs metric`, `obs logs`, and `obs traces`.
- Docker Compose installer assets and Kubernetes Helm chart assets for the Sentinel observability stack.
- Test platform with gateway, orders, payments, inventory, worker services, Postgres, Redis, OpenTelemetry Collector, Locust load scenarios, chaos profiles, and Kubernetes manifests.
- CI for the CLI package using GitHub Actions, Ruff, and Pytest.
- Gateway image workflow for multi-architecture GHCR builds.

## Architecture

```text
User
  |
  v
sentinel-cli
  |-- LLM provider adapters
  |-- tool registry: bash, filesystem, MCP, observability tools
  |-- session, trajectory, hooks, memory, and config layers
  |
  v
observability-gateway
  |-- Prometheus: instant metric queries
  |-- Loki: query_range log retrieval
  |-- Tempo: trace search and trace detail retrieval
  |
  v
Target platform and observability backends
```

The repository also includes deployment paths for different environments:

- `for-download/compose/` contains a Docker Compose observability stack with Prometheus, Loki, Tempo, Grafana, and the Sentinel gateway image.
- `charts/sentinel/` contains a Helm chart that installs kube-prometheus-stack, Loki, Tempo, Grafana, and `sentinel-gateway` into an existing Kubernetes cluster.
- `test-platform/` contains a realistic target application tree used to generate metrics, logs, and traces for the Sentinel workflow.
- `skills/` and `cli/skills/` contain structured operational and agentic guidance files used as project knowledge and implementation references.

## Tech Stack

- Python 3.11+ for the CLI, gateway, and test services.
- FastAPI and Uvicorn for HTTP services.
- Pydantic and pydantic-settings for typed configuration and request/response models.
- HTTPX for outbound API and backend calls.
- PyYAML and python-dotenv for configuration files and environment loading.
- Rich for CLI output and progress rendering.
- Pytest and Ruff for test and lint workflows.
- Docker Compose for local observability and target-platform runs.
- Helm and Kubernetes manifests for cluster deployment paths.
- Prometheus, Loki, Tempo, Grafana, OpenTelemetry Collector, Postgres, Redis, and Locust in the supporting lab platform.

## Repository Layout

```text
sentinel-coming/
|-- cli/                         # Sentinel CLI Python package
|-- observability-gateway/       # Read-only FastAPI gateway for telemetry backends
|-- test-platform/               # Multi-service target app, load, chaos, and smoke scripts
|-- charts/sentinel/             # Helm chart for Kubernetes observability stack
|-- for-download/                # Compose bundle and operational setup scripts
|-- scripts/                     # MicroK8s/COS helper scripts and repo automation
|-- skills/                      # COS/Juju/MicroK8s operational skill documents
|-- documantations/              # Project and phase documentation
|-- .github/workflows/           # CLI CI and gateway image workflows
`-- agentic/                     # External/reference agent projects, not the main product
```

Important note: `agentic/` contains independent reference projects. The main Sentinel implementation is in `cli/`, `observability-gateway/`, `test-platform/`, `charts/`, `for-download/`, `scripts/`, `skills/`, and `documantations/`.

## Main Modules

### `cli/`

`cli/` is the main user-facing package. Its source code lives under `cli/src/sentinel_cli/`.

Key areas:

- `cli/app.py`: argparse command surface and runtime wiring.
- `agent/`: agent loop, context compaction, and turn-end processing.
- `llm/`: provider factory, Anthropic adapter, OpenAI-compatible adapter, streaming, retries, and shared types.
- `tools/`: bash, filesystem, MCP, approval, registry, and observability tools.
- `observability/`: gateway and Grafana connection checks.
- `config/`: Pydantic configuration models and layered loader.
- `memory/`: extraction, dreaming, magic docs, memory path handling, and redaction-aware persistence.
- `session/`: session store and trajectory recording.
- `installers/`: Docker Compose, Kubernetes Helm, and COS discovery/install backends.
- `assets/`: packaged Compose and Helm chart assets used by the install command.

### `observability-gateway/`

`observability-gateway/` is a standalone FastAPI service. It exposes a small read-only API and adapts requests to Prometheus, Loki, and Tempo.

Endpoints:

- `GET /health`
- `GET /api/v1/status`
- `POST /api/v1/metrics/query`
- `POST /api/v1/logs/query_range`
- `POST /api/v1/traces/search`
- `GET /api/v1/traces/{trace_id}`

The gateway supports bearer-token protection through `SENTINEL_OBSERVABILITY_GATEWAY_TOKEN` when that token is configured. Backend errors are returned through a structured model that avoids leaking secrets.

### `test-platform/`

`test-platform/` provides a target application for realistic observability tests:

- `gateway`: public API facade.
- `orders`: coordinates payments and inventory, writes to Postgres, and emits Redis Stream events.
- `payments`: payment simulation with Redis idempotency.
- `inventory`: stock reads/reservations with Redis cache-through behavior.
- `worker`: Redis Streams consumer group processor.
- `load/`: Locust scenarios including steady, diurnal, flash crowd, and gradual degradation.
- `chaos/profiles/`: healthy, slow database, cache stampede, downstream outage, memory leak, and cascading profiles.
- `k8s/`: namespace, services, deployments/stateful resources, OpenTelemetry Collector config, and network policy manifests.

### `charts/sentinel/`

The Helm chart installs Prometheus, Loki, Grafana, Tempo, and the Sentinel gateway into an existing Kubernetes cluster. The chart uses upstream dependencies from the Prometheus Community and Grafana Helm repositories and keeps service names aligned with the CLI discovery code.

### `for-download/`

This folder contains deployment-oriented assets:

- `compose/docker-compose.yaml`: local observability stack.
- `compose/.env.example`: ports and gateway token defaults for the compose stack.
- `prepare-env.sh`: MicroK8s, MetalLB, and Juju preparation helper.
- `my-product-bundle.yaml`: COS Lite bundle including Prometheus, Loki, Alertmanager, Grafana, Traefik, Catalogue, Tempo, and OpenTelemetry Collector.
- `faz1-telemetry.sh` and `faz4-5.sh`: operational scripts for telemetry setup and post-deployment checks.

## Setup

Clone the repository and create a virtual environment:

```bash
cd sentinel-coming
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install the CLI for local development:

```bash
cd cli
python -m pip install -e ".[dev]"
python -m sentinel_cli --help
```

Install the CLI with optional MCP support:

```bash
cd cli
python -m pip install -e ".[dev,mcp]"
python -m sentinel_cli doctor --profile local
```

Install and run the observability gateway locally:

```bash
cd observability-gateway
python -m pip install -e ".[dev]"
sentinel-observability-gateway
```

Alternative gateway startup:

```bash
cd observability-gateway
uvicorn observability_gateway.main:app --host 0.0.0.0 --port 8091
```

## Configuration

The CLI keeps committed templates separate from local secrets:

- `cli/config/sentinel.example.yaml`: committed YAML template.
- `cli/.env.example`: committed environment template.
- `cli/config/sentinel.yaml`: local runtime config, ignored by Git.
- `cli/.env`: local secrets and overrides, ignored by Git.

Create local configuration:

```bash
cd cli
cp config/sentinel.example.yaml config/sentinel.yaml
cp .env.example .env
```

Common CLI environment variables from `cli/.env.example`:

- `SENTINEL_CONFIG`
- `SENTINEL_PROFILE`
- `SENTINEL_MODEL`
- `SENTINEL_OPENAI_BASE_URL`
- `SENTINEL_API_KEY`
- `SENTINEL_LOCAL_BASE_URL`
- `SENTINEL_LOCAL_MODEL`
- `ANTHROPIC_API_KEY`
- `SENTINEL_ANTHROPIC_MODEL`
- `SENTINEL_HTTP_CONNECT_TIMEOUT_SEC`
- `SENTINEL_HTTP_TIMEOUT_SEC`
- `SENTINEL_CONTEXT_WINDOW_TOKENS`
- `SENTINEL_LOG_LEVEL`
- `SENTINEL_MAX_TURNS`
- `SENTINEL_AUTO_APPROVE`
- `SENTINEL_SESSION_DIR`
- `SENTINEL_TRAJECTORY_DIR`
- `SENTINEL_EXPERIMENTAL_MCP`

Gateway-related CLI settings are configured under `observability_gateway` in `sentinel.yaml`:

```yaml
observability_gateway:
  enabled: true
  base_url: http://127.0.0.1:8091
  timeout_sec: 10
  token_env: SENTINEL_OBSERVABILITY_GATEWAY_TOKEN
```

Gateway service environment variables documented in `observability-gateway/README.md` include:

- `SENTINEL_OBSERVABILITY_CONFIG_PATH`
- `SENTINEL_OBSERVABILITY_GATEWAY_TOKEN`
- `SENTINEL_OBSERVABILITY_PROMETHEUS__BASE_URL`
- `SENTINEL_OBSERVABILITY_PROMETHEUS__TOKEN_ENV`
- `SENTINEL_OBSERVABILITY_LOKI__BASE_URL`
- `SENTINEL_OBSERVABILITY_TEMPO__BASE_URL`
- `SENTINEL_OBSERVABILITY_HTTP__TIMEOUT_SEC`
- `SENTINEL_OBSERVABILITY_HTTP__RETRY__MAX_ATTEMPTS`

The compose package in `for-download/compose/.env.example` also defines ports for Prometheus, Loki, Tempo, Grafana, and the Sentinel gateway.

## Usage

Run a one-off agent prompt:

```bash
cd cli
source .venv/bin/activate
python -m sentinel_cli run "Summarize the current observability gateway status"
```

Start an interactive REPL:

```bash
cd cli
source .venv/bin/activate
python -m sentinel_cli repl
```

Inspect effective configuration:

```bash
cd cli
python -m sentinel_cli config
```

Run diagnostics:

```bash
cd cli
python -m sentinel_cli doctor --profile local
```

Query telemetry through the gateway:

```bash
cd cli
python -m sentinel_cli obs metric 'up'
python -m sentinel_cli obs logs --service gateway
python -m sentinel_cli obs traces --service orders
```

Run a Compose install flow:

```bash
cd cli
python -m sentinel_cli install --mode compose
```

Run a Kubernetes Helm install flow:

```bash
cd cli
python -m sentinel_cli install --mode k8s
```

The `cos` install backend currently includes discovery/config wiring, while its preflight, install, and verify steps are marked as TODO in code. Use the scripts under `scripts/` and `for-download/` for the existing MicroK8s/Juju/COS operational path.

## Local Target Platform

The test platform can be started with Docker Compose:

```bash
cd test-platform
docker compose up --build
```

The `test-platform/README.md` documents the local database environment variables and health checks:

```bash
export ORDERS_DB_URL=postgresql+asyncpg://sentinel:sentinel@localhost:5432/orders_db
export PAYMENTS_DB_URL=postgresql+asyncpg://sentinel:sentinel@localhost:5432/payments_db
export INVENTORY_DB_URL=postgresql+asyncpg://sentinel:sentinel@localhost:5432/inventory_db
export PAYMENTS_REDIS_URL=redis://localhost:6379/1
python scripts/seed_db.py
curl http://localhost:8080/health
curl http://localhost:8081/health
curl http://localhost:8082/health
curl http://localhost:8083/health
```

Run a ground-truth scenario:

```bash
cd test-platform
python scripts/scenario_runner.py run <scenario.yaml>
```

Run the COS smoke workflow when a compatible MicroK8s/Juju/COS lab is already available:

```bash
cd test-platform
./scripts/run_cos_stack_check.sh
```

Run the local stack smoke workflow:

```bash
cd test-platform
./scripts/run_local_stack_check.sh
```

These smoke scripts expect the repository-level `.venv` and required local infrastructure commands to exist. They write run artifacts under `test-platform/runs/...`.

## Testing and Quality

CLI lint and tests:

```bash
cd cli
python -m ruff check .
python -m pytest -q
```

Gateway tests:

```bash
cd observability-gateway
python -m pytest -q
```

Build a CLI wheel:

```bash
cd cli
python -m build
```

Build a gateway wheel:

```bash
cd observability-gateway
python -m build
```

The GitHub Actions workflow `.github/workflows/cli-ci.yml` runs the CLI package on Python 3.12 with editable dev installation, Ruff, and Pytest. The `.github/workflows/gateway-image.yml` workflow builds and pushes the gateway image to GHCR for `gateway-v*` tags or manual dispatch.

## Deployment Options

Docker image for the gateway:

```bash
docker pull ghcr.io/caglarkc/sentinel-gateway:latest
```

Helm chart:

```bash
helm dependency update ./charts/sentinel
helm upgrade --install sentinel ./charts/sentinel \
  --create-namespace -n sentinel \
  --set gateway.token=<token>
```

Local/lab Compose stack assets are available under `for-download/compose/` and packaged into the CLI install assets.

## Security and Reliability Notes

- The observability gateway is intentionally read-only; it does not implement alert management, dashboard management, backend write operations, or a Grafana datasource proxy.
- Gateway bearer authentication is enabled when `SENTINEL_OBSERVABILITY_GATEWAY_TOKEN` is configured.
- Gateway backend errors use a structured response model with retryability metadata and secret-safe messages.
- CLI configuration templates keep secrets in environment variables instead of committed config files.
- `.gitignore` excludes `.env`, local Sentinel sessions, credentials, key material, build artifacts, caches, logs, and local run outputs.
- CLI tools include approval modes, shell and file write timeouts, output limits, optional read-only bash behavior, and an optional memory write jail.
- Memory writes pass through redaction logic for common secret patterns before persistence.
- The gateway Dockerfile runs the service as a non-root `sentinel` user.
- The Helm chart sets non-root pod security context, disables privilege escalation, drops Linux capabilities, and uses a read-only root filesystem for the gateway container.

## Current Limitations

- The project is marked `Pre-Alpha` in the CLI package metadata.
- The `cos` installer backend is not a full installer yet; code marks preflight, install, and verify as TODO.
- Production hardening such as TLS termination, process supervision, and secret rotation is documented as outside the current gateway README scope.
- No screenshots or UI assets were found in the main Sentinel project tree during README preparation.
- `agentic/` contains external/reference projects and should not be presented as the shipped Sentinel product.

## Future Improvements

- Complete the COS installer backend so MicroK8s/Juju/COS setup can be driven consistently from the CLI.
- Add a production deployment guide covering TLS, ingress, secret rotation, and process supervision.
- Expand end-to-end tests around the gateway-backed agent `run` and `repl` workflows.
- Add example scenario files for `scenario_runner.py` in a discoverable location.
- Publish architecture diagrams and generated screenshots or conceptual visuals for portfolio presentation.
- Add a concise public quickstart that separates local demo, Kubernetes demo, and COS lab paths.

## License

MIT License - Copyright (c) 2026 Ali Caglar Kocer
