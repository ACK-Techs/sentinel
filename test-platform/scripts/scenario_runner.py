from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
import ulid
import yaml

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / "runs"
GROUND_TRUTH = ROOT / "ground-truth.jsonl"
COMPOSE_PORTS = {
    "gateway": 8080,
    "orders": 8081,
    "payments": 8082,
    "inventory": 8083,
}


def now() -> str:
    return datetime.now(UTC).isoformat()


def log(message: str) -> None:
    print(f"{now()} {message}", flush=True)


def write_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def write_summary(run_id: str, summary: dict[str, Any]) -> None:
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def annotate_namespace(namespace: str, patch: dict[str, str], runtime: str) -> None:
    if runtime == "compose":
        write_jsonl(
            GROUND_TRUTH,
            {
                "ts": now(),
                "run_id": patch.get("sentinel.io/run-id", "compose"),
                "scenario": patch.get("sentinel.io/scenario", "compose"),
                "event": "annotation_skipped",
                "target": namespace,
                "chaos_state": patch,
                "version": 0,
            },
        )
        return
    for key, value in patch.items():
        subprocess.run(
            [
                "kubectl",
                "annotate",
                "namespace",
                namespace,
                f"{key}={value}",
                "--overwrite",
            ],
            check=True,
            cwd=ROOT,
        )


def service_url(service: str, namespace: str, runtime: str) -> str:
    if runtime == "compose":
        port = COMPOSE_PORTS[service]
        return f"http://127.0.0.1:{port}"
    return f"http://{service}.{namespace}.svc.cluster.local:8080"


def apply_profile(
    service: str,
    namespace: str,
    token: str,
    profile: str,
    runtime: str,
) -> dict[str, Any]:
    response = httpx.post(
        f"{service_url(service, namespace, runtime)}/admin/chaos/profile",
        json={"name": profile},
        headers={"X-Chaos-Token": token},
        timeout=5.0,
    )
    response.raise_for_status()
    return response.json()


def reload_profile(service: str, namespace: str, token: str, runtime: str) -> dict[str, Any]:
    response = httpx.post(
        f"{service_url(service, namespace, runtime)}/admin/chaos/reload",
        headers={"X-Chaos-Token": token},
        timeout=5.0,
    )
    response.raise_for_status()
    return response.json()


def healthcheck(service: str, namespace: str, runtime: str) -> None:
    response = httpx.get(f"{service_url(service, namespace, runtime)}/health", timeout=2.0)
    response.raise_for_status()


def start_load(scenario_name: str, runtime: str, namespace: str) -> subprocess.Popen[str]:
    if runtime == "compose":
        env = os.environ.copy()
        env["SCENARIO"] = scenario_name
        subprocess.run(
            ["docker", "compose", "up", "-d", "load"],
            cwd=ROOT,
            check=True,
            env=env,
        )
        return subprocess.Popen(
            ["docker", "compose", "logs", "-f", "load"],
            cwd=ROOT,
            text=True,
            env=env,
        )
    subprocess.run(
        ["kubectl", "-n", namespace, "scale", "deploy/load", "--replicas=1"],
        cwd=ROOT,
        check=True,
    )
    return subprocess.Popen(
        ["kubectl", "-n", namespace, "logs", "-f", "deploy/load"],
        cwd=ROOT,
        text=True,
    )


