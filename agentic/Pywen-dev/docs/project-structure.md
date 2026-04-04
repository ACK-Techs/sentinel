# Pywen 项目结构说明

```
Pywen/
├── agents/                             # 智能体系统
|   └── qwen/                           # Qwen 智能体实现
|       ├── qwen_agent.py               # Qwen 智能体主类
|       ├── turn.py                     # Qwen 智能体回合管理
|       ├── task_continuation_checker.py    # 任务续写检查
|       └── loop_detection_service.py   # Qwen 智能体循环检测服务
|   base_agent.py                       # 基础智能体类
├── config/                             # 智能体配置管理模块
│   ├── config.py                       # 配置类定义，支持环境变量和配置文件加载
|   └── loader.py                       # 智能体配置加载器
├── core/                               # 智能体核心模块
│   ├── client.py                       # 智能体级LLM 客户端，用于与大模型交互
│   ├── tool_scheduler.py               # 工具调度器
│   ├── tool_executor.py                # 工具执行器
│   ├── tool_registry.py                # 工具注册器
|   └── trajectory_recorder.py          # 轨迹记录器
├── tools/                              # 工具生态系统
│   ├── base.py                         # 工具基类，定义所有工具的抽象接口
│   ├── bash_tool.py                    # Shell 命令执行工具
│   ├── edit_tool.py                    # 文件编辑工具
│   ├── file_tools.py                   # 文件工具（写文件、读文件）
│   ├── glob_tool.py                    # 文件 glob 工具
│   ├── grep_tool.py                    # 文件 grep 工具
│   ├── ls_tool.py                      # 文件 ls 命令工具
│   ├── memory_tool.py                  # 内存工具
│   ├── read_many_files_tool.py         # 批量读取文件工具
│   ├── web_fetch_tool.py               # 网络抓取工具
│   └── web_search_tool.py              # 网络搜索工具（基于 Serper API）
├── docs/                               # 项目文档
│   └── project-structure.md            # 项目结构说明文档
├── trajectories/                       # 执行轨迹记录（自动生成）
│   └── trajectory_xxxxxx.json          # 单次会话的完整执行轨迹，包含 LLM 交互和工具调用
├── ui/                                 # CLI 界面
|   ├── commands/                       # 命令模块  
|   |   ├── __init__.py                 # 命令模块入口
|   |   ├── about_command.py            # 关于版本命令
|   |   ├── auth_command.py             # 配置信息命令
|   |   ├── base_command.py             # 命令基类
|   |   ├── clear_command.py            # 清空命令
|   |   ├── help_command.py             # 帮助命令
|   |   ├── memory_command.py           # 记忆命令
|   |   ├── quit_command.py             # 退出命令
|   |   └── ...
|   |── utils/                          # 界面工具模块
|   |   └── keyboard.py                 # 键盘绑定
│   ├── cli_console.py                  # CLI 界面实现
│   ├── command_processor.py            # 命令处理
|   └── config_wizard.py                # 配置向导│   
├── utils                               # 系统级工具模块
|   ├── __init__.py
|   ├── base_content_generator.py       # 抽象类，用于生成内容
|   ├── qwen_content_generator.py       # Qwen 模型内容生成
|   ├── llm_basics.py                   # LLM 基础数据结构
|   ├── llm_client.py                   # LLM 客户端
|   ├── llm_config.py                   # LLM 配置
|   └── token_limits.py                 # Token 限制管理
├── cli.py                              # CLI 入口点，支持 `pywen` 启动
├── pyproject.toml                      # 项目配置文件（依赖管理、构建配置、开发工具配置）
├── README.md                           # 项目说明（英文）
├── README_ch.md                        # 项目说明（中文）
└── pywen_config.json                   # 运行时配置文件（API 密钥、模型设置、用户偏好）
```