"""Install command orchestration."""

from __future__ import annotations

import argparse
import sys

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from sentinel_cli.cli.errors import EXIT_TOOL, UserFacingError
from sentinel_cli.installers import ComposeInstaller, CosInstaller, K8sInstaller
from sentinel_cli.installers.base import BaseInstaller, InstallContext


INSTALLERS: dict[str, type[BaseInstaller]] = {
    "cos": CosInstaller,
    "compose": ComposeInstaller,
    "k8s": K8sInstaller,
}


class InstallError(UserFacingError):
    """Install command failure with a stable exit code."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(message=message, exit_code=EXIT_TOOL, detail=detail)


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--mode",
        choices=sorted(INSTALLERS),
        default=None,
        help="Kurulum hedefi.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Kurulum adimlarini uygula gibi goster, degisiklik yapma.",
    )
    parser.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Preflight kontrollerini atla.",
    )


def _installer_for(mode: str) -> type[BaseInstaller]:
    try:
        return INSTALLERS[mode]
    except KeyError as exc:
        raise InstallError(f"Bilinmeyen install mode: {mode}") from exc


def run(args: argparse.Namespace) -> int:
    console = Console()
    mode = args.mode or _select_mode(console)
    context = InstallContext(
        mode=mode,
        dry_run=args.dry_run,
        skip_preflight=args.skip_preflight,
        console=console,
    )
    installer = _installer_for(mode)(context)

    steps = [("preflight", installer.preflight)]
    if args.skip_preflight:
        steps = [("preflight", lambda: console.print("[yellow]preflight skipped[/yellow]"))]
    steps.extend(
        [
            ("install", installer.install),
            ("wire", installer.wire),
            ("verify", installer.verify),
        ]
    )

    console.print(
        f"[bold]Sentinel install[/bold] mode={mode} "
        f"dry_run={str(args.dry_run).lower()} "
        f"skip_preflight={str(args.skip_preflight).lower()}"
    )

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        ) as progress:
            for name, action in steps:
                task = progress.add_task(f"{name}...", total=None)
                action()
                progress.update(task, description=f"{name} done")
                progress.stop_task(task)
    except UserFacingError:
        raise
    except Exception as exc:
        raise InstallError("Install komutu basarisiz oldu.", detail=str(exc)) from exc

    console.print("[green]Install akisi tamamlandi.[/green]")
    return 0


def _select_mode(console: Console) -> str:
    if not sys.stdin.isatty():
        raise InstallError("Install mode gerekli: --mode {cos,compose,k8s}")

    modes = sorted(INSTALLERS)
    console.print("Kurulum modu secin:")
    for index, mode in enumerate(modes, start=1):
        console.print(f"  {index}. {mode}")

    while True:
        value = input("mode [compose]: ").strip() or "compose"
        if value in INSTALLERS:
            return value
        if value.isdigit():
            choice = int(value)
            if 1 <= choice <= len(modes):
                return modes[choice - 1]
        console.print("[red]Gecersiz mode.[/red] cos, compose veya k8s girin.")
