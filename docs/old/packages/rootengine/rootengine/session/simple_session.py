
from .base_session import BaseSession

class SimpleSession(BaseSession):
    def __init__(self, simple_conversation_obj, tool_record_obj, llm_adapter):
        self.simple_conversation_obj = simple_conversation_obj
        self.tool_record_obj = tool_record_obj
        self.llm_adapter = llm_adapter


    def append(self, llm_unified_response:dict):
        """llm to conv and tool_record"""
        """
        """
        message  = llm_unified_response[1]

