# RootEngine

轻量级 AI Agent 框架，核心是 ReAct 循环（Reasoning + Action）。

## 安装

```bash
pip install rootengine
```

## 快速开始

```python
from rootengine.agent import Agent
from rootengine.llm.adapter import OpenAIAdapter
from rootengine.tool import tool
from rootengine.types.agent import AgentLLM


@tool
def get_weather(city: str) -> str:
    """获取城市天气。"""
    return f"{city} 今天晴，气温 25 度"


# 1. 构造 LLM 配置
llm = AgentLLM(
    adapter=OpenAIAdapter(api_key="your-api-key"),
    model="gpt-4o",
    temperature=0.7,
)

# 2. 创建 Agent
agent = Agent(
    llm=llm,
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

## 核心概念

- **Agent**：配置层，负责创建 Engine、管理会话持久化
- **Engine**：业务层，持有 LLM + Conversation + Tool，执行 ReAct 循环
- **Adapter**：LLM 后端适配器，支持 OpenAI 等，可自定义

## License

MIT