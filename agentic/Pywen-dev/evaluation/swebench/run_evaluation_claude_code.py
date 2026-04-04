import os
import shutil
import argparse
import traceback

from typing import Any, Callable, cast
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from dataclasses import dataclass

from docker import from_env, DockerClient
from docker.errors import ImageNotFound, APIError, NotFound
from docker.models.containers import Container, ExecResult
from datasets import load_dataset
from tqdm import tqdm


AGENT_IMAGE = "pywen/claude-code-agent:0.1"
AGENT_IMAGE_DOCKERFILE = "Dockerfile.claude-code-agent"

CLAUDE_BIN_IN_CONTAINER = "/usr/local/share/npm-global/bin/claude"

HOST_AGENT_CACHE_DIRNAME = "claude_agent_cache"
HOST_USR_LOCAL_DIRNAME = "usr_local"
HOST_CLAUDE_HOME_DIRNAME = "claude_home"  # ~/.claude 缓存
RESULTS_DIRNAME = "results"


class DockerOps:
    """ docker 操作的统一封装,增加错误处理机制（与 Pywen 原实现保持一致） """

    def __init__(self):
        self.client: DockerClient = from_env()

    def image_exists(self, name: str) -> bool:
        try:
            self.client.images.get(name)
            return True
        except ImageNotFound:
            return False

    def pull_image(self, name: str) -> None:
        last_err = None
        for _ in range(3):
            try:
                self.client.images.pull(name)
                return
            except Exception as e:  # noqa: BLE001
                last_err = e
        raise RuntimeError(f"Failed to pull image {name}: {last_err}")

    def build_image(self, tag: str, dockerfile: Path, context: Path) -> None:
        try:
            stream = self.client.api.build(
                path=str(context),
                dockerfile=str(dockerfile.name),
                tag=tag,
                decode=True,
                rm=True,
            )
            for chunk in stream:
                if "error" in chunk:
                    raise RuntimeError(chunk["error"])
        except APIError as e:  # noqa: PERF203
            raise RuntimeError(f"Docker build failed: {e}") from e

    def run_container(
        self,
        image: str,
        *,
        command: str = "/bin/bash",
        detach: bool = True,
        tty: bool = False,
        stdin_open: bool = True,
        environment: dict | None = None,
        volumes: dict | None = None,
        working_dir: str | None = None,
    ) -> Container:
        try:
            container = self.client.containers.run(
                image=image,
                command=command,
                detach=detach,
                tty=tty,
                stdin_open=stdin_open,
                environment=environment or {},
                volumes=volumes or {},
                working_dir=working_dir,
            )
            return cast(Container, container)
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"Failed to run container from {image}: {e}") from e

    def exec_sh(self, container: Container, shell_cmd: str, check: bool = True) -> str:
        """ 在容器内用 /bin/bash -lc 执行命令。统一解析 ExitCode 和输出，失败时抛错。 """

        try:
            res: ExecResult = container.exec_run(
                cmd=["/bin/bash", "--noprofile", "--norc", "-lc", shell_cmd],
                tty=False,
                stdin=False,
            )
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"Exec failed: {shell_cmd}\n{e}") from e

        code = getattr(res, "exit_code", None)
        out = getattr(res, "output", None)
        if code is None:
            code = res[0]
            out = res[1]
        text = (
            out.decode("utf-8", "ignore")
            if isinstance(out, (bytes, bytearray))
            else (out or "")
        )

        if check and code != 0:
            raise RuntimeError(f"Command failed ({code}): {shell_cmd}\n{text}")
        return text

    def stop_and_remove(self, container: Container | None) -> None:
        if container is None:
            return
        try:
            container.stop(timeout=5)
        except Exception:  # noqa: BLE001
            pass
        try:
            container.remove()
        except Exception:  # noqa: BLE001
            pass

    def cp_from_container(self, container: Container, src_path: str, dst: Path) -> None:
        """ 将容器内路径内容复制到宿主目录。dst 若不存在会创建。 """

        dst.mkdir(parents=True, exist_ok=True)
        try:
            stream, _ = container.get_archive(src_path)
        except NotFound as e:  # noqa: PERF203
            raise RuntimeError(f"Path not found in container: {src_path}") from e

        import io
        import tarfile

        bio = io.BytesIO()
        for chunk in stream:
            bio.write(chunk)
        bio.seek(0)
        with tarfile.open(fileobj=bio, mode="r|*") as tar:
            tar.extractall(path=dst)


