
from .types.tool import ToolRegistry, ToolCall, ToolMap, ToolResult

class Tool:
    def __init__(self, tool_registry: ToolRegistry, tool_map: ToolMap):
        self.tool_registry = tool_registry
        self.tool_map = tool_map

    def call(self, tool_call: ToolCall):

        function = self.tool_map.get_func(tool_call.name)

        try:
            content =  str(function(**tool_call.arguments))
        except Exception as e:
            content = str(e)
        result = ToolResult(tool_call_id=tool_call.id, content=content)
        return result



