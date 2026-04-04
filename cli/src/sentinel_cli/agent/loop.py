"""Agent turn loop for Phase 2.C."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from sentinel_cli.config import AppConfig, ResolvedProfile
from sentinel_cli.hooks import HookManager
from sentinel_cli.llm.errors import LLMError
from sentinel_cli.llm.types import ChatMessage, ChatRequest, CompletionResult, MessageRole, ToolCall
from sentinel_cli.session import SessionState, SessionStore, TrajectoryRecorder
from sentinel_cli.tools import ToolRegistry

from sentinel_cli.agent.compaction import HistoryCompactor


@dataclass(slots=True)
class AgentRunResult:
    output_text: str
    turns_used: int
    stopped_reason: str
    session_id: str
    warnings: list[str]


class AgentLoop:
    """Minimal single-agent turn loop with tool execution."""

    def __init__(
        self,
        *,
        config: AppConfig,
        resolved_profile: ResolvedProfile,
        provider: Any,
        session_store: SessionStore,
        trajectory: TrajectoryRecorder,
        hook_manager: HookManager | None = None,
        prompt_input=input,
    ) -> None:
        self._config = config
        self._profile = resolved_profile
        self._provider = provider
        self._session_store = session_store
        self._trajectory = trajectory
        self._registry = ToolRegistry(config=config, hook_manager=hook_manager, prompt_input=prompt_input)
        self._compactor = HistoryCompactor(config)

    def _tool_result_message(self, tool_call: ToolCall, result: Any) -> ChatMessage:
        return ChatMessage(
            role=MessageRole.TOOL,
            tool_call_id=tool_call.id,
            content=json.dumps(
                {
                    "ok": result.ok,
                    "code": result.code,
                    "message": result.message,
                    "data": result.data,
                },
                ensure_ascii=True,
            ),
        )

    def _request(self, messages: list[ChatMessage]) -> ChatRequest:
        return ChatRequest(
            messages=messages,
            system_prompt=self._config.agent.system_prompt,
            tools=self._registry.definitions() if self._profile.supports_tools else [],
        )

    def run(
        self,
        *,
        prompt: str,
        cwd: str,
        interactive: bool,
        session_id: str | None = None,
        resume: bool = False,
    ) -> AgentRunResult:
        warnings: list[str] = []
        if session_id and resume:
            try:
                session = self._session_store.load(session_id)
            except FileNotFoundError:
                session = self._session_store.create(profile=self._profile.name, provider=self._profile.provider)
                warnings.append("Istenen oturum bulunamadi; yeni oturum acildi.")
        else:
            session = self._session_store.create(profile=self._profile.name, provider=self._profile.provider)

        if session.profile != self._profile.name or session.provider != self._profile.provider:
            warnings.append(
                "Profil veya saglayici degisti. Eski gecmis yeni provider ile uyumsuz olabilir; yeni oturum onerilir."
            )
            session = self._session_store.create(profile=self._profile.name, provider=self._profile.provider)

        session.messages = self._compactor.compact(session.messages)
        session.messages.append(ChatMessage(role=MessageRole.USER, content=prompt))
        self._session_store.save(session)
        self._trajectory.append(
            session.session_id,
            {"event": "user_prompt", "profile": self._profile.name, "content": prompt},
        )

        repeated_calls: dict[tuple[str, str], int] = {}

        for turn in range(1, self._config.agent.max_turns + 1):
            request = self._request(session.messages)
            try:
                result: CompletionResult = self._provider.complete(request)
            except KeyboardInterrupt:
                return AgentRunResult(
                    output_text="Islem kullanici tarafindan iptal edildi.",
                    turns_used=turn,
                    stopped_reason="interrupted",
                    session_id=session.session_id,
                    warnings=warnings,
                )
            except LLMError as exc:
                raise

            if result.text:
                session.messages.append(ChatMessage(role=MessageRole.ASSISTANT, content=result.text))
                self._trajectory.append(
                    session.session_id,
                    {"event": "assistant_text", "turn": turn, "content": result.text},
                )

            if not result.tool_calls:
                self._session_store.save(session)
                return AgentRunResult(
                    output_text=result.text or "(bos yanit)",
                    turns_used=turn,
                    stopped_reason="final_answer",
                    session_id=session.session_id,
                    warnings=warnings,
                )

            for tool_call in result.tool_calls:
                fingerprint = (tool_call.name, tool_call.arguments_json)
                repeated_calls[fingerprint] = repeated_calls.get(fingerprint, 0) + 1
                if repeated_calls[fingerprint] > self._config.agent.repeat_tool_call_limit:
                    warnings.append("Ayni tool cagrisi tekrar etti; dongu durduruldu.")
                    self._session_store.save(session)
                    return AgentRunResult(
                        output_text="Ayni tool cagrisi tekrarlandigi icin ajan durduruldu.",
                        turns_used=turn,
                        stopped_reason="repeated_tool_call",
                        session_id=session.session_id,
                        warnings=warnings,
                    )
                try:
                    tool_result = self._registry.execute_tool_call(
                        tool_call,
                        cwd=cwd,
                        session_id=session.session_id,
                        interactive=interactive,
                    )
                except ValueError as exc:
                    tool_result = type(
                        "AnonymousResult",
                        (),
                        {"ok": False, "code": "TOOL_PARSE_ERROR", "message": str(exc), "data": None},
                    )()
                session.messages.append(self._tool_result_message(tool_call, tool_result))
                self._trajectory.append(
                    session.session_id,
                    {
                        "event": "tool_result",
                        "turn": turn,
                        "tool_name": tool_call.name,
                        "ok": tool_result.ok,
                        "code": tool_result.code,
                        "message": tool_result.message,
                    },
                )
                session.messages = self._compactor.compact(session.messages)
                self._session_store.save(session)

        return AgentRunResult(
            output_text="Maksimum tur sinirina ulasildi.",
            turns_used=self._config.agent.max_turns,
            stopped_reason="max_turns",
            session_id=session.session_id,
            warnings=warnings,
        )
