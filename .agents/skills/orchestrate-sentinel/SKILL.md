---
name: orchestrate-sentinel
description: Manage and execute Sentinel CLI, observability-gateway, test-platform, installer, chart, and docs work through the repository's central .orchestrator run graph. Use for project planning, PM decomposition, architecture/contracts, implementation, review, verification, integration, resuming prior work, or coordinating Codex/Cursor/Claude agents. Enforces gateway read-only, install-path separation, evidence contracts, risk gates, and Git checkpoints.
---

# Orchestrate Sentinel

Use `.orchestrator` as the source of truth for non-trivial project work. Do not manage multi-step implementation only in conversation memory.

## Start

1. Read repository-root `README.md` and `INSTALL.md`.
2. Read `.orchestrator/PROJECT-STATE.md` and `.orchestrator/SYSTEM.md`.
3. Read `.orchestrator/COMMIT_CONVENTION.md` and the assigned role under `.orchestrator/roles/`.
4. Run `node .orchestrator/bin/orchestrator.mjs discover` when catalog is missing or repository structure changed.
5. Inspect active runs before creating a duplicate run.

For module and capability selection, read [module-routing.md](references/module-routing.md). For reusable graph shapes, read [run-patterns.md](references/run-patterns.md).

## Choose workflow

### Answer, audit, or design only

Use a read-only `analysis`, `specification`, `architecture-review`, or `pm-planning` item. Do not infer implementation authorization.

### Build or change

Create or resume a run. Apply contract-first ordering:

```text
PM scope -> architecture/contract -> implement -> review -> verify -> integration -> PM acceptance
```

Add independent review and verification for every item required by `.orchestrator/config.json` risk policy.

### Diagnose

Create read-only discovery/reproduction items first. Do not add a fix item unless the request includes fixing or the user later authorizes it.

### Resume

Run `validate`, `status`, then inspect `events.jsonl` and `results/`. Reconcile stale `active` ownership before redispatch.

## PM Manager protocol

- Preserve the complete approved scope; never collapse Compose, Kubernetes, and COS into one installer story.
- Keep the observability gateway read-only unless the user explicitly approves `gateway-write-expansion`.
- Treat `agentic/` as reference code, not product source.
- Assign role, capabilities, write scopes, risks, approvals, outputs, and exact acceptance to every item.
- Keep architecture, implementation, review, verification, and integration ownership separate.
- Record durable decisions in `run.decisions`, not only prose.
- Create revision items; never rewrite failed history.
- Do not mark completion until accepted integration and documentation synchronization exist.

## Dispatch protocol

1. Run `sync` and `status`.
2. Select the first safe batch.
3. Prefer native subagents for bounded independent items when available.
4. Use worktrees for parallel writers when supported; otherwise serialize.
5. Render a platform handoff when native delegation is unavailable:

```bash
node .orchestrator/bin/orchestrator.mjs render <run.json> <item-id> --platform cursor
```

6. Require `.orchestrator/contracts/result.schema.json` output.
7. Record accepted attempt with `record`; do not manually set `done`.
8. After a write item passes its checks, record one atomic Conventional Commit with `type(scope): summary`. `Work-Item` and `Phase` footers are optional.
9. If the commit message is valid, `git push` is allowed. Never force-push and never use `scripts/auto-push-watch.sh`.

## Role routing

- `pm-planning`, backlog, scope, acceptance: `roles/pm-manager.md`
- architecture, ADR, schema, module boundary: `roles/architecture-manager.md`
- code/config/test/docs mutation: `roles/code-implementer.md`
- independent diff/contract review: `roles/independent-reviewer.md`
- test execution: `roles/verifier.md`
- secret/token/approval/gateway-auth: `roles/security-data-reviewer.md`
- accepted cross-module assembly: `roles/integration-manager.md`

## Non-negotiable product invariants

- Gateway stays read-only; no alert, dashboard, backend write, or Grafana proxy without approval.
- CLI talks to Prometheus/Loki/Tempo only through the gateway.
- Secrets stay in environment variables, not committed YAML.
- Compose, Kubernetes, and COS install paths stay distinct; COS installer is not complete.
- `agentic/` is reference, not the shipped product.
- Tool approval, timeouts, and redaction are not silently disabled.
- Do not claim a check ran when it did not.

## Completion

Return the outcome, accepted artifacts, executed checks, commit SHA, remaining risks, and next graph state. Read-only items do not create empty commits. Valid Conventional Commit messages may be pushed with `git push`; never force-push.
