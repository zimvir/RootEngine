"""工具集合。"""

from typing import Callable

from rootengine.types.tool import ToolCall, ToolDefinition, ToolResult

from .base_tool import BaseTool

def tool(func: Callable) -> BaseTool:
    """@tool 装饰器：返回 BaseTool 对象。"""
    return BaseTool(func)


class Tool:
    """工具集合，维护 name -> BaseTool 的映射。"""

    def __init__(self, tools: list[BaseTool] = None):
        self._map: dict[str, BaseTool] = {}
        if tools:
            for t in tools:
                self._map[t.name] = t

    def add(self, base_tool: BaseTool) -> "Tool":
        """添加一个工具。"""
        self._map[base_tool.name] = base_tool
        return self

    def get(self, name: str) -> BaseTool | None:
        """根据 name 获取工具。"""
        return self._map.get(name)

    def invoke(self, tool_call: ToolCall) -> ToolResult:
        """执行单个工具调用。"""
        t = self.get(tool_call.name)
        if t is None:
            return ToolResult(tool_call_id=tool_call.id, content=f"Tool '{tool_call.name}' not found")
        content = t.invoke(tool_call.arguments)
        return ToolResult(tool_call_id=tool_call.id, content=content)

    def invoke_many(self, tool_calls: list[ToolCall]) -> list[ToolResult]:
        """批量执行工具调用。"""
        return [self.invoke(tc) for tc in tool_calls]

    def to_definitions(self) -> list[ToolDefinition]:
        """生成所有工具的 ToolDefinition 列表（发给 LLM）。"""
        return [t.to_definition() for t in self._map.values()]