"""Shell tool with timeout and output truncation."""

from __future__ import annotations

import re
import shlex
import subprocess

from pydantic import BaseModel, ConfigDict, Field

from sentinel_cli.tools.base import ToolContext, ToolResult

CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
_READ_ONLY_ALLOWED = frozenset(
    {"ls", "cat", "head", "tail", "grep", "find", "pwd", "echo", "wc", "stat", "sort", "uniq", "git"}
)


def _bash_read_only_blocks(command: str) -> str | None:
    stripped = command.strip()
    if not stripped:
        return "Bos komut."
    if any(symbol in stripped for symbol in (">", "`", "$(", "\n")):
        return "Yonlendirme veya komut substitution salt okunur modda engellendi."
    lowered = stripped.lower()
    if "|" in lowered or ";" in lowered:
        return "Pipe veya zincir komut salt okunur modda engellendi."
    try:
        parts = shlex.split(stripped)
    except ValueError:
        return "Komut ayrıştırılamadı."
    if not parts:
        return "Bos komut."
    binary = parts[0].split("/")[-1].lower()
    if binary not in _READ_ONLY_ALLOWED:
        return f"'{binary}' salt okunur izin listesinde degil."
    return None


class BashArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    command: str
    cwd: str | None = None
    timeout_sec: int | None = Field(default=None, ge=1, le=120)


class BashTool:
    name = "bash"
    description = "Kontrollu shell komutu calistirir."
    risk_level = "shell"
    args_model = BashArgs

    def __init__(self, *, default_timeout_sec: int, max_output_chars: int) -> None:
        self._default_timeout_sec = default_timeout_sec
        self._max_output_chars = max_output_chars

    def definition(self):
        from sentinel_cli.llm.types import ToolDefinition

        return ToolDefinition(
            name=self.name,
            description=self.description,
            input_schema=self.args_model.model_json_schema(),
        )

    def execute(self, arguments: BashArgs, context: ToolContext) -> ToolResult:
        cwd = arguments.cwd or context.cwd
        timeout = arguments.timeout_sec or self._default_timeout_sec
        try:
            completed = subprocess.run(
                arguments.command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(False, "TIMEOUT", f"Komut zaman asimina ugradi ({timeout}s).")
        except OSError as exc:
            return ToolResult(False, "EXEC_ERROR", f"Komut calistirilamadi: {exc}")

        output = (completed.stdout or "") + ("\n" + completed.stderr if completed.stderr else "")
        output = CONTROL_CHARS.sub("", output)
        truncated = False
        if len(output) > self._max_output_chars:
            output = output[: self._max_output_chars] + "\n...[truncated]..."
            truncated = True
        code = "OK" if completed.returncode == 0 else "EXIT_NONZERO"
        return ToolResult(
            completed.returncode == 0,
            code,
            output.strip() or "(no output)",
            data={"returncode": completed.returncode, "truncated": truncated},
        )
