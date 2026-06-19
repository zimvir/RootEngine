"""Message: 对话原子单元（pydantic）

rootengine 中所有对话、LLM 请求、工具调用的基本数据单元。
"""

from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """assistant 发起的工具调用"""

    id: str
    registry_id: str
    arguments: dict = Field(default_factory=dict)


class ToolResult(BaseModel):
    """tool 角色的 content：工具执行结果"""

    registry_id: str
    result: Any
    status: Literal["success", "error", "timeout", "cancelled"] = "success"
    error: str | None = None


class Message(BaseModel):
    """一条对话消息。

    同一份 Message 在内部存储、LLM 请求、LLM 响应里都通用。
    """

    # === 必填 ===
    role: Literal["system", "user", "assistant", "tool"]
    content: str | None | ToolResult = None
    created_at: str

    # === 可选（按 role 选择性使用）===
    tool_calls: list[ToolCall] = Field(default_factory=list)
    """assistant 时：LLM 决定要调用的工具列表。"""

    tool_call_id: str | None = None
    """tool 时：关联到 assistant 消息里对应 tool_call 的 id。"""

    reasoning: str | None = None
    """assistant 时：思维链 / 推理内容（可选）。"""

    extra: dict = Field(default_factory=dict)
    """扩展点，放任意额外数据。"""