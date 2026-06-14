# Changelog

所有重要版本变更记录。

格式基于 [Keep a Changelog](https://keepachangelog.com/)。

## [1.0.0] - unreleased

### Added
- 初始架构：Agent + Engine 双层设计
- `AgentLLM`：LLM 配置类，支持自定义 Adapter
- `Agent.react()`：ReAct 循环入口
- `Agent.invoke()`：单次 LLM 调用
- `Engine`：业务层，执行 ReAct loop
- `LLM` + `BaseAdapter` + `OpenAIAdapter`：LLM 调用体系
- `Conversation`：消息管理
- `Tool` + `@tool` 装饰器：工具注册与调用
- 统一数据类型：`Message`、`LLMRequest`、`LLMResponse`、`ToolDefinition` 等

### Changed
- `involve` → `invoke`（LLM 调用方法命名统一）

### Deprecated
- `rootengine-core` 包已废弃，合并到 `rootengine`

---

## [0.5.12] - 2026-06-13

### Deprecated
- `rootengine-core` 不再维护，请迁移到 `rootengine`

---

## [0.5.11] - 2026-06-13

### Changed
- LLM schema 统一为 unified request/response 格式