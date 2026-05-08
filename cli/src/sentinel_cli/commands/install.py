"""Install command orchestration."""

from __future__ import annotations

import argparse

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
        required=True,
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
    context = InstallContext(
        mode=args.mode,
        dry_run=args.dry_run,
        skip_preflight=args.skip_preflight,
        console=console,
    )
    installer = _installer_for(args.mode)(context)

    steps = []
    if not args.skip_preflight:
        steps.append(("preflight", installer.preflight))
    steps.extend(
        [
            ("install", installer.install),
            ("wire", installer.wire),
            ("verify", installer.verify),
        ]
    )

    console.print(
        f"[bold]Sentinel install[/bold] mode={args.mode} "
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
