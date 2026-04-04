"""Approval policy helpers for mutating and risky tools."""

from __future__ import annotations

from dataclasses import dataclass

from sentinel_cli.config import ToolExecutionSettings


DANGEROUS_SHELL_PATTERNS = ("rm -rf", "sudo ", "curl |", "wget |", "shutdown", "reboot")
SENSITIVE_FILE_PATTERNS = (".env", ".pem", ".key", ".token", "id_rsa", ".kube")


@dataclass(slots=True)
class ApprovalDecision:
    approved: bool
    reason: str


class ApprovalPolicy:
    """Interactive/auto approval gate aligned with Phase 2.A."""

    def __init__(self, settings: ToolExecutionSettings) -> None:
        self._settings = settings

    def decide(
        self,
        *,
        tool_name: str,
        interactive: bool,
        prompt: str,
        input_fn=input,
    ) -> ApprovalDecision:
        if self._settings.approval_mode == "deny":
            return ApprovalDecision(False, "Politika geregi bu arac kapali.")
        if self._settings.auto_approve or self._settings.approval_mode == "auto":
            return ApprovalDecision(True, "Otomatik onay aktif.")
        if not interactive:
            return ApprovalDecision(False, "Etkilesimsiz modda acik onay alinmadan riskli arac calismaz.")
        answer = input_fn(f"{prompt} [y/N]: ").strip().lower()
        return ApprovalDecision(answer in {"y", "yes"}, "Kullanici onayi")

    @staticmethod
    def classify_shell(command: str) -> str:
        lowered = command.lower()
        if any(pattern in lowered for pattern in DANGEROUS_SHELL_PATTERNS):
            return "shell-high"
        return "shell-low"

    @staticmethod
    def is_sensitive_path(path: str) -> bool:
        lowered = path.lower()
        return any(pattern in lowered for pattern in SENSITIVE_FILE_PATTERNS)
