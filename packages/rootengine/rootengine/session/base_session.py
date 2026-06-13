from abc import ABC, abstractmethod
class BaseSession(ABC):
    @abstractmethod
    def call(self, client):
        """发送请求到 LLM，返回原始响应"""
        pass

    @abstractmethod
    def append(self, response):
        """将 LLM 响应写入 conversation"""
        pass

    # @abstractmethod
    # def to_dict(self) -> dict:
    #     """序列化 session 状态（用于持久化）"""
    #     pass

    @abstractmethod
    def reset(self):
        """重置 session（清空 messages、tool_calls 等）"""
        pass