@dataclass
class BenchmarkConfig:
    valid_datasets: list[str]
    load_dataset: Callable[[str], Any]
    image_name: Callable[[str], str]
    problem_statement: Callable[[dict, Path], Any]
    working_dir: Callable[[str], str]
    evaluate_harness: Callable[..., list[str]]
    evaluate_harness_before: Callable[..., Any]
    evaluate_harness_after: Callable[..., Any]


def _write_problem_statement(instance_dir: Path, content: str) -> int:
    with open(instance_dir / "problem_statement.txt", "w", encoding="utf-8") as f:
        return f.write(content)


BENCHMARK_CONFIG: dict[str, BenchmarkConfig] = {
    "SWE-bench": BenchmarkConfig(
        valid_datasets=["SWE-bench", "SWE-bench_Lite", "SWE-bench_Verified"],
        load_dataset=lambda dataset_name: load_dataset(
            f"princeton-nlp/{dataset_name}", split="test"
        ),
        image_name=lambda instance_id: (
            f"swebench/sweb.eval.x86_64.{instance_id.lower()}:latest".replace(
                "__", "_1776_"
            )
        ),
        problem_statement=lambda instance, instance_dir: _write_problem_statement(
            instance_dir, instance.get("problem_statement", "")
        ),
        working_dir=lambda instance_id: "/testbed/",
        evaluate_harness=lambda dataset_name, task_results_dir, task_id, max_workers: [
            "swebench_venv/bin/python",
            "-m",
            "swebench.harness.run_evaluation",
            "--dataset_name",
            f"princeton-nlp/{dataset_name}",
            "--predictions_path",
            (task_results_dir / "predictions.json").absolute().as_posix(),
            "--max_workers",
            str(max_workers),
            "--run_id",
            task_id,
        ],
        evaluate_harness_before=lambda: None,
        evaluate_harness_after=lambda: None,
    ),
}


