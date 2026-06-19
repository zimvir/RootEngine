from .types import Message
from .utils import get_iso_timestamp, build_system_message


class Conversation:
    def __init__(self, system_prompt: str = None):
        self.messages: list[Message] = []
        self.system_prompt = system_prompt
        if self.system_prompt:
            self.append(build_system_message(system_prompt))

    def append(self, message: Message) -> "Conversation":
        self.messages.append(message)
        return self

    def append_many(self, messages: list[Message]) -> "Conversation":
        self.messages.extend(messages)
        return self

    # def append_user(self, content: str) -> "Conversation":
    #     self.messages.append(Message(role="user", content=content, created_at=get_iso_timestamp()))
    #     return self
    #
    # def append_assistant(self, content: str | None = None, tool_calls: list | None = None) -> "Conversation":
    #     msg = Message(role="assistant", content=content, created_at=get_iso_timestamp())
    #     if tool_calls:
    #         msg.tool_calls = tool_calls
    #     self.messages.append(msg)
    #     return self
    #
    # def append_tool(self, tool_call_id: str, content: str) -> "Conversation":
    #     self.messages.append(Message(
    #         role="tool",
    #         tool_call_id=tool_call_id,
    #         content=content,
    #         created_at=get_iso_timestamp()
    #     ))
    #     return self

    def append_system(self, content: str) -> "Conversation":
        self.messages.append(Message(role="system", content=content, created_at=get_iso_timestamp()))
        return self

    def delete(self, index: int=-1) -> "Conversation":
        self.messages.pop(index)
        return self

    def get_messages(self) -> list[Message]:
        return self.messages

    def get_messages_in_list(self) -> list[dict]:
        return [m.model_dump(exclude_none=True) for m in self.messages]

    @classmethod
    def from_dict_list(cls, messages: list[dict]) -> "Conversation":
        conv = cls()
        conv.messages = [Message.model_validate(m) for m in messages]
        return conv

    @classmethod
    def from_list(cls, messages: list[Message]) -> "Conversation":
        conv = cls()
        conv.messages = list(messages)
        return conv

    def clear(self) -> "Conversation":
        self.messages = []
        return self

