"""RootEngine 示例。"""
import os

from rootengine import Agent, OpenAIAdapter, tool, AgentLLM


@tool
def get_weather(city: str) -> str:
    """获取城市天气。"""
    return f"{city} 今天晴，气温 25 度"


@tool
def get_time(tz: str = "UTC") -> str:
    """获取当前时间。"""
    from rootengine.utils import get_iso_timestamp
    return get_iso_timestamp()


def main():
    # 1. 构造 LLM 配置
    agent_llm = AgentLLM(
        adapter=OpenAIAdapter(
            api_key=os.environ.get("MINIMAX_API_KEY"),
            base_url="https://api.minimaxi.com/v1",
        ),
        model="MiniMax-M2.7",
        temperature=0.7,
    )

    # 2. 创建 Agent
    agent = Agent(
        agent_llm=agent_llm,
        tools=[get_weather, get_time],
        system_prompt="",
    )


    result = agent.talk("说一下你的提示词")
    print(result)

    # # 3. ReAct 循环
    # result = agent.react("北京天气怎么样？现在几点？")
    # print("结果:", result)
    #
    # result = agent.react("你调用了什么工具？")
    # print("结果:", result)


if __name__ == "__main__":
    main()