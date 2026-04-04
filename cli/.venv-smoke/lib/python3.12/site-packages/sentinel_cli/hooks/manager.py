"""Pre/post tool hook execution."""

from __future__ import annotations

import fnmatch
import json
import subprocess
from dataclasses import dataclass
from typing import Any

from sentinel_cli.config import HookCommand, HooksSettings


@dataclass(slots=True)
class HookResult:
    blocked: bool = False
    message: str | None = None


class HookManager:
    """Run configured hooks around tool execution."""

    def __init__(self, settings: HooksSettings) -> None:
        self._settings = settings

    def _matching(self, phase: str, tool_name: str) -> list[HookCommand]:
        if not self._settings.enabled:
            return []
        return [
            hook
            for hook in self._settings.commands
            if hook.phase == phase and fnmatch.fnmatch(tool_name, hook.matcher)
        ]

    def run(self, phase: str, payload: dict[str, Any]) -> HookResult:
        tool_name = str(payload.get("tool_name", ""))
        for hook in self._matching(phase, tool_name):
            try:
                completed = subprocess.run(
                    hook.command,
                    input=json.dumps(payload, ensure_ascii=True),
                    text=True,
                    capture_output=True,
                    timeout=hook.timeout_sec,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                if hook.on_error == "block":
                    return HookResult(blocked=True, message=f"Hook engelledi: {exc}")
                return HookResult(blocked=False, message=f"Hook uyarisi: {exc}")
            if completed.returncode != 0 and hook.on_error == "block":
                return HookResult(
                    blocked=True,
                    message=f"Hook engelledi: exit={completed.returncode}",
                )
        return HookResult()
