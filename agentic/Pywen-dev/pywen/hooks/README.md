# Hooks 使用指南

本文档介绍如何在 **Pywen** 中使用 Hook 机制。

---

## 概览

* 配置文件：`~/.pywen/pywen_hooks.json`
* 入口：`HookManager.emit(event, ...)`
* 事件：
  * 无 matcher：`UserPromptSubmit`、`Stop` 等
  * 有 matcher（按工具名匹配）：`PreToolUse`、`PostToolUse`
* I/O 协议：Hook 从 **stdin** 接收 JSON；通过 **stdout/stderr + exit code** 或 **JSON stdout** 反馈决策与提示
* 已去除：`transcript_path`、`PYWEN_PROJECT_DIR`（脚本不应依赖项目根）

---

## 快速开始

### 1) 在pywen配置目录添加 `pywen_hooks.json`

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "./.pywen/hooks/prompt_guard.py" } ] }
    ],
    "PreToolUse": [
      {
        "matcher": "bash|write_file|edit",
        "hooks": [ { "type": "command", "command": "./.pywen/hooks/pre_check.py", "timeout": 5 } ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "write_file|edit|bash",
        "hooks": [ { "type": "command", "command": "./.pywen/hooks/post_audit.py" } ]
      }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "./.pywen/hooks/stop_test.py" } ] }
    ]
  }
}
```

> `matcher`：仅 `PreToolUse`/`PostToolUse` 使用；大小写敏感。支持精确、正则、`*`/空（全匹配）。

### 2) 脚本权限

```bash
chmod +x ./.pywen/hooks/*.py
```

### 3) Qwen Agent 已接入

* 工具执行前：触发 `PreToolUse`（阻断时展示原因并跳过真实工具）
* 工具执行后：触发 `PostToolUse`（可追加上下文、可阻断后续处理）
* 用户提交：触发 `UserPromptSubmit`（可追加上下文或阻断）
* 回合结束：触发 `Stop`（可见提示或阻断“停止”让代理续写）

---

## Hook 输入（stdin JSON）

所有事件共有字段：

```json
{
  "session_id": "abc123",
  "cwd": "/current/working/dir",
  "hook_event_name": "PreToolUse" // or PostToolUse / UserPromptSubmit / Stop ...
}
```

额外字段：

* **PreToolUse**：`tool_name: str`, `tool_input: dict`
* **PostToolUse**：`tool_name: str`, `tool_input: dict`, `tool_response: dict`
* **UserPromptSubmit**：`prompt: str`
* **Stop**：`stop_hook_active: bool`

---

## Hook 输出（两种方式）

### A. 简单模式：退出码 + 文本

* `exit 0`：成功（不阻断）。`stdout` 对于某些事件不会自动注入；`stderr` 可在 UI 中显示（取决于你的打印逻辑，当前实现 **会显示**）。
* `exit 2`：**阻断**。`stderr` 会作为原因反馈给用户/代理。
* 其他非 0：不阻断，但把 `stderr` 展示给用户（“可见但不拦”）。

### B. 高级模式：JSON 到 `stdout`

* 通用字段：

  ```json
  {
    "continue": true,                // 设为 false 可直接让上游停止后续流程
    "stopReason": "string",          // 展示给用户
    "systemMessage": "string"        // 在 UI 中可见的横幅/提示
  }
  ```
* **PreToolUse** 专属：

  ```json
  {
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "allow" | "deny" | "ask",
      "permissionDecisionReason": "string"
    }
  }
  ```
* **PostToolUse** 专属：

  ```json
  {
    "decision": "block",             // 或省略（不阻断）
    "reason": "string",
    "hookSpecificOutput": {
      "hookEventName": "PostToolUse",
      "additionalContext": "string"  // 将被注入为 system 消息
    }
  }
  ```
* **UserPromptSubmit**：

  ```json
  {
    "decision": "block",
    "reason": "string",
    "hookSpecificOutput": {
      "hookEventName": "UserPromptSubmit",
      "additionalContext": "string"
    }
  }
  ```
* **Stop**：

  ```json
  { "decision": "block", "reason": "string" }
  ```

---

## 示例脚本

### 1) UserPromptSubmit（不阻断 + 注入上下文）

`./.pywen/hooks/prompt_guard.py`

```python
#!/usr/bin/env python3
import json, re, sys, datetime
d = json.load(sys.stdin)
p = d.get("prompt","")

if re.search(r"(?i)\b(password|api[_-]?key|secret|token)\s*[:=]", p):
    print(json.dumps({"decision":"block","reason":"Prompt contains potential secrets. Please remove them."}))
    sys.exit(0)

print(json.dumps({
  "systemMessage": "🛈 Prompt checked by hook.",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": f"[HOOK] Time={datetime.datetime.now().isoformat()}"
  }
}))
sys.exit(0)
```

### 2) PreToolUse（显示但不阻断）

`./.pywen/hooks/pre_check.py`

```python
#!/usr/bin/env python3
import json, sys
d = json.load(sys.stdin)
tool = d.get("tool_name")
inp  = d.get("tool_input", {})
print(f"✅ [PreToolUse] {tool} about to run, input={inp}", file=sys.stderr)
sys.exit(1)  # 非 0 且 != 2 => 不阻断，但用户可见
```

> 若要阻断，改为输出：
>
> ```python
> print(json.dumps({
>   "hookSpecificOutput":{
>     "hookEventName":"PreToolUse",
>     "permissionDecision":"deny",
>     "permissionDecisionReason":"Dangerous command detected."
>   }
> }))
> sys.exit(0)
> ```

### 3) PostToolUse（追加上下文 + 可见横幅，不阻断）

`./.pywen/hooks/post_audit.py`

```python
#!/usr/bin/env python3
import json
d = json.load(sys.stdin)
tool = d.get("tool_name")
print(json.dumps({
  "systemMessage": f"📣 [PostToolUse] {tool} finished.",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": f"[HOOK] {tool} completed successfully."
  }
}))
sys.exit(0)
```

> 若要“拦回去”（判定失败），可：
>
> ```python
> print(json.dumps({"decision":"block","reason":"Lint failed: please fix format"}))
> sys.exit(0)
> ```

### 4) Stop（不阻断但可见）

`./.pywen/hooks/stop_test.py`

```python
#!/usr/bin/env python3
import sys
print("✅ [Stop] hook executed (non-blocking).", file=sys.stderr)
sys.exit(1)
```

> 若要要求继续（阻断停止）：
>
> ```python
> print(json.dumps({"decision":"block","reason":"Please continue with a short summary."}))
> sys.exit(0)
> ```

---

## 触发与可见性

* 你的 Qwen agent 已在工具前后触发 `PreToolUse`/`PostToolUse`，并在控制台打印 hook 返回的 `msg`；阻断时会返回“失败的工具结果/错误事件”，用户能直接看到原因。
* `UserPromptSubmit` 在进入 agent 处理前触发；`systemMessage`/`stderr` 会显示；`additionalContext` 以 **system** 注入。
* `Stop` 在一轮完成时触发；`stderr` 或 `systemMessage` 会显示；`block` 会阻断停止（若上层支持续写逻辑则继续一轮）。

---

## matcher 速记

* 仅用于 `PreToolUse`/`PostToolUse`：与 `tool_name` 全匹配（大小写敏感）
* 支持：

  * 精确：`"write_file"`
  * 正则：`"edit|write_file"`
  * 全匹配：`"*"`、`""`、或省略

确保与你工具注册名一致（例如 `"bash"`, `"write_file"`, `"edit"` …）。

---

## 常见问题与排错

1. **看不到 hook 输出**

   * 确认 agent 侧在 `ok=True` 时也会打印 `msg`（你当前实现已处理）。
   * 确认脚本有执行权限、路径正确。
   * 排查 `matcher` 是否命中相应 `tool_name`。

2. **PreToolUse 阻断但仍执行了工具**

   * 确认 agent 在 `pre_ok=False` 时 `continue` 跳过真实执行（你的实现已处理）。
   * 脚本用 `exit 2` 或 JSON 的 `permissionDecision: "deny"`。

3. **PostToolUse 阻断无效**

   * 脚本需输出 `{"decision":"block","reason":"..."}`；agent 将结果改写为失败并展示原因（你的实现已处理）。

4. **脚本报 `126`**（找到但不可执行）

   * 给执行权限或用 `python script.py` 调用；加 shebang `#!/usr/bin/env python3`。

---

## 最小自测（不走 LLM）

```python
ok, msg, extra = hook_mgr.emit(
    HookEvent.PreToolUse,
    base_payload={"session_id":"test","cwd":os.getcwd()},
    tool_name="bash",
    tool_input={"command":"echo ok"}
)
print("PRE:", ok, msg)

ok, msg, extra = hook_mgr.emit(
    HookEvent.PostToolUse,
    base_payload={"session_id":"test","cwd":os.getcwd()},
    tool_name="bash",
    tool_input={"command":"echo ok"},
    tool_response={"success": True, "result":"ok", "error": None}
)
print("POST:", ok, msg, extra)
```
