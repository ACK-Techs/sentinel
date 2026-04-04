"""Minimal CLI surface with Phase 2.B config integration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sentinel_cli import __version__
from sentinel_cli.config import CliOverrides, ConfigError, load_config, resolve_profile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinel-cli",
        description="Sentinel Faz 2 agentic CLI package skeleton",
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Aktif config profilini sec (or. cloud, local, anthropic).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="YAML config dosyasi yolu. Oncelik: defaults < file < env < CLI.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Aktif profile uygulanacak model override degeri.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Aktif profile uygulanacak base_url override degeri.",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic"],
        default=None,
        help="Aktif profile uygulanacak provider override degeri.",
    )
    parser.add_argument(
        "--connect-timeout",
        type=float,
        default=None,
        help="HTTP connect timeout saniye cinsinden.",
    )
    parser.add_argument(
        "--read-timeout",
        type=float,
        default=None,
        help="HTTP read timeout saniye cinsinden.",
    )
    parser.add_argument(
        "--dump-config",
        action="store_true",
        help="Efektif config ve aktif profil ozetini secret-safe bicimde yazdir.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the package version and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    overrides = CliOverrides(
        config_path=args.config,
        profile=args.profile,
        model=args.model,
        base_url=args.base_url,
        provider=args.provider,
        connect_timeout_sec=args.connect_timeout,
        read_timeout_sec=args.read_timeout,
    )
    if args.dump_config:
        try:
            config = load_config(config_path=args.config, cli_overrides=overrides)
            profile = resolve_profile(config)
        except ConfigError as exc:
            print(f"Config hatasi: {exc}")
            return 2
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
        return 0

    parser.print_help()
    return 0
