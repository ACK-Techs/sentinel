# Pywen × BFCL：函数调用评估指南

---

## 一、先决条件

* 操作系统：Linux / macOS / Windows
* Python ≥ 3.11
* Git（用于自动下载数据集）
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
- `datasets`：HuggingFace datasets（用于加载数据集）
- `tqdm`：进度条显示

---

## 三、目录结构

```
Pywen/
├─ pywen/                      # Pywen 源码
├─ pywen_config.example.yaml   # 配置模板
└─ evaluation/
   └─ bfcl/
      ├─ run_bfcl_evaluation.py  # 评估脚本
      ├─ dataset.py              # 数据集加载
      ├─ evaluator.py            # 评估逻辑
      ├─ adapter.py              # LLM 适配器
      ├─ gorilla/                # 自动下载的 BFCL 数据集（首次运行后生成）
      └─ results/                # 评估结果输出目录
```

---

## 四、运行方式

### 1）快速开始（推荐先试）

```bash
cd Pywen

# 评估 5 个样本
python evaluation/bfcl/run_bfcl_evaluation.py \
  --category simple_python \
  --samples 5 \
  --config ~/.pywen/pywen_config.yaml
```

### 2）评估所有样本

```bash
python evaluation/bfcl/run_bfcl_evaluation.py \
  --category simple_python \
  --samples 0 \
  --config ~/.pywen/pywen_config.yaml
```

### 3）评估多个类别

```bash
# 评估多个类别（循环运行）
for category in simple_python multiple parallel; do
  python evaluation/bfcl/run_bfcl_evaluation.py \
    --category $category \
    --samples 10 \
    --config ~/.pywen/pywen_config.yaml
done
```

---

## 五、参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--category` | `simple_python` | 评估类别（见下表） |
| `--samples` | `5` | 评估样本数（`0` 表示全部） |
| `--data-dir` | - | BFCL 数据目录路径（默认自动下载） |
| `--config` | `~/.pywen/pywen_config.yaml` | Pywen 配置文件路径 |
| `--output-dir` | `evaluation/bfcl/results` | 输出目录路径 |

### 支持的评估类别

| 类别 | 说明 |
|------|------|
| `simple_python` | 简单的 Python 函数调用 |
| `multiple` | 多函数调用场景 |
| `parallel` | 并行函数调用 |
| `parallel_multiple` | 并行多函数调用 |
| `java` | Java 函数调用 |
| `javascript` | JavaScript 函数调用 |
| `live_simple` | 实时 API 简单调用 |
| `live_multiple` | 实时 API 多函数调用 |
| `live_parallel` | 实时 API 并行调用 |
| `live_parallel_multiple` | 实时 API 并行多函数调用 |
| `live_relevance` | 实时 API 相关函数调用 |
| `live_irrelevance` | 实时 API 无关函数调用 |
| `irrelevance` | 无关函数调用 |
| `multi_turn_base` | 多轮对话基础场景 |
| `multi_turn_miss_func` | 多轮对话缺失函数 |
| `multi_turn_miss_param` | 多轮对话缺失参数 |
| `multi_turn_long_context` | 多轮对话长上下文 |

---

## 六、输出结果

评估完成后会在输出目录生成两个文件：

### 1. 详细结果 JSON

文件：`bfcl_{category}_detailed.json`

包含完整的评估结果，包括每个样本的详细信息：

```json
{
  "total_samples": 10,
  "correct_samples": 8,
  "overall_accuracy": 0.8,
  "category_metrics": {
    "simple_python": {
      "total": 10,
      "correct": 8,
      "accuracy": 0.8
    }
  },
  "results": [
    {
      "sample_id": "sample_1",
      "category": "simple_python",
      "correct": true,
      "model_output": "math.factorial(5)",
      "expected": ["math.factorial(5)"],
      "latency_ms": 1234.56
    }
  ]
}
```

### 2. BFCL 格式结果

文件：`BFCL_v4_{category}_result.json`

标准 BFCL 格式，可用于提交到排行榜：

