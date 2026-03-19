    

def print_system(content):
    print(f"系统：{content}")
ps = print_system

# 返回openai的字典格式
def oa(role, content):
    return {'role': role, 'content': content}
def oat(role, content,tool_calls):
    return {'role': role, 'content': content,'tool_calls': tool_calls}




#返回 UTC 的 ISO 格式的时间
from datetime import datetime, timezone
def get_iso_timestamp(microseconds=True):
    """自定义是否包含微秒"""
    if microseconds:
        return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')
    else:
        return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

