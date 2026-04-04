"""Tool registry, parsing, and execution pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from sentinel_cli.config import AppConfig
from sentinel_cli.hooks import HookManager
from sentinel_cli.llm.types import ToolCall, ToolDefinition
from sentinel_cli.tools.approval import ApprovalPolicy
from sentinel_cli.tools.base import SentinelTool, ToolContext, ToolResult
from sentinel_cli.tools.bash import BashTool
from sentinel_cli.tools.filesystem import ReadFileTool, WriteFileTool


@dataclass(slots=True)
class ParsedToolCall:
    tool: SentinelTool
    arguments: Any


class ToolRegistry:
    """Built-in tools plus optional MCP discovery metadata."""

    def __init__(
        self,
        *,
        config: AppConfig,
        hook_manager: HookManager | None = None,
        prompt_input=input,
    ) -> None:
        self._config = config
        self._hook_manager = hook_manager or HookManager(config.hooks)
        self._approval = ApprovalPolicy(config.tools)
        self._prompt_input = prompt_input
        self._tools: dict[str, SentinelTool] = {
            "bash": BashTool(
                default_timeout_sec=config.tools.shell_timeout_sec,
                max_output_chars=config.tools.max_output_chars,
            ),
            "read_file": ReadFileTool(),
            "write_file": WriteFileTool(),
        }

    def definitions(self) -> list[ToolDefinition]:
        return [tool.definition() for tool in self._tools.values()]

    def parse_tool_call(self, tool_call: ToolCall) -> ParsedToolCall:
        tool = self._tools.get(tool_call.name)
        if tool is None:
            raise ValueError(f"Bilinmeyen tool: {tool_call.name}")
        try:
            payload = json.loads(tool_call.arguments_json or "{}")
        except json.JSONDecodeError as exc:
            raise ValueError(f"Tool argumani gecerli JSON degil: {exc}") from exc
        try:
            parsed = tool.args_model.model_validate(payload)
        except ValidationError as exc:
            raise ValueError(f"Tool argumani semaya uymuyor: {exc}") from exc
        return ParsedToolCall(tool=tool, arguments=parsed)

    def execute_tool_call(
        self,
        tool_call: ToolCall,
        *,
        cwd: str,
        session_id: str,
        interactive: bool,
    ) -> ToolResult:
        parsed = self.parse_tool_call(tool_call)
        prompt = f"{parsed.tool.name} araci calistirilsin mi?"
        decision = self._approval.decide(
            tool_name=parsed.tool.name,
            interactive=interactive,
            prompt=prompt,
            input_fn=self._prompt_input,
        )
        if not decision.approved and parsed.tool.name in {"bash", "write_file"}:
            return ToolResult(False, "APPROVAL_DENIED", decision.reason)

        hook_payload = {
            "session_id": session_id,
            "cwd": cwd,
            "tool_name": parsed.tool.name,
            "tool_input": parsed.arguments.model_dump(mode="json"),
        }
        pre = self._hook_manager.run("pre_tool", hook_payload)
        if pre.blocked:
            return ToolResult(False, "HOOK_BLOCKED", pre.message or "Pre hook engelledi.")

        result = parsed.tool.execute(
            parsed.arguments,
            ToolContext(
                cwd=cwd,
                session_id=session_id,
                interactive=interactive,
                auto_approve=self._config.tools.auto_approve,
            ),
        )
        self._hook_manager.run(
            "post_tool",
            {
                **hook_payload,
                "tool_response": {
                    "ok": result.ok,
                    "code": result.code,
                    "message": result.message,
                },
            },
        )
        return result