```json
[
  {
    "id": "sample_1",
    "result": "math.factorial(5)",
    "correct": true
  }
]
```

---

## 七、评估模式

评估器支持两种评估模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `ast` | 使用 Python AST 解析和比较函数调用 | 默认模式，能处理不同格式的等价调用 |
| `exact` | 直接比较输出字符串 | 需要完全匹配的场景 |

默认使用 AST 匹配模式，能够处理：
- 不同格式的函数调用（代码块、JSON、纯文本）
- 参数顺序不同的等价调用
- 带命名参数的调用

如需修改评估模式，可在代码中设置：

```python
from evaluation.bfcl.evaluator import BFCLEvaluator

evaluator = BFCLEvaluator(
    dataset=dataset,
    category="simple_python",
    evaluation_mode="ast"  # 或 "exact"
)
```

---

## 八、工作原理（简述）

1. **数据集加载**：首次运行自动从 GitHub 克隆 BFCL 数据集（使用 sparse checkout，仅下载数据目录）
2. **LLM 调用**：通过适配器将 Pywen 的 LLMClient 转换为 BFCL 评估接口
3. **结果评估**：使用 AST 解析或精确匹配比较模型输出与标准答案
4. **报告生成**：生成包含准确率、延迟等指标的详细报告，并导出标准 BFCL 格式

---

## 九、代码中使用

除了命令行，也可以在代码中直接使用：

```python
from evaluation.bfcl.run_bfcl_evaluation import run_bfcl_evaluation

# 运行评估
results = run_bfcl_evaluation(
    category="simple_python",
    max_samples=10,
    config_path="~/.pywen/pywen_config.yaml",
    output_dir="./results"
)

# 查看结果
print(f"准确率: {results['overall_accuracy']:.2%}")
print(f"正确数: {results['correct_samples']}/{results['total_samples']}")
```

### 使用底层 API

```python
from evaluation.bfcl.dataset import BFCLDataset
from evaluation.bfcl.evaluator import BFCLEvaluator
from evaluation.bfcl.adapter import create_bfcl_adapter
from pywen.llm.llm_client import LLMClient
from pywen.config.manager import ConfigManager

# 创建 LLM 客户端
config = ConfigManager().resolve_effective_config(None)
llm_client = LLMClient(config.active_model)

# 创建适配器
adapter = create_bfcl_adapter(llm_client, config.active_model.model)

# 加载数据集
dataset = BFCLDataset(category="simple_python", auto_download=True)

# 创建评估器
evaluator = BFCLEvaluator(dataset=dataset, category="simple_python")

# 运行评估
results = evaluator.evaluate(agent=adapter, max_samples=10)
```

---

## 十、常见问题

### Q: 数据集下载失败怎么办？

A: 确保已安装 git，并且网络可以访问 GitHub。也可以手动下载数据集：

```bash
cd evaluation/bfcl
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/ShishirPatil/gorilla.git gorilla

cd gorilla
git sparse-checkout set berkeley-function-call-leaderboard/bfcl_eval/data
```

### Q: 评估结果不准确怎么办？

A: 
1. 检查模型配置是否正确（`--config` 参数）
2. 尝试不同的评估模式（AST vs 精确匹配）
3. 查看详细结果 JSON 中的 `model_output` 和 `expected` 字段
4. 检查函数定义是否正确传递

### Q: 如何批量评估所有类别？

A: 编写脚本循环运行：

```bash
for category in simple_python multiple parallel java javascript; do
  python evaluation/bfcl/run_bfcl_evaluation.py \
    --category $category \
    --samples 0 \
    --config ~/.pywen/pywen_config.yaml
done
```

---

## 十一、清理

```bash
# 删除下载的数据集（会在下次运行时自动重新下载）
rm -rf evaluation/bfcl/gorilla

# 删除评估结果
rm -rf evaluation/bfcl/results
```

---

## 参考

- [Berkeley Function Call Leaderboard](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard)
- [Pywen 文档](../README.md)