class ClaudeCodeBenchmarkEvaluation:
    """使用 Claude Code 官方 CLI 进行 SWE-bench 评估。

    结构尽量与 Pywen 自身的 BenchmarkEvaluation 保持一致，只是把
    "agent" 换成了官方的 claude CLI。
    """

    def __init__(
        self,
        benchmark: str,
        working_dir: str,
        dataset_name: str = "SWE-bench_Lite",
        run_id: str = "claude-code",
        max_workers: int = 4,
        instance_ids: list[str] | None = None,
        pattern: str | None = None,
        limit: int | None = None,
        force: bool = False,
    ) -> None:
        self.pattern = pattern
        self.limit = limit
        self.skip_completed = not force

        self.ops = DockerOps()

        self.benchmark = benchmark
        self.config: BenchmarkConfig = BENCHMARK_CONFIG[benchmark]
        self.dataset_name = dataset_name
        self.dataset: Any = self.config.load_dataset(self.dataset_name)

        eval_dir = Path(__file__).parent.resolve()
        self.working_dir = (eval_dir / working_dir).resolve()
        self.working_dir.mkdir(parents=True, exist_ok=True)

        self.results_dir = (eval_dir / RESULTS_DIRNAME).resolve()
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.task_id = f"{benchmark}_{dataset_name}_{run_id}".replace("/", "_")
        self.task_results_dir = self.results_dir / self.task_id
        self.task_results_dir.mkdir(parents=True, exist_ok=True)

        if instance_ids is not None:
            self.instance_ids = instance_ids
        else:
            ids = [item["instance_id"] for item in self.dataset]
            if self.pattern:
                import re

                regex = re.compile(self.pattern)
                ids = [iid for iid in ids if regex.search(iid)]
            if self.limit:
                ids = ids[: self.limit]
            self.instance_ids = ids

        self.max_workers = max_workers

        self.host_agent_cache = self.working_dir / HOST_AGENT_CACHE_DIRNAME
        self.host_agent_cache.mkdir(parents=True, exist_ok=True)

        # 转发 Anthropic 配置到 SWE-bench 容器中
        # 优先读取 ANTHROPIC_AUTH_TOKEN，兼容 ANTHROPIC_API_KEY
        self.anthropic_api_key = os.environ.get("ANTHROPIC_AUTH_TOKEN", "") or os.environ.get("ANTHROPIC_API_KEY", "")
        self.anthropic_base_url = os.environ.get("ANTHROPIC_BASE_URL", "")

    # ------------------------------------------------------------------
    # 构建 Claude Code agent 镜像并导出 /usr/local
    # ------------------------------------------------------------------
    def ensure_agent_image_and_cache(self) -> None:
        """确保 Claude Code agent 镜像存在并把 /usr/local 导出到宿主机缓存。

        在 Pywen 仓库根目录下使用 Dockerfile.claude-code-agent 构建一个
        只安装官方 @anthropic-ai/claude-code 的镜像，然后把其中的 /usr/local
        拷贝出来，之后每个 SWE-bench 实例容器都挂载这个目录即可。
        """

        repo_root = Path(__file__).parents[2].resolve()  # Pywen 仓库根目录
        dockerfile = repo_root / AGENT_IMAGE_DOCKERFILE
        if not dockerfile.exists():
            raise FileNotFoundError(
                f"Missing {AGENT_IMAGE_DOCKERFILE} at Pywen repo root: {dockerfile}"
            )

        if not self.ops.image_exists(AGENT_IMAGE):
            print(f"Building Claude Code agent image {AGENT_IMAGE} ...")
            self.ops.build_image(tag=AGENT_IMAGE, dockerfile=dockerfile, context=repo_root)
        else:
            print(f"Found Claude Code agent image {AGENT_IMAGE}")

        target_usr_local = self.host_agent_cache / HOST_USR_LOCAL_DIRNAME

        def _has_claude_bin(base: Path) -> bool:
            candidates = [
                base / "bin" / "claude",
                base / "usr" / "local" / "share" / "npm-global" / "bin" / "claude",
                base / "local" / "share" / "npm-global" / "bin" / "claude",
            ]
            return any(p.exists() for p in candidates)

        target_claude_home = self.host_agent_cache / HOST_CLAUDE_HOME_DIRNAME

        need_export_usr_local = not _has_claude_bin(target_usr_local)
        need_export_claude_home = not target_claude_home.exists()

        if need_export_usr_local or need_export_claude_home:
            print("Exporting /usr/local and ~/.claude from Claude Code agent image ...")
            container: Container | None = None
            try:
                container = self.ops.run_container(AGENT_IMAGE, command="sleep 60")

                if need_export_usr_local:
                    shutil.rmtree(target_usr_local, ignore_errors=True)
                    self.ops.cp_from_container(container, "/usr/local", target_usr_local)

                if need_export_claude_home:
                    # 初始化 ~/.claude 目录（在容器里跑一次 claude --version 来生成）
                    self.ops.exec_sh(container, "/usr/local/share/npm-global/bin/claude --version", check=False)
                    target_claude_home.mkdir(parents=True, exist_ok=True)
                    try:
                        self.ops.cp_from_container(container, "/root/.claude", target_claude_home)
                    except RuntimeError:
                        # 如果 ~/.claude 不存在，创建空目录即可
                        pass
            finally:
                self.ops.stop_and_remove(container)
        else:
            print("Found existing host cache of Claude Code /usr/local and ~/.claude. Skipping export.")

    def _resolve_usr_local_host_dir(self) -> Path:
        """在导出的缓存中解析出真正的 /usr/local 目录。"""

        base = (self.host_agent_cache / HOST_USR_LOCAL_DIRNAME).resolve()
        candidates = [
            base,
            base / "usr" / "local",
            base / "local",
        ]
        for c in candidates:
            if (c / "share" / "npm-global" / "bin" / "claude").exists() or (c / "bin").exists():
                return c

        raise FileNotFoundError(
            f"Could not locate a usable /usr/local in host cache under {base}"
        )

    def _resolve_claude_home_host_dir(self) -> Path:
        """在导出的缓存中解析出 ~/.claude 目录。"""

        base = (self.host_agent_cache / HOST_CLAUDE_HOME_DIRNAME).resolve()
        # tar 导出后可能是 base/.claude 或者直接就是 base
        candidates = [
            base / ".claude",
            base / "claude",
            base,
        ]
        for c in candidates:
            if c.exists() and c.is_dir():
                return c

        # 如果都不存在，创建并返回 base
        base.mkdir(parents=True, exist_ok=True)
        return base

    # ------------------------------------------------------------------
    # SWE-bench 实例执行
    # ------------------------------------------------------------------
    def pull_images(self) -> None:
        names = {self.config.image_name(iid) for iid in self.instance_ids}
        print(f"Preparing {len(names)} SWE-bench images ...")
        for name in tqdm(sorted(names), desc="Pull SWE images"):
            if not self.ops.image_exists(name):
                self.ops.pull_image(name)

    def _is_instance_completed(self, instance_id: str) -> bool:
        instance_res_dir = self.task_results_dir / instance_id
        patch_path = instance_res_dir / f"{instance_id}.patch"
        log_path = instance_res_dir / "run.log"

        if patch_path.exists() and patch_path.stat().st_size > 0:
            return True
        if log_path.exists() and log_path.stat().st_size > 0:
            return True
        return False

    def run_one_instance(self, instance_id: str) -> None:
        if self.skip_completed and self._is_instance_completed(instance_id):
            print(f"⏭️  Skipping {instance_id} (already completed)")
            return

        ops = DockerOps()
        instance = next((i for i in self.dataset if i["instance_id"] == instance_id), None)
        if not instance:
            print(f"Instance {instance_id} not found in dataset {self.dataset_name}")
            return

        image_name = self.config.image_name(instance_id)
        if not ops.image_exists(image_name):
            print(f"Pulling {image_name} ...")
            ops.pull_image(image_name)

        instance_res_dir = self.task_results_dir / instance_id
        instance_res_dir.mkdir(parents=True, exist_ok=True)
        self.config.problem_statement(instance, instance_res_dir)

        host_usr_local = self._resolve_usr_local_host_dir()
        host_claude_home = self._resolve_claude_home_host_dir()

        volumes: dict[str, dict[str, str]] = {
            str(instance_res_dir): {"bind": "/results", "mode": "rw"},
            str(host_usr_local): {"bind": "/usr/local", "mode": "ro"},
            str(host_claude_home): {"bind": "/root/.claude", "mode": "rw"},
        }

        env: dict[str, str] = {
            "PATH": "/usr/local/share/npm-global/bin:" + os.environ.get("PATH", ""),
            "HOME": "/root",
        }
        if self.anthropic_api_key:
            env["ANTHROPIC_API_KEY"] = self.anthropic_api_key
        if self.anthropic_base_url:
            env["ANTHROPIC_BASE_URL"] = self.anthropic_base_url

        container: Container | None = None
        try:
            container = ops.run_container(
                image=image_name,
                command="/bin/bash",
                environment=env,
                volumes=volumes,
                tty=True,
                stdin_open=True,
            )

            problem_stmt_path = instance_res_dir / "problem_statement.txt"
            problem_stmt = (
                problem_stmt_path.read_text(encoding="utf-8")
                if problem_stmt_path.exists()
                else ""
            )
            prompt = (
                "You are Claude Code running inside a Docker container for the SWE-bench "
                "benchmark. The repository under test is checked out at /testbed.\n\n"
                "Your goal is to fully resolve the GitHub issue described below by "
                "editing the code in /testbed and running the relevant tests. Do not "
                "just describe changes — you must actually apply them to the files so "
                "that `git diff` reflects your final patch.\n\n"
                f"Issue description:\n{problem_stmt}\n\n"
                "You should:\n"
                "- Inspect the codebase under /testbed using your tools.\n"
                "- Identify the root cause of the issue.\n"
                "- Implement a concrete fix by editing the appropriate files.\n"
                "- Run the project tests (for example via pytest or other project-"
                "specific commands) until you are confident the issue is resolved.\n"
                "When you are done, leave all changes applied in the working tree.\n"
            )
            (instance_res_dir / "problem_statement_for_claude.txt").write_text(
                prompt, encoding="utf-8"
            )

            # --dangerously-skip-permissions 在 root 用户下被禁用
            # 解决方案：创建非 root 用户 "claude"，以该用户身份运行 claude CLI
            setup_user_cmd = """
# 创建非 root 用户
useradd -m -s /bin/bash claude 2>/dev/null || true
# 让 claude 用户无密码 sudo
echo 'claude ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
# 确保 claude 用户的 home 目录存在
mkdir -p /home/claude/.claude && chown -R claude:claude /home/claude
# 给 testbed 设置 git safe directory
git config --global --add safe.directory /testbed
"""
            ops.exec_sh(container, setup_user_cmd, check=False)

            # 使用 base64 编码来安全传递 prompt，避免 shell 特殊字符问题
            import base64
            prompt_b64 = base64.b64encode(prompt.encode("utf-8")).decode("ascii")
            ops.exec_sh(
                container,
                f"echo '{prompt_b64}' | base64 -d > /tmp/claude_prompt.txt && chown claude:claude /tmp/claude_prompt.txt",
                check=False,
            )

            # 创建运行脚本（使用 heredoc 避免引号问题）
            run_script = f"""#!/bin/bash
cd /testbed
source /opt/miniconda3/etc/profile.d/conda.sh
conda activate testbed
export HOME=/home/claude
export PATH="/usr/local/share/npm-global/bin:$PATH"
PROMPT=$(cat /tmp/claude_prompt.txt)
{CLAUDE_BIN_IN_CONTAINER} -p --dangerously-skip-permissions "$PROMPT"
"""
            script_b64 = base64.b64encode(run_script.encode("utf-8")).decode("ascii")
            ops.exec_sh(
                container,
                f"echo '{script_b64}' | base64 -d > /tmp/run_claude.sh && chmod +x /tmp/run_claude.sh && chown claude:claude /tmp/run_claude.sh",
                check=False,
            )

            # 以 claude 用户身份执行脚本
            output = ops.exec_sh(container, "su claude -c '/tmp/run_claude.sh'", check=False)
            (instance_res_dir / "run.log").write_text(output, encoding="utf-8")

            patch_out = ops.exec_sh(container, "cd /testbed && git diff", check=False)
            if patch_out.strip():
                (instance_res_dir / f"{instance_id}.patch").write_text(
                    patch_out, encoding="utf-8"
                )
                print(f"✅ Patch saved: {instance_id}")
            else:
                print(f"⚠️  No patch generated for {instance_id}")

        except Exception as e:  # noqa: BLE001
            print(f"Error running {instance_id}: {e}")
            traceback.print_exc()
        finally:
            ops.stop_and_remove(container)

    def run_all(self) -> None:
        self.ensure_agent_image_and_cache()
        self.pull_images()

        if self.skip_completed:
            completed = [iid for iid in self.instance_ids if self._is_instance_completed(iid)]
            remaining = [iid for iid in self.instance_ids if not self._is_instance_completed(iid)]
            print(
                f"📊 Status: {len(completed)} completed, {len(remaining)} remaining "
                f"(total: {len(self.instance_ids)})"
            )
            if not remaining:
                print("✅ All instances already completed!")
                return
        else:
            print(
                f"Running {len(self.instance_ids)} instances with {self.max_workers} workers"
            )

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.run_one_instance, iid): iid for iid in self.instance_ids
            }
            for fut in tqdm(as_completed(futures), total=len(futures)):
                iid = futures[fut]
                try:
                    fut.result()
                except Exception as e:  # noqa: BLE001
                    print(f"Instance {iid} crashed: {e}")

    def collect_predictions(self, instance_ids: list[str] | None = None) -> Path:
        """收集所有 patch，生成 SWE-bench 兼容的 predictions.json。"""

        import json

        if instance_ids is None:
            instance_ids = [item["instance_id"] for item in self.dataset]

        predictions: list[dict[str, str]] = []
        found_count = 0
        missing_count = 0

        for instance_id in instance_ids:
            patch_path = self.task_results_dir / instance_id / f"{instance_id}.patch"
            if not patch_path.exists():
                missing_count += 1
                continue

            patch_content = patch_path.read_text(encoding="utf-8")
            if not patch_content.strip():
                missing_count += 1
                continue

            predictions.append(
                {
                    "instance_id": instance_id,
                    "model_name_or_path": "claude-code",
                    "model_patch": patch_content,
                }
            )
            found_count += 1

        predictions_path = self.task_results_dir / "predictions.json"
        with open(predictions_path, "w", encoding="utf-8") as f:
            json.dump(predictions, f, indent=2, ensure_ascii=False)

        print(f"✅ Collected {found_count} patches into {predictions_path}")
        if missing_count > 0:
            print(f"⚠️  {missing_count} instances have no patch")

        return predictions_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run Claude Code (official CLI) on SWE-bench instances using official "
            "SWE-bench Docker images (Pywen evaluation layout)."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--instance-ids",
        nargs="+",
        help=(
            "Specific instance IDs to run (e.g., django__django-11001). If not "
            "specified, runs all instances in dataset."
        ),
    )
    parser.add_argument(
        "--dataset",
        default="SWE-bench_Lite",
        choices=["SWE-bench", "SWE-bench_Lite", "SWE-bench_Verified"],
        help="Dataset to use",
    )
    parser.add_argument(
        "--max-workers", type=int, default=1, help="Number of parallel workers"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only run first N instances after filtering",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default=None,
        help="Regex to filter instance_id",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="expr",
        choices=["expr", "collect", "e2e"],
        help="Mode: expr=only generate patches, collect=only collect predictions, e2e=both",
    )
    parser.add_argument(
        "--run-id",
        type=str,
        default="claude-code",
        help="Run ID, used to name the results directory",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-run all instances, ignoring existing results",
    )


    args = parser.parse_args()

    if args.mode != "collect" and not args.instance_ids:
        print("⚠️  Warning: No --instance-ids specified. Will run ALL instances in dataset.")
        print(f"   Dataset: {args.dataset}")
        resp = input("   Continue? [y/N]: ")
        if resp.lower() != "y":
            print("Aborted.")
            return

    evaluator = ClaudeCodeBenchmarkEvaluation(
        benchmark="SWE-bench",
        working_dir="claude_workspace",
        dataset_name=args.dataset,
        max_workers=args.max_workers,
        instance_ids=args.instance_ids,
        pattern=args.pattern,
        limit=args.limit,
        force=args.force,
        run_id=args.run_id,
    )

    if args.mode in ("expr", "e2e"):
        evaluator.run_all()

    if args.mode in ("collect", "e2e"):
        evaluator.collect_predictions(args.instance_ids)


if __name__ == "__main__":
    main()
