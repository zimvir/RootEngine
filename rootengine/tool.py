"""工具注册与调用。"""

import inspect
from typing import Callable

from .types.tool import (
    ToolCall,
    ToolDefinition,
    ToolMap,
    ToolRegistry,
    ToolResult,
)


# 全局注册表
_registry = ToolRegistry(name="default")
_toolmap = ToolMap()


def _generate_tool_definition(func: Callable) -> ToolDefinition:
    """从函数签名生成 ToolDefinition。"""
    name = func.__name__
    description = (func.__doc__ or "").strip()
    sig = inspect.signature(func)

    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
    }

    for param_name, param in sig.parameters.items():
        # 跳过 self / cls 参数
        if param_name in ("self", "cls"):
            continue

        # 类型注解转字符串
        if param.annotation is not inspect.Parameter.empty:
            param_type = param.annotation.__name__
        else:
            param_type = "string"

        prop = {"type": param_type}

        # 有默认值
        if param.default is not inspect.Parameter.empty:
            prop["default"] = param.default
        else:
            parameters["required"].append(param_name)

        parameters["properties"][param_name] = prop

    return ToolDefinition(name=name, description=description, parameters=parameters)


def tool(func: Callable) -> Callable:
    """@tool 装饰器：自动注册函数到全局 registry。

    用法：
        @tool
        def get_weather(city: str) -> str:
            \"\"\"获取天气\"\"\"
            return f"{city} is sunny"
    """
    definition = _generate_tool_definition(func)
    _registry.tools.append(definition)
    _toolmap.register(definition.name, func)
    return func


def get_tools() -> list[ToolDefinition]:
    """获取所有已注册的工具定义。"""
    return list(_registry.tools)


def get_tool_map() -> ToolMap:
    """获取 name -> 函数 的映射。"""
    return _toolmap


class Tool:
    """工具调用器。"""

    def __init__(self, registry: ToolRegistry | None = None, tool_map: ToolMap | None = None):
        self.registry = registry or _registry
        self.tool_map = tool_map or _toolmap

    def call(self, tool_call: ToolCall) -> ToolResult:
        """执行单个工具调用。"""
        function = self.tool_map.get_func(tool_call.name)
        if function is None:
            return ToolResult(
                tool_call_id=tool_call.id,
                content=f"Tool '{tool_call.name}' not found",
            )

        try:
            content = str(function(**tool_call.arguments))
        except Exception as e:
            content = str(e)

        return ToolResult(tool_call_id=tool_call.id, content=content)

    def call_all(self, tool_calls: list[ToolCall]) -> list[ToolResult]:
        """批量执行工具调用。"""
        return [self.call(tc) for tc in tool_calls]