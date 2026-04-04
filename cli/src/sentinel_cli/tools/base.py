"""Base contracts for built-in and optional tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from pydantic import BaseModel

from sentinel_cli.llm.types import ToolDefinition


@dataclass(slots=True)
class ToolContext:
    cwd: str
    session_id: str
    interactive: bool
    auto_approve: bool


@dataclass(slots=True)
class ToolResult:
    ok: bool
    code: str
    message: str
    data: dict[str, Any] | None = None


class SentinelTool(Protocol):
    name: str
    description: str
    risk_level: str
    args_model: type[BaseModel]

    def definition(self) -> ToolDefinition:
        ...

    def execute(self, arguments: BaseModel, context: ToolContext) -> ToolResult:
        ...
