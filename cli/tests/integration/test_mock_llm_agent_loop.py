from __future__ import annotations

import json

import httpx

from sentinel_cli.agent import AgentLoop
from sentinel_cli.config import CliOverrides, load_config, resolve_profile
from sentinel_cli.hooks import HookManager
from sentinel_cli.llm.factory import build_provider
from sentinel_cli.session import SessionStore, TrajectoryRecorder


def test_mock_llm_agent_loop_reads_file_and_returns_summary(tmp_path) -> None:
    info_path = tmp_path / "info.txt"
    info_path.write_text("grafana ok", encoding="utf-8")

    requests: list[dict[str, object]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        requests.append(payload)

        if len(requests) == 1:
            tool_names = [tool["function"]["name"] for tool in payload.get("tools", [])]
            assert "read_file" in tool_names
            return httpx.Response(
                200,
                json={
                    "choices": [
                        {
                            "message": {
                                "content": "Dosyayi kontrol ediyorum.",
                                "tool_calls": [
                                    {
                                        "id": "call_1",
                                        "type": "function",
                                        "function": {
                                            "name": "read_file",
                                            "arguments": json.dumps({"path": str(info_path)}),
                                        },
                                    }
                                ],
                            },
                            "finish_reason": "tool_calls",
                        }
                    ]
                },
            )

        messages = payload["messages"]
        assert messages[-1]["role"] == "tool"
        tool_payload = json.loads(messages[-1]["content"])
        assert tool_payload["ok"] is True
        assert tool_payload["data"]["content"] == "grafana ok"
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {"content": "Grafana durumu: grafana ok"},
                        "finish_reason": "stop",
                    }
                ]
            },
        )

    config = load_config(
        cli_overrides=CliOverrides(profile="cloud", model="mock-cloud"),
        env={"SENTINEL_API_KEY": "redacted"},
    )
    config.profiles["cloud"].supports_tools = True
    config.tools.auto_approve = True
    config.tools.approval_mode = "auto"
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "trajectories"
    config.session.trajectory_enabled = True

    profile = resolve_profile(config, env={"SENTINEL_API_KEY": "redacted"})
    provider = build_provider(
        config,
        transport=httpx.MockTransport(handler),
        resolved_profile=profile,
    )
    loop = AgentLoop(
        config=config,
        resolved_profile=profile,
        provider=provider,
        session_store=SessionStore(config.session),
        trajectory=TrajectoryRecorder(config.session.trajectory_directory, enabled=True),
        hook_manager=HookManager(config.hooks),
    )

    result = loop.run(prompt="Grafana durumunu ozetle", cwd=str(tmp_path), interactive=False)

    assert result.output_text == "Grafana durumu: grafana ok"
    assert result.turns_used == 2
    assert result.warnings == []
    assert len(requests) == 2
