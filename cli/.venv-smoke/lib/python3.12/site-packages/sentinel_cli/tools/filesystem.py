"""Filesystem read/write tools with repo-root jail."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from sentinel_cli.tools.base import ToolContext, ToolResult


def _sanitize_text(text: str, *, limit: int) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    return text[:limit] + "\n...[truncated]...", True


def _resolve_within_root(root: Path, requested: str, *, must_exist: bool) -> Path:
    candidate = (root / requested).resolve()
    if not str(candidate).startswith(str(root.resolve())):
        raise PermissionError("Istenen path repo kokunun disina cikiyor.")
    if must_exist and not candidate.exists():
        raise FileNotFoundError(str(candidate))
    return candidate


class ReadFileArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    max_chars: int = Field(default=4000, ge=1, le=20000)


class WriteFileArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    content: str
    create_dirs: bool = False


class ReadFileTool:
    name = "read_file"
    description = "Repo kokune gore bir metin dosyasini okur."
    risk_level = "read-safe"
    args_model = ReadFileArgs

    def definition(self):
        from sentinel_cli.llm.types import ToolDefinition

        return ToolDefinition(
            name=self.name,
            description=self.description,
            input_schema=self.args_model.model_json_schema(),
        )

    def execute(self, arguments: ReadFileArgs, context: ToolContext) -> ToolResult:
        root = Path(context.cwd).resolve()
        try:
            path = _resolve_within_root(root, arguments.path, must_exist=True)
            if path.is_dir():
                return ToolResult(False, "IS_DIR", "Dizin yerine dosya bekleniyordu.")
            data = path.read_bytes()
            if b"\x00" in data:
                return ToolResult(False, "BINARY_FILE", f"Binary dosya atlandi: {path}")
            text = data.decode("utf-8", errors="replace")
            text, truncated = _sanitize_text(text, limit=arguments.max_chars)
            return ToolResult(
                True,
                "OK",
                f"{path}",
                data={"content": text, "truncated": truncated},
            )
        except FileNotFoundError:
            return ToolResult(False, "ENOENT", f"Dosya bulunamadi: {arguments.path}")
        except PermissionError as exc:
            return ToolResult(False, "PATH_ESCAPE", str(exc))
        except OSError as exc:
            return ToolResult(False, "READ_ERROR", f"Dosya okunamadi: {exc}")


class WriteFileTool:
    name = "write_file"
    description = "Repo kokune gore bir metin dosyasina atomik sekilde yazar."
    risk_level = "write-controlled"
    args_model = WriteFileArgs

    def definition(self):
        from sentinel_cli.llm.types import ToolDefinition

        return ToolDefinition(
            name=self.name,
            description=self.description,
            input_schema=self.args_model.model_json_schema(),
        )

    def execute(self, arguments: WriteFileArgs, context: ToolContext) -> ToolResult:
        root = Path(context.cwd).resolve()
        try:
            path = _resolve_within_root(root, arguments.path, must_exist=False)
            if ".git" in path.parts:
                return ToolResult(False, "GIT_PROTECTED", ".git altina yazma varsayilan olarak engellendi.")
            if arguments.create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)
            elif not path.parent.exists():
                return ToolResult(False, "MISSING_PARENT", f"Ust dizin yok: {path.parent}")
            fd, temp_name = tempfile.mkstemp(dir=str(path.parent), prefix=".sentinel-", text=True)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(arguments.content)
                os.replace(temp_name, path)
            finally:
                if os.path.exists(temp_name):
                    os.unlink(temp_name)
            return ToolResult(True, "OK", f"Dosya yazildi: {path}", data={"bytes": len(arguments.content.encode('utf-8'))})
        except PermissionError as exc:
            return ToolResult(False, "PATH_ESCAPE", str(exc))
        except OSError as exc:
            return ToolResult(False, "WRITE_ERROR", f"Dosya yazilamadi: {exc}")
