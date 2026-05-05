"""Agent turn loop for Phase 2.C."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from sentinel_cli.config import AppConfig, ResolvedProfile
from sentinel_cli.hooks import HookManager
from sentinel_cli.llm.errors import LLMError
from sentinel_cli.llm.types import ChatMessage, ChatRequest, CompletionResult, MessageRole, ToolCall
from sentinel_cli.observability import GatewayClient, GatewayClientError, check_gateway_connection, check_grafana_connection
from sentinel_cli.session import SessionState, SessionStore, TrajectoryRecorder
from sentinel_cli.tools import ToolRegistry

from sentinel_cli.agent.compaction import HistoryCompactor
from sentinel_cli.agent.turn_end import TurnEndContext, schedule_turn_end_pipeline


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
        self._hook_manager = hook_manager or HookManager(config.hooks)
        self._registry = ToolRegistry(config=config, hook_manager=self._hook_manager, prompt_input=prompt_input)
        self._compactor = HistoryCompactor(config)

    def _finalize_turn(
        self,
        session: SessionState,
        *,
        cwd: str,
        interactive: bool,
        stopped_reason: str,
    ) -> None:
        if stopped_reason == "interrupted":
            return
        ctx = TurnEndContext(
            session=session,
            cwd=cwd,
            interactive=interactive,
            stopped_reason=stopped_reason,
            profile=self._profile.name,
            provider=self._provider,
        )
        schedule_turn_end_pipeline(
            self._config,
            hook_manager=self._hook_manager,
            session_store=self._session_store,
            trajectory=self._trajectory,
            ctx=ctx,
        )

    def _tool_result_message(self, tool_call: ToolCall, result: Any) -> ChatMessage:
        return ChatMessage(
            role=MessageRole.TOOL,
            name=tool_call.name,
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
        system_prompt = self._config.agent.system_prompt
        session = getattr(self, "_active_session", None)
        if session and session.grafana_context_snapshot:
            system_prompt = (
                f"{system_prompt}\n\n"
                "Grafana operasyonel ozeti asagidadir; bu ozet canli panel veya metrik akisi degildir.\n"
                f"{session.grafana_context_snapshot}"
            )
        if session and session.observability_context_snapshot:
            system_prompt = (
                f"{system_prompt}\n\n"
                "Observability gateway operasyonel ozeti asagidadir; bu ozet canli veri dump'i degildir.\n"
                f"{session.observability_context_snapshot}"
            )
        return ChatRequest(
            messages=messages,
            system_prompt=system_prompt,
            tools=self._registry.definitions() if self._profile.supports_tools else [],
        )

    def _ensure_grafana_snapshot(self, session) -> None:
        if not self._config.agent.grafana_context_in_repl:
            return
        if session.grafana_context_snapshot is not None:
            return

        result = check_grafana_connection(self._config.grafana, env=dict(os.environ))
        session.grafana_context_snapshot = json.dumps(result.to_dict(), ensure_ascii=True)
        self._session_store.save(session)

    def _ensure_observability_snapshot(self, session) -> None:
        if not self._config.agent.grafana_context_in_repl:
            return
        if session.observability_context_snapshot is not None:
            return

        env = dict(os.environ)
        gateway = check_gateway_connection(self._config.observability_gateway, env=env)
        snapshot = {
            "gateway": {
                "configured": gateway.configured,
                "attempted": gateway.attempted,
                "ok": gateway.ok,
                "status": gateway.status,
            },
            "backends_configured": [],
            "backends_reachable": [],
        }

        if gateway.base_url_present:
            try:
                payload = GatewayClient(self._config.observability_gateway, env=env).get_status()
            except GatewayClientError:
                payload = None
            if isinstance(payload, dict):
                backends = payload.get("backends", {})
                if isinstance(backends, dict):
                    snapshot["backends_configured"] = sorted(
                        name
                        for name, details in backends.items()
                        if isinstance(details, dict) and details.get("configured") is True
                    )
                    snapshot["backends_reachable"] = sorted(
                        name
                        for name, details in backends.items()
                        if isinstance(details, dict) and details.get("reachable") is True
                    )

        session.observability_context_snapshot = json.dumps(snapshot, ensure_ascii=True)
        self._session_store.save(session)

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

        self._ensure_grafana_snapshot(session)
        self._ensure_observability_snapshot(session)
        self._active_session = session
        session.messages = self._compactor.compact(session.messages, session=session)
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
                self._active_session = None
                return AgentRunResult(
                    output_text="Islem kullanici tarafindan iptal edildi.",
                    turns_used=turn,
                    stopped_reason="interrupted",
                    session_id=session.session_id,
                    warnings=warnings,
                )
            except LLMError:
                raise

            if result.text:
                session.messages.append(ChatMessage(role=MessageRole.ASSISTANT, content=result.text))
                self._trajectory.append(
                    session.session_id,
                    {"event": "assistant_text", "turn": turn, "content": result.text},
                )

            if not result.tool_calls:
                self._session_store.save(session)
                self._finalize_turn(
                    session,
                    cwd=cwd,
                    interactive=interactive,
                    stopped_reason="final_answer",
                )
                self._active_session = None
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
                    self._finalize_turn(
                        session,
                        cwd=cwd,
                        interactive=interactive,
                        stopped_reason="repeated_tool_call",
                    )
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
                session.messages = self._compactor.compact(session.messages, session=session)
                self._session_store.save(session)

        self._session_store.save(session)
        self._finalize_turn(
            session,
            cwd=cwd,
            interactive=interactive,
            stopped_reason="max_turns",
        )
        self._active_session = None
        return AgentRunResult(
            output_text="Maksimum tur sinirina ulasildi.",
            turns_used=self._config.agent.max_turns,
            stopped_reason="max_turns",
            session_id=session.session_id,
            warnings=warnings,
        )
