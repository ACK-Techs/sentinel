"""CLI surface with run/repl/config/doctor entrypoints."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from sentinel_cli import __version__
from sentinel_cli.agent import AgentLoop
from sentinel_cli.cli.errors import (
    EXIT_INTERRUPTED,
    EXIT_LLM,
    EXIT_OK,
    EXIT_TOOL,
    EXIT_USAGE,
    UserFacingError,
)
from sentinel_cli.cli.logging_utils import configure_logging
from sentinel_cli.config import CliOverrides, ConfigError, load_config, resolve_profile
from sentinel_cli.hooks import HookManager
from sentinel_cli.llm.errors import LLMError
from sentinel_cli.llm.factory import build_provider
from sentinel_cli.session import SessionStore, TrajectoryRecorder
from sentinel_cli.tools import MCPClientManager


def _add_common_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--profile", default=None, help="Aktif config profili.")
    parser.add_argument("--config", type=Path, default=None, help="YAML config dosyasi yolu.")
    parser.add_argument("--model", default=None, help="Aktif profile model override.")
    parser.add_argument("--base-url", default=None, help="Aktif profile base_url override.")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default=None, help="Provider override.")
    parser.add_argument("--connect-timeout", type=float, default=None, help="HTTP connect timeout.")
    parser.add_argument("--read-timeout", type=float, default=None, help="HTTP read timeout.")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default=None, help="Log seviyesi.")
    parser.add_argument("--max-turns", type=int, default=None, help="Ajan icin max turn sayisi.")
    parser.add_argument("--yes", action="store_true", help="Mutating tool isteklerini otomatik onayla.")
    parser.add_argument("--enable-trajectory", action="store_true", help="Trajectory kaydini etkinlestir.")
    parser.add_argument("--session-id", default=None, help="Var olan oturumu hedefle.")
    parser.add_argument("--resume", action="store_true", help="Verilen session_id ile devam etmeyi dene.")
    parser.add_argument("--verbose", action="store_true", help="Teknik hata detaylarini goster.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinel-cli",
        description="Sentinel Faz 2 agentic CLI",
    )
    _add_common_flags(parser)
    parser.add_argument("--dump-config", action="store_true", help="Efektif config ozetini yazdir.")
    parser.add_argument("--version", action="store_true", help="Sadece surum bilgisini yazdir.")

    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Tek seferlik prompt calistir.")
    _add_common_flags(run_parser)
    run_parser.add_argument("prompt", nargs="?", default=None, help="Tek seferlik prompt metni.")

    repl_parser = subparsers.add_parser("repl", help="Etkilesimli REPL oturumu baslat.")
    _add_common_flags(repl_parser)

    config_parser = subparsers.add_parser("config", help="Efektif config ve profili goster.")
    _add_common_flags(config_parser)

    doctor_parser = subparsers.add_parser("doctor", help="Profil ve bagimlilik kontrolu ozetini goster.")
    _add_common_flags(doctor_parser)

    subparsers.add_parser("version", help="Surum yazdir.")
    return parser


def _cli_overrides(args: argparse.Namespace) -> CliOverrides:
    return CliOverrides(
        config_path=args.config,
        profile=getattr(args, "profile", None),
        model=getattr(args, "model", None),
        base_url=getattr(args, "base_url", None),
        provider=getattr(args, "provider", None),
        connect_timeout_sec=getattr(args, "connect_timeout", None),
        read_timeout_sec=getattr(args, "read_timeout", None),
        log_level=getattr(args, "log_level", None),
        max_turns=getattr(args, "max_turns", None),
        auto_approve=getattr(args, "yes", False) or None,
        trajectory_enabled=getattr(args, "enable_trajectory", False) or None,
    )


def _load_runtime(args: argparse.Namespace):
    config = load_config(config_path=args.config, cli_overrides=_cli_overrides(args))
    profile = resolve_profile(config)
    logger = configure_logging("DEBUG" if args.verbose else config.logging.level)
    return config, profile, logger


def _print_config(config, profile) -> int:
    print(
        json.dumps(
            {
                "config": config.sanitized_summary(),
                "active_profile": profile.sanitized_summary(),
            },
            indent=2,
            ensure_ascii=True,
            default=str,
        )
    )
    return EXIT_OK


def _doctor(config, profile) -> int:
    mcp = MCPClientManager(config.mcp).discover_tools()
    payload = {
        "profile": profile.name,
        "provider": profile.provider,
        "model": profile.model,
        "base_url": profile.base_url,
        "api_key_present": bool(profile.api_key),
        "trajectory_enabled": config.session.trajectory_enabled,
        "mcp": {"available": mcp.available, "message": mcp.message, "tools": mcp.tools},
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return EXIT_OK


def _build_agent(config, profile, *, input_fn=input):
    provider = build_provider(config, resolved_profile=profile)
    session_store = SessionStore(config.session)
    trajectory = TrajectoryRecorder(
        config.session.trajectory_directory,
        enabled=config.session.trajectory_enabled,
    )
    hooks = HookManager(config.hooks)
    return AgentLoop(
        config=config,
        resolved_profile=profile,
        provider=provider,
        session_store=session_store,
        trajectory=trajectory,
        hook_manager=hooks,
        prompt_input=input_fn,
    )


def _run_once(args: argparse.Namespace, *, prompt: str, interactive: bool) -> int:
    config, profile, logger = _load_runtime(args)
    agent = _build_agent(config, profile)
    result = agent.run(
        prompt=prompt,
        cwd=os.getcwd(),
        interactive=interactive,
        session_id=args.session_id,
        resume=args.resume,
    )
    for warning in result.warnings:
        print(f"Uyari: {warning}", file=sys.stderr)
    print(result.output_text)
    logger.info(
        "agent_run_completed",
        extra={
            "session_id": result.session_id,
            "provider": profile.provider,
            "turn": result.turns_used,
            "event_name": result.stopped_reason,
        },
    )
    return EXIT_OK


def _repl(args: argparse.Namespace) -> int:
    config, profile, logger = _load_runtime(args)
    agent = _build_agent(config, profile)
    print("Sentinel REPL basladi. /exit ile cikis yapabilirsiniz.")
    session_id = args.session_id
    while True:
        try:
            prompt = input("sentinel> ").strip()
        except EOFError:
            print()
            return EXIT_OK
        except KeyboardInterrupt:
            print("\nREPL iptal edildi.")
            return EXIT_INTERRUPTED

        if not prompt:
            continue
        if prompt in {"/exit", "/quit"}:
            return EXIT_OK
        if prompt == "/help":
            print("/exit, /quit, /help")
            continue
        try:
            result = agent.run(
                prompt=prompt,
                cwd=os.getcwd(),
                interactive=True,
                session_id=session_id,
                resume=bool(session_id),
            )
        except KeyboardInterrupt:
            print("Ajan turu iptal edildi.")
            continue
        session_id = result.session_id
        for warning in result.warnings:
            print(f"Uyari: {warning}", file=sys.stderr)
        print(result.output_text)
        logger.info(
            "repl_turn_completed",
            extra={
                "session_id": result.session_id,
                "provider": profile.provider,
                "turn": result.turns_used,
                "event_name": result.stopped_reason,
            },
        )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.version or args.command == "version":
            print(__version__)
            return EXIT_OK

        if args.dump_config or args.command == "config":
            config, profile, _ = _load_runtime(args)
            return _print_config(config, profile)

        if args.command == "doctor":
            config, profile, _ = _load_runtime(args)
            return _doctor(config, profile)

        if args.command == "run":
            prompt = args.prompt
            if prompt is None:
                if sys.stdin.isatty():
                    raise UserFacingError("Run komutu icin prompt veya pipe girdisi gerekli.", EXIT_USAGE)
                prompt = sys.stdin.read().strip()
            return _run_once(args, prompt=prompt, interactive=sys.stdin.isatty())

        if args.command == "repl":
            return _repl(args)

        if not sys.stdin.isatty():
            prompt = sys.stdin.read().strip()
            return _run_once(args, prompt=prompt, interactive=False)

        return _repl(args)
    except ConfigError as exc:
        print(f"Config hatasi: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except UserFacingError as exc:
        print(exc.message, file=sys.stderr)
        if getattr(args, "verbose", False) and exc.detail:
            print(exc.detail, file=sys.stderr)
        return exc.exit_code
    except LLMError as exc:
        print(f"LLM hatasi: {exc}", file=sys.stderr)
        if getattr(args, "verbose", False):
            raise
        return EXIT_LLM
    except ValueError as exc:
        print(f"Tool hatasi: {exc}", file=sys.stderr)
        if getattr(args, "verbose", False):
            raise
        return EXIT_TOOL
    except KeyboardInterrupt:
        print("Islem kullanici tarafindan iptal edildi.", file=sys.stderr)
        return EXIT_INTERRUPTED
