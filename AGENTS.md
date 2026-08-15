# Project Agent Instructions

This repository builds Sentinel: an agentic Python CLI, a read-only observability gateway, and a lab test platform.

For non-trivial planning, architecture, implementation, review, verification, integration, or resume work, use `.agents/skills/orchestrate-sentinel/SKILL.md` and the `.orchestrator` control plane.

Read in order: `README.md`, `INSTALL.md`, `.orchestrator/SYSTEM.md`, active run and assigned role.

- Do not reduce approved scope for speed.
- Keep `observability-gateway` read-only unless the user explicitly approves a write expansion.
- Keep Compose, Kubernetes, and COS install paths distinct; do not claim the COS installer is complete.
- Treat `agentic/` as reference code, not the shipped product.
- Use contract-first dependency graphs.
- Implementers only edit assigned write scopes. Completed write items use an atomic Conventional Commit `type(scope): summary`. `Work-Item` and `Phase` footers are optional.
- If the commit message is valid, `git add`, `git commit`, and `git push` are allowed. Force-push is forbidden. Do not use `scripts/auto-push-watch.sh` for orchestrated work.
- High-risk work requires independent review and verification.
- Conversation memory is not completion evidence; run/result artifacts are.
- Preserve user changes and unrelated dirty-worktree content.
