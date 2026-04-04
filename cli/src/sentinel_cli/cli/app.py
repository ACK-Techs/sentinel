"""Minimal Phase 2.A CLI placeholder."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinel-cli",
        description="Sentinel Faz 2 agentic CLI package skeleton",
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Planned profile selector (Phase 2.B).",
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
        from sentinel_cli import __version__

        print(__version__)
        return 0

    parser.print_help()
    return 0
