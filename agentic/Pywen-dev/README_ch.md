# Pywen

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Python 3.12-](https://img.shields.io/badge/python-3.12-red.svg)](https://www.python.org/downloads/)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Alpha](https://img.shields.io/badge/Status-Alpha-red)

**中文版** | [English](README.md)

![Pywen Logo](./docs/Pywen.png)

**Pywen** 是一个基于 **Qwen3-Coder** 的 Python CLI 工具，专为智能软件工程任务设计。它提供对话式界面，能够理解自然语言指令并通过先进的智能体系统执行复杂的开发工作流。

## 🧬 近期更新

- **最新**：重构核心智能体命名，从 QwenAgent 改为 PywenAgent，提升清晰度和一致性
- 2025.08.26 更新 `/agent` 模块，新增Claude Code智能体，执行逻辑对标Claude Code，实现task tool、todowrite tool等专有工具。你可以使用`/agent claude`切换为Claude Code智能体。
- 2025.08.08 更新 `/agent` 切换智能体模块，新增DeepResearch 智能体，执行逻辑对标Google开源的DeepResearch LangGraph版本。你可以使用`/agent research`切换为 GeminiResearchDemo 智能体。在你使用之前，请确保你具有serper api key。
- 2025.08.06 更新第一版Pywen，执行逻辑对标Gemini CLI/Qwen Code

## 🎯 项目背景

Pywen 核心基于[**Qwen3-Coder**](https://github.com/QwenLM/Qwen3-Coder)大语言模型，旨在为开发者提供一个高效、智能的代码助手。项目主要从[**Qwen-Code**](https://github.com/QwenLM/qwen-code)修改而来，针对 Python 开发者和 Qwen3-Coder 模型进行了深度优化。

### 为什么选择 Qwen3-Coder？

- 🚀 **代码专精**：Qwen3-Coder 在代码生成、理解和修复方面表现卓越
- ⚡ **高效推理**：优化的模型架构，提供快速响应
- 🔧 **工程实用**：专门针对实际软件开发场景训练

**项目状态：** 项目仍在积极开发中，欢迎您帮助我们改进 Pywen。

## 与其他 Code Agent CLI 的区别

Pywen 是一个基于 Python 开发的 CLI 工具，具有良好的 Python 生态兼容性和开发友好性。它提供 **透明、模块化的架构**，使研究人员和开发者可以轻松修改、扩展与分析，从而成为 **研究 AI Agent 架构、开展消融研究、开发新型 Agent 能力** 的理想平台。这种 **研究友好的设计**，让学术界与开源社区能够更便捷地为基础 Agent 框架做出贡献并构建创新应用，助力 AI Agent 快速发展领域的持续突破。


## ✨ 特性

- 🤖 **多智能体支持**：Pywen 智能体（基于 Qwen3-Coder）、Claude Code 智能体、Codex 智能体和研究智能体
- 🚀 **Qwen3-Coder-Plus 驱动**：基于阿里云最新的代码专用大模型
- 📦 **模块化**：基于模块化架构，可扩展和可定制
- 🛠️ **丰富的工具生态系统**：文件编辑、bash 执行、网络搜索、内存管理等
- 📊 **轨迹记录**：详细记录所有 Agent 操作以供调试和分析
- ⚙️ **智能配置**：基于 YAML 的配置系统，支持环境变量
- 📈 **会话统计**：实时跟踪 API 调用、工具使用和Token消耗
- 🔄 **智能体切换**：使用 `/agent` 命令在不同智能体间无缝切换

## 🚀 快速开始

### 安装

```bash 
pip install pywen
```

<details>
<summary>使用uv从源码开始构建 (recommended)</summary>

```bash
git clone https://github.com/PAMPAS-Lab/Pywen.git
cd Pywen
uv venv
uv sync --all-extras

# linux/macos
source .venv/bin/activate

# windows
.venv\Scripts\activate
```

</details>

### 首次使用

直接运行 `pywen` 命令即可启动：

```bash
# 交互模式（默认）
pywen

# 单次提示模式
pywen "创建一个 Python hello world 脚本"

# 指定智能体类型
pywen --agent pywen
pywen --agent claude
pywen --agent codex

# 通过命令行指定模型和 API 密钥
pywen --model "Qwen/Qwen3-Coder-Plus" --api_key "your-key"
```

如果是首次运行且没有配置文件：

- Pywen 会优先查找配置文件：
  - 默认路径：`~/.pywen/pywen_config.yaml`
  - 当前工作目录或父目录中的 `pywen_config.yaml`
- 如果都找不到，会尝试查找示例配置 `pywen_config.example.yaml`，并自动复制到默认路径：

```bash
# 在 Pywen 仓库根目录
cp pywen/config/pywen_config.example.yaml ~/.pywen/pywen_config.yaml
```

- 如果既没有实际配置文件，也找不到示例文件，则会报错提示，并给出两种解决方式：
  - 手动复制示例文件为 `pywen_config.yaml` 并编辑其中的 `api_key` / `model` 等字段
  - 或者通过环境变量直接提供配置（例如 `PYWEN_API_KEY` / `PYWEN_MODEL` / `PYWEN_BASE_URL`）

因此，**推荐做法** 是先根据示例文件或 README 的配置示例，准备好 `pywen_config.yaml` 或相关环境变量，然后再运行 `pywen`。

完成上述配置后，您就可以正常使用 Pywen 了。

### 基本用法

进入 Pywen 命令行界面后，您可以：

```bash
# 文件操作
> 创建一个计算斐波那契数列的 Python 脚本
> 重构 main.py 中的函数，让它们更加高效

# 代码分析和调试
> 修复这个项目中的 bug 并添加单元测试
> 分析我代码中的性能瓶颈

# 项目管理
> 建立一个具有合理结构的新 Flask Web 应用
> 为这个代码库添加全面的文档
```

## 📖 使用指南

### 命令行界面

#### 可用命令

```bash
# 系统命令
/about       show version info
/agent       switch between different agents (pywen/claude/codex/research)
/clear       clear the screen and conversation history
/help        for help on pywen code
/model       view and manage model configurations
/stats       check session stats
/tools       list available Pywen tools 
/bug         submit a bug report
/quit        exit the cli

# 特殊命令
!<command>   - Execute shell command

# 键盘快捷键
Ctrl+Y       - Toggle YOLO mode (auto-approve all operations - use with caution!)

# 直接输入任务描述即可执行智能体
```

#### 智能体切换

Pywen 支持多种专业化的智能体：

```bash
# 列出可用智能体
/agent

# 切换到 Pywen 智能体（默认，基于 Qwen3-Coder）
/agent pywen

# 切换到 Claude Code 智能体
/agent claude

# 切换到 Codex 智能体（OpenAI GPT-5 Codex）
/agent codex

# 切换到研究智能体（基于 Gemini）
/agent research
```

**可用智能体：**
- **Pywen 智能体** (`pywen`)：基于 Qwen3-Coder 的通用编程助手
- **Claude Code 智能体** (`claude`)：高级文件操作和项目理解能力
- **Codex 智能体** (`codex`)：基于 OpenAI Codex 的编程助手
- **研究智能体** (`research`)：多步骤研究智能体，用于全面信息收集

### YOLO 模式

**请谨慎使用：**
- 按 `Ctrl+Y` 切换 YOLO 模式
- 在 YOLO 模式下，所有工具调用都会自动批准，无需用户确认
- 这会加快执行速度，但移除了安全检查
- 模式激活时会在界面中显示状态

### 配置管理

Pywen 使用 YAML 格式的配置文件。默认配置文件位于 `~/.pywen/pywen_config.yaml`。

**配置示例：**

```yaml
# 默认使用的智能体
default_agent: pywen

# 模型配置
agents:
  # Pywen 智能体（Qwen3-Coder）
  - agent_name: pywen
    model: "Qwen/Qwen3-Coder-Plus"
    api_key: "your-api-key"
    base_url: "https://api-inference.modelscope.cn/v1"
    provider: openai
    wire_api: chat

  # Claude Code 智能体
  - agent_name: claude
    provider: anthropic
    model: "claude-3.5-sonnet"
    api_key: "your-anthropic-key"
    base_url: "https://api.anthropic.com/v1"
    wire_api: chat

  # Codex 智能体
  - agent_name: codex
    provider: openai
    model: "gpt-5.1"
    api_key: "your-openai-key"
    base_url: "https://api.openai.com/v1/"
    wire_api: responses

# 权限等级：locked / edit_only / planning / yolo
permission_level: locked

# 最大对话轮数
max_turns: 10

# 内存监控设置
memory_monitor:
  check_interval: 3
  maximum_capacity: 100000
  model: "Qwen/Qwen3-235B-A22B-Instruct-2507"
```

**配置优先级：**
1. 命令行参数（最高）
2. 配置文件值
3. 环境变量
4. 默认值（最低）

**配置文件位置：**
- 默认：`~/.pywen/pywen_config.yaml`
- 可以使用 `--config` 参数指定自定义路径

### 环境变量

您可以通过环境变量设置 API 密钥。Pywen 支持智能体特定的环境变量：

```bash
# Pywen 智能体（Qwen3-Coder）
export PYWEN_PYWEN_API_KEY="your-api-key"
export PYWEN_PYWEN_BASE_URL="https://api-inference.modelscope.cn/v1"
export PYWEN_PYWEN_MODEL="Qwen/Qwen3-Coder-Plus"

# Claude 智能体
export PYWEN_CLAUDE_API_KEY="your-anthropic-key"
export PYWEN_CLAUDE_BASE_URL="https://api.anthropic.com/v1"
export PYWEN_CLAUDE_MODEL="claude-3.5-sonnet"

# Codex 智能体
export PYWEN_CODEX_API_KEY="your-openai-key"
export PYWEN_CODEX_BASE_URL="https://api.openai.com/v1/"
export PYWEN_CODEX_MODEL="gpt-5.1"

# 通用回退（如果未设置智能体特定变量）
export PYWEN_API_KEY="your-api-key"
export PYWEN_BASE_URL="https://api-inference.modelscope.cn/v1"

# 工具 API 密钥（可选但推荐）
export SERPER_API_KEY="your-serper-api-key"  # 用于网络搜索
export JINA_API_KEY="your-jina-api-key"      # 用于内容读取
```

**环境变量格式：**
- 智能体特定：`PYWEN_<智能体名称>_<字段>`（例如：`PYWEN_PYWEN_API_KEY`）
- 通用：`PYWEN_<字段>`（如果未设置智能体特定变量则使用此回退）

## 🛠️ 可用工具

Pywen 为软件开发提供了全面的工具包。不同的智能体可能具有不同的工具访问权限：

**通用工具（大多数智能体可用）：**
- **文件操作**：`read_file`、`write_file`、`edit`、`read_many_files`
- **文件系统**：`ls`、`glob`、`grep`
- **Bash 执行**：`bash` - 运行 shell 命令和脚本
- **网络操作**：`web_search`、`web_fetch`
- **内存管理**：`memory` - 存储和检索信息

**智能体特定工具：**
- **Claude 智能体**：`task`、`todo` - 任务规划和管理
- **Codex 智能体**：`update_plan`、`apply_patch` - Codex 特定操作
- **研究智能体**：专业化的研究工作流工具

有关所有可用工具及其功能的详细信息，请参阅 [docs/tools.md](docs/tools.md)。

## 🔌 MCP（Model Context Protocol）集成

Pywen 还支持 **MCP（Model Context Protocol）**，可用于连接外部工具和服务，例如浏览器。

### 启用 MCP
1. 打开配置文件：
   ```bash
   ~/.pywen/pywen_config.yaml
   ```
2. 找到 `mcp` 配置并启用：
   ```yaml
   mcp:
     enabled: true
     isolated: false
     servers:
       - name: "playwright"
         command: "npx"
         args:
           - "@playwright/mcp@latest"
         enabled: true
         include:
           - "browser_*"
         save_images_dir: "./outputs/playwright"
   ```
### 安装 Node.js 环境

确保你的设备已安装 Node.js。你可以通过以下命令验证：
```bash
node -v 
```
如果没有安装，请按照 [Node.js 安装指南](https://nodejs.org)安装

### 浏览器依赖

如果你的设备没有安装浏览器，可以使用以下命令为 Playwright 安装浏览器：
```bash
npx playwright install --with-deps
```
这将安装 Chromium 浏览器并解决所有 Playwright 所需的系统依赖。
启用 MCP 并安装所需浏览器后，Pywen 将能够调用 playwright MCP 服务端来执行浏览器自动化、截图捕获以及网页交互等任务。


## 📊 轨迹记录

Pywen 自动记录详细的执行轨迹以供调试和分析：

```bash
# 轨迹文件自动保存到 trajectories/ 目录
trajectories/trajectory_xxxxxx.json
```

轨迹文件包含：
- **LLM 交互**：所有消息、响应和工具调用
- **智能体步骤**：状态转换和决策点
- **工具使用**：调用了哪些工具及其结果
- **元数据**：时间戳、Token使用量和执行指标

## 📈 会话统计

通过实时统计监控您的使用情况：

```bash
> /stats
```

跟踪：
- API 调用和Token消耗
- 工具使用模式
- 会话持续时间
- 模型性能指标

## 🤝 贡献

我们欢迎为 Pywen 做出贡献！以下是开始的方法：

1. Fork 仓库
2. 设置开发环境：
   ```bash
   git clone https://github.com/your-username/Pywen.git
   cd Pywen
   uv venv
   uv sync --all-extras
   ```
3. 创建功能分支
4. 进行更改并添加测试
5. 提交拉取请求

### 开发指南

- 遵循 PEP 8 风格指南
- 为新功能添加测试
- 根据需要更新文档
- 适当使用类型提示
- 确保所有测试在提交前通过

## 📋 要求

- Python 3.10+,<3.13
- 所选智能体的 API 密钥：
  - **Pywen 智能体**：ModelScope API 密钥或通义千问 API 密钥
  - **Claude 智能体**：Anthropic API 密钥
  - **Codex 智能体**：OpenAI API 密钥
  - **研究智能体**：Google API 密钥（以及用于网络搜索的 Serper API 密钥）
- 用于 API 访问的互联网连接
- （可选）Node.js 用于 MCP 服务器支持

## 🔧 故障排除

### 常见问题

**配置问题：**
```bash
# 使用默认配置重新生成配置
rm ~/.pywen/pywen_config.yaml
pywen
```

**API 密钥问题：**
```bash
# 验证您的 API 密钥已设置（Pywen 智能体）
echo $PYWEN_PYWEN_API_KEY

# 或检查通用回退
echo $PYWEN_API_KEY

# 在 Pywen 中检查配置
> /model
```

**智能体切换问题：**
```bash
# 列出可用智能体
> /agent

# 检查当前智能体类型
> /stats
```


## 🙏 致谢

我们感谢：

- **Google** 的[Gemini CLI](https://github.com/google-gemini/gemini-cli)项目，为本项目提供了智能体执行逻辑和丰富的工具生态库
- **阿里云通义千问团队** 提供强大的 [Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder) 模型和 [Qwen-Code](https://github.com/QwenLM/qwen-code) 参考实现
- **ByteDance** 的 [trae-agent](https://github.com/bytedance/trae-agent) 项目，为本项目提供了宝贵的基础架构
- **Yuyz0112** 的 [claude-code-reverse](https://github.com/Yuyz0112/claude-code-reverse)项目和 **shareAI-lab** 的 [Kode](https://github.com/shareAI-lab/Kode)项目，为本项目的claude code智能体开发提供思路

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

**Pywen - 让 Qwen3-Coder 的强大能力触手可及，助力智能软件开发！** 🚀

**PAMPAS-Lab - 致力于大模型智能体框架突破，为 AI 研究与应用架桥铺路！** 🚀

---

## 🌟Star History

[![Star History Chart](https://api.star-history.com/svg?repos=PAMPAS-Lab/Pywen&type=Date)](https://www.star-history.com/#PAMPAS-Lab/Pywen&Date)
