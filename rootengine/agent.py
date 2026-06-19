from pathlib import Path

from .engine import Engine
from .llm import LLM
from .conversation import Conversation
from .tool import Tool, BaseTool
from .types.agent import AgentLLM
from .types import ToolDefinition
from .utils import build_system_message, build_message, build_tool_message, build_user_message, build_assistant_message

class Agent:

    def __init__(
        self,
        agent_llm: AgentLLM,
        *,
        tools: list[BaseTool] | None = None,
        system_prompt: str | None = None,
        # session_id: str | None = None,
        # db_path: str | Path | None = None,
        # max_retries: int = 3,
        timeout: float | None = None,
    ):
        self.conversation = Conversation(system_prompt)
        self.tool = Tool(tools or [])
        # self.session_id = session_id
        # self.db_path = db_path

        self.engine = Engine(
            model=agent_llm.model,
            llm=LLM(agent_llm.adapter),
            conversation=self.conversation,
            tool=self.tool,
        )


    def react(self, input_prompt:str) -> "str":
        """一次 react 循环"""
        response = self.engine.run(build_user_message(input_prompt))
        return response.content

    def talk(self, input_prompt:str) -> "str":
        """一次 agent 调用"""
        return self.engine.invoke(build_user_message(input_prompt)).content



