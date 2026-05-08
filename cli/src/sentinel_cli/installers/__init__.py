"""Installer implementations."""

from sentinel_cli.installers.compose import ComposeInstaller
from sentinel_cli.installers.cos import CosInstaller
from sentinel_cli.installers.k8s import K8sInstaller

__all__ = ["ComposeInstaller", "CosInstaller", "K8sInstaller"]
