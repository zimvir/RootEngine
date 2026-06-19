# RootEngine

轻量级 Python AI Agent 框架，基于简洁的 ReAct 循环（Reasoning + Action）。


## 特点

- **轻量** — 核心代码量少，无过多抽象层，快速上手
- **双层架构** — `Agent` 负责配置，`Engine` 执行业务逻辑，职责分离
- **适配器模式** — LLM 后端可替换，默认支持 OpenAI，实现 `BaseAdapter` 即可扩展
- **ReAct 循环** — 调用 `Agent.react()` 即可启动，自动处理工具调用
- **装饰器注册工具** — `@tool` 装饰器即可注册，无需手动定义 Schema
- **基于 Pydantic** — 所有数据模型类型安全、验证严格
- **会话管理** — `Conversation` 自动维护对话历史，支持 system prompt

## 快速开始

## 安装

```bash
pip install rootengine
```

```python
from rootengine import Agent, OpenAIAdapter, tool, AgentLLM

@tool
def get_weather(city: str) -> str:
    """获取城市天气。"""
    return f"{city} 今天晴，气温 25 度"

# 1. 构造 LLM 配置
agent_llm = AgentLLM(
    adapter=OpenAIAdapter(api_key="your-api-key"),
    model="gpt-4o",
    temperature=0.7,
)

# 2. 创建 Agent
agent = Agent(
    agent_llm=agent_llm,
    tools=[get_weather],
    system_prompt="你是一个有用的助手。",
)

# 3. ReAct 循环
result = agent.react("北京天气怎么样？")
print("结果:", result)
```

## 架构

```
Agent          ← 用户入口，配置层
  └── Engine   ← 业务层，ReAct loop
        ├── LLM(Adapter)   ← LLM 调用
        ├── Conversation   ← 消息管理
        └── Tool          ← 工具注册 + 调用
```

### 核心模块

| 模块 | 说明 |
|------|------|
| `Agent` | 配置层，创建 Engine，管理会话 |
| `Engine` | 业务层，执行 ReAct 循环 |
| `Conversation` | 消息管理，维护对话历史 |
| `LLM` / `BaseAdapter` | LLM 调用抽象，支持自定义适配器 |
| `Tool` / `BaseTool` | 工具注册与调用 |
| `types` | 数据类型定义（Message, ToolCall, ToolDefinition 等） |

### 核心概念

- **Agent**：配置层，负责创建 Engine、管理会话持久化
- **Engine**：业务层，持有 LLM + Conversation + Tool，执行 ReAct 循环
- **Adapter**：LLM 后端适配器，目前支持 OpenAI，可自行扩展

## 依赖

- Python >= 3.10
- pydantic >= 2.0
- openai >= 1.0

## License

MIT
