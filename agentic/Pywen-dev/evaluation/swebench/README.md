# Pywen × SWE-bench：容器化运行指南

---

## 一、先决条件

* 操作系统：Linux / macOS（Windows 需 WSL2）
* Docker ≥ 20.10
* 网络能访问 Docker Hub（拉取 SWE-bench 镜像）
* 已准备好 **Pywen 配置文件** `pywen_config.yaml`

  运行时通过 `--config` 指向自定义路径，比如自己的 `~/.pywen/pywen_config.yaml`

---

## 二、安装依赖

评估功能需要额外的可选依赖：

```bash
# 使用 uv（推荐）
uv sync --extra evaluation

# 或使用 pip
pip install -e ".[evaluation]"
```

可选依赖包括：
- `sb-cli`：SWE-bench 云端评估提交
- `docker`：Docker Python SDK
- `tqdm`：进度条
- `datasets`：HuggingFace datasets

---

## 三、目录结构（关键路径）

```
Pywen/
├─ Dockerfile.pywen-agent      # 构建 Pywen Agent 镜像
├─ pyproject.toml
├─ uv.lock
├─ .python-version             # 指定 Python 版本（3.12.x）
├─ pywen/                      # Pywen 源码
├─ pywen_config.example.yaml   # 配置模板
└─ evaluation/
   └─ run_evaluation.py        # 评测脚本（SWE-bench）
```

运行后脚本会在工作目录下生成缓存与结果：

```
evaluation/
├─ pywen_workspace/pywen_agent_cache/
│  ├─ Pywen/                # 映射到容器 /opt/Pywen（含 .venv）
│  ├─ uv_bin/uv             # 映射到容器 /root/.local/bin/uv
│  └─ uv_share/uv/...       # 映射到容器 /root/.local/share/uv（含托管 CPython）
└─ results/
   └─ SWE-bench_.../        # 每个实例的日志、patch、predictions.json 等
```

---

## 四、构建镜像（一次性）

在项目根目录执行：

```bash
docker build -f Dockerfile.pywen-agent -t pywen/agent:0.1 .
```

如果需要重新构建镜像（比如Pywen代码修改更新等）：

```bash
docker build --no-cache -f Dockerfile.pywen-agent -t pywen/agent:0.1 .
```

镜像中包含：

* `/opt/Pywen/.venv`（venv；其 python 为 uv 的 shim）
* `/root/.local/bin/uv`
* `/root/.local/share/uv`（**托管的 CPython 3.12 + 轮子缓存**）

> 镜像构建时 **不会 apt 安装 python**。uv 会根据 `.python-version` 自动下载 manylinux 预编译的 CPython 3.12。

---

## 五、运行方式

### 1）快速开始（推荐先试）

```bash
cd Pywen

# 跑 2 个实例试试
python evaluation/run_evaluation.py \
  --config ~/.pywen/pywen_config.yaml \
  --limit 2 \
  --mode e2e
```

### 2）跑指定实例

```bash
python evaluation/run_evaluation.py \
  --config ~/.pywen/pywen_config.yaml \
  --instance-ids django__django-11001 astropy__astropy-12907
```

### 3）跑 50 个实例（并行）

```bash
python evaluation/run_evaluation.py \
  --config ~/.pywen/pywen_config.yaml \
  --limit 50 \
  --max-workers 4 \
  --mode e2e
```

---

## 六、参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--dataset` | `SWE-bench_Lite` | 数据集：`SWE-bench` / `SWE-bench_Lite` / `SWE-bench_Verified` |
| `--config` | `~/.pywen/pywen_config.yaml` | Pywen 配置文件路径 |
| `--agent` | `pywen` | Agent 类型：`pywen` / `codex` / `claude` |
| `--instance-ids` | - | 指定实例 ID（空则跑全量） |
| `--pattern` | - | 用正则匹配实例 ID |
| `--limit` | - | 最多跑多少个实例 |
| `--max-workers` | `1` | 并发数 |
| `--mode` | `expr` | 运行模式（见下表） |
| `--run-id` | `pywen-agent` | 运行标识符 |
| `--force` | `False` | 强制重跑所有实例（默认会跳过已完成的） |

### 运行模式

| 模式 | 说明 |
|------|------|
| `expr` | 只生成 patch |
| `collect` | 只收集已有 patch 成 `predictions.json` |
| `e2e` | 生成 patch + 收集 |

### 断点续跑

默认会自动跳过已完成的实例（存在 patch 或 run.log），中断后再次运行会从上次的进度继续：

```bash
# 第一次运行（假设跑了 30 个后中断）
python evaluation/run_evaluation.py --limit 100

# 再次运行，会自动跳过已完成的 30 个，继续剩余 70 个
python evaluation/run_evaluation.py --limit 100

# 如果想强制重跑所有（忽略已有结果）
python evaluation/run_evaluation.py --limit 100 --force
```

---

## 七、提交云端评估

生成 `predictions.json` 后，可以提交到 SWE-bench 云端评估：

```bash
# 提交到 SWE-bench Lite（test 分割）
sb-cli submit swe-bench_lite test \
    --predictions_path evaluation/results/SWE-bench_SWE-bench_Lite_pywen-agent/predictions.json \
    --run_id my_run_name
```

**数据集对照表**：

| 你跑的 --dataset | sb-cli 参数 |
|------------------|-------------|
| `SWE-bench_Lite` | `swe-bench_lite test` |
| `SWE-bench_Verified` | `swe-bench_verified test` |
| `SWE-bench` | `swe-bench-m test` |

---

## 八、工作原理（简述）

1. **构建阶段**：用 uv 根据 `.python-version` 下载 **CPython 3.12（manylinux 预编译）**，创建 `.venv` 并安装依赖。
2. **导出缓存**：从构建镜像把 `/opt/Pywen`、`/root/.local/bin/uv`、`/root/.local/share/uv` 拷贝到宿主 `pywen_agent_cache/`。
3. **运行阶段**：每个 SWE 实例容器挂载三处缓存；在容器内以 **`/opt/Pywen/.venv/bin/pywen ...`** 直接运行（不需要 `source activate`）。
4. `.venv/bin/python` 是 uv 的 **shim**，会解析到挂载的 `~/.local/share/uv/python/.../bin/python`，避免依赖实例容器的系统 Python/`libpython3.12.so`。

---

## 九、手动调试（可选）

想进入某个 SWE 实例容器手动跑 Pywen，可参考：

```bash
docker run --rm -it \
  -v "$(pwd)/pywen_workspace/pywen_agent_cache/Pywen":/opt/Pywen:ro \
  -v "$(pwd)/pywen_workspace/pywen_agent_cache/uv_bin":/root/.local/bin:ro \
  -v "$(pwd)/pywen_workspace/pywen_agent_cache/uv_share":/root/.local/share:ro \
  -v "$(pwd)/results/demo":/results:rw \
  --workdir /testbed \
  swebench/sweb.eval.x86_64.<instance_id>:latest \
  bash

# 容器里：
/opt/Pywen/.venv/bin/pywen --config /results/pywen_config.yaml --agent pywen --permission-mode yolo
```

---

## 十、清理

```bash
# 删除导出的缓存（会在下次运行时自动重新导出）
rm -rf pywen_workspace/pywen_agent_cache

# 删除评测结果
rm -rf results
```