def stop_load(process: subprocess.Popen[str] | None, runtime: str, namespace: str) -> None:
    if process is None:
        return
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
    if runtime == "compose":
        subprocess.run(["docker", "compose", "stop", "load"], cwd=ROOT, check=True)
        return
    subprocess.run(
        ["kubectl", "-n", namespace, "scale", "deploy/load", "--replicas=0"],
        cwd=ROOT,
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("scenario")
    run_parser.add_argument("--namespace", default="sentinel-target")
    run_parser.add_argument("--dry-run", action="store_true")
    run_parser.add_argument("--runtime", choices=["compose", "k8s"], default="compose")
    run_parser.add_argument("--token", default=os.getenv("CHAOS_TOKEN", "sentinel-chaos-token"))

    subparsers.add_parser("list")
    abort_parser = subparsers.add_parser("abort")
    abort_parser.add_argument("--namespace", default="sentinel-target")
    abort_parser.add_argument("--runtime", choices=["compose", "k8s"], default="compose")
    abort_parser.add_argument("--token", default=os.getenv("CHAOS_TOKEN", "sentinel-chaos-token"))
    abort_parser.add_argument("--services", default="orders,payments,inventory,gateway")

    return parser.parse_args()


@dataclass
class ScenarioStep:
    at_s: int
    target: str
    profile: str


@dataclass
class Scenario:
    name: str
    description: str
    duration_s: int
    warmup_s: int
    cooldown_s: int
    load_scenario: str
    expected_symptoms: list[str]
    steps: list[ScenarioStep]


def read_scenario(path: Path) -> Scenario:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    steps = [
        ScenarioStep(
            at_s=int(step["at_s"]),
            target=str(step["target"]),
            profile=str(step["chaos"]["profile"]),
        )
        for step in raw["steps"]
    ]
    return Scenario(
        name=str(raw["name"]),
        description=str(raw.get("description", raw["name"])),
        duration_s=int(raw["duration_s"]),
        warmup_s=int(raw.get("warmup_s", 0)),
        cooldown_s=int(raw.get("cooldown_s", 0)),
        load_scenario=str(raw["load"]["scenario"]),
        expected_symptoms=list(raw.get("expected_symptoms", [])),
        steps=steps,
    )


def abort_services(
    namespace: str,
    token: str,
    services: list[str],
    status_value: str,
    runtime: str,
) -> None:
    for service in services:
        try:
            apply_profile(service, namespace, token, "healthy", runtime)
        except Exception as exc:  # noqa: BLE001
            log(f"abort reset failed for {service}: {exc}")
    annotate_namespace(
        namespace,
        {"sentinel.io/run-status": status_value, "sentinel.io/run-end": now()},
        runtime,
    )


def run_scenario(args: argparse.Namespace) -> int:
    scenario_path = Path(args.scenario)
    scenario = read_scenario(scenario_path)
    run_id = str(ulid.new())
    gt_path = GROUND_TRUTH
    load_process: subprocess.Popen[str] | None = None
    services = sorted({step.target for step in scenario.steps})
    summary: dict[str, Any] = {
        "run_id": run_id,
        "scenario": scenario.name,
        "steps": [],
        "status": "running",
    }

    def handle_signal(signum: int, _frame: Any) -> None:
        abort_services(args.namespace, args.token, services, "aborted", args.runtime)
        write_jsonl(
            gt_path,
            {
                "ts": now(),
                "run_id": run_id,
                "scenario": scenario.name,
                "event": "aborted",
                "target": ",".join(services),
                "chaos_state": {"signal": signum},
                "version": -1,
            },
        )
        stop_load(load_process, args.runtime, args.namespace)
        raise SystemExit(1)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    for service in services:
        if not args.dry_run:
            healthcheck(service, args.namespace, args.runtime)

    for service in services:
        if not args.dry_run:
            apply_profile(service, args.namespace, args.token, "healthy", args.runtime)

    write_jsonl(
        gt_path,
        {
            "ts": now(),
            "run_id": run_id,
            "scenario": scenario.name,
            "event": "run_start",
            "target": ",".join(services),
            "chaos_state": {"description": scenario.description},
            "version": 0,
        },
    )

    if not args.dry_run:
        annotate_namespace(
            args.namespace,
            {
                "sentinel.io/run-id": run_id,
                "sentinel.io/scenario": scenario.name,
                "sentinel.io/chaos-start": now(),
                "sentinel.io/run-status": "running",
            },
            args.runtime,
        )

    if not args.dry_run:
        load_process = start_load(scenario.load_scenario, args.runtime, args.namespace)
    write_jsonl(
        gt_path,
        {
            "ts": now(),
            "run_id": run_id,
            "scenario": scenario.name,
            "event": "load_start",
            "target": "gateway",
            "chaos_state": {"load_scenario": scenario.load_scenario},
            "version": 0,
        },
    )
    time.sleep(scenario.warmup_s)

    started = time.monotonic()
    for step in scenario.steps:
        while time.monotonic() - started < step.at_s:
            time.sleep(0.5)
        if args.dry_run:
            response_body = {"applied": {"profile": step.profile}, "version": 0}
        elif step.profile == "reload":
            response_body = reload_profile(step.target, args.namespace, args.token, args.runtime)
        else:
            response_body = apply_profile(
                step.target,
                args.namespace,
                args.token,
                step.profile,
                args.runtime,
            )
        write_jsonl(
            gt_path,
            {
                "ts": now(),
                "run_id": run_id,
                "scenario": scenario.name,
                "event": "chaos_apply",
                "target": step.target,
                "chaos_state": response_body.get("applied", {}),
                "version": response_body.get("version", 0),
            },
        )
        summary["steps"].append({"target": step.target, "profile": step.profile})

    while time.monotonic() - started < scenario.duration_s:
        time.sleep(1)

    if not args.dry_run:
        abort_services(args.namespace, args.token, services, "completed", args.runtime)
    write_jsonl(
        gt_path,
        {
            "ts": now(),
            "run_id": run_id,
            "scenario": scenario.name,
            "event": "chaos_end",
            "target": ",".join(services),
            "chaos_state": {"expected_symptoms": scenario.expected_symptoms},
            "version": 0,
        },
    )

    time.sleep(scenario.cooldown_s)
    stop_load(load_process, args.runtime, args.namespace)
    write_jsonl(
        gt_path,
        {
            "ts": now(),
            "run_id": run_id,
            "scenario": scenario.name,
            "event": "run_end",
            "target": ",".join(services),
            "chaos_state": {"status": "completed"},
            "version": 0,
        },
    )
    summary["status"] = "completed"
    summary["started_at"] = now()
    summary["ended_at"] = now()
    summary["expected_symptoms"] = scenario.expected_symptoms
    write_summary(run_id, summary)
    return 0


def list_scenarios() -> int:
    for path in sorted((ROOT / "chaos" / "profiles").glob("*.yaml")):
        print(path.stem)
    return 0


def abort_command(args: argparse.Namespace) -> int:
    services = [item.strip() for item in args.services.split(",") if item.strip()]
    abort_services(args.namespace, args.token, services, "aborted", args.runtime)
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "run":
        return run_scenario(args)
    if args.command == "list":
        return list_scenarios()
    if args.command == "abort":
        return abort_command(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
