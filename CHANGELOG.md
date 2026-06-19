# Changelog

格式基于 [Keep a Changelog](https://keepachangelog.com/)。

---

## [0.1.0] - 2026-06-19

### 项目起源

本项目经历了多次重构，分支历史如下：

| 分支 | 说明 | 状态 |
|------|------|------|
| `main` | 旧版 `rootengine-core`（0.5.x），已废弃 | 存档 |
| `rewrite-v0.5.0` | 重构尝试（未完成） | 存档 |
| `rewrite-v1.0.0` | 成功完成 v1.0.0 重构 | 已合并到 `master` |
| `master` | **当前主线**，全新 `rootengine` 包，接替 `rootengine-core` | 活跃 |

> `rootengine` 与 `rootengine-core` 是两个独立的 PyPI 包，后者已废弃。

---

### 源码概述

```
rootengine/
├── agent.py          # Agent 配置层，入口
├── engine.py         # Engine 业务层，ReAct 循环
├── conversation.py   # Conversation 消息管理
├── llm/
│   ├── llm.py        # LLM 调用封装
│   ├── base_adapter.py   # BaseAdapter 抽象类
│   └── adapter/
│       └── openai_adapter.py  # OpenAI 适配器
├── tool/
│   ├── base_tool.py  # BaseTool，工具执行单元
│   └── tools.py      # Tool，工具集合管理
├── types/
│   ├── agent.py      # AgentLLM 配置类型
│   ├── llm.py        # LLMRequest / LLMResponse
│   ├── messages.py   # Message 对话消息
│   └── tool.py       # ToolCall / ToolDefinition / ToolResult
└── utils/            # 工具函数
```

---

### 架构特点

- **双层架构**：`Agent`（配置）+ `Engine`（业务）分离
- **适配器模式**：LLM 后端可插拔，实现 `BaseAdapter` 即可扩展
- **ReAct 循环**：`Engine.run()` 自动处理工具调用直到输出
- **装饰器注册**：`@tool` 装饰器一行注册工具

### Added

- 初始架构：Agent + Engine 双层设计
- `AgentLLM`：LLM 配置类，支持自定义 Adapter
- `Agent.react()`：ReAct 循环入口
- `Agent.invoke()`：单次 LLM 调用
- `Engine`：业务层，执行 ReAct loop
- `LLM` + `BaseAdapter` + `OpenAIAdapter`：LLM 调用体系
- `Conversation`：消息管理
- `Tool` + `@tool` 装饰器：工具注册与调用
- `BaseTool.invoke(retry=N)`：工具调用失败重试机制
- 统一数据类型：`Message`、`LLMRequest`、`LLMResponse`、`ToolDefinition` 等
- `pyproject.toml`：单包 PyPI 结构
- 测试用例：25 个测试覆盖 Conversation、BaseTool、Tool

### Changed

- `involve` → `invoke`（LLM 调用方法命名统一）
- 工具模块重构：`Tool`、`ToolCall`、`ToolDefinition` 独立类型

---

## [Old] rootengine-core 历史

| 版本 | 说明 |
|------|------|
| 0.5.12 | 废弃宣告 |
| 0.5.11 | LLM schema 统一为 unified request/response |
| 0.5.1 | base_conversation 替代 no_tool_conversation |
| 0.1.0 | 首个可用版本 |

旧版历史可在 `main` 分支查看。
