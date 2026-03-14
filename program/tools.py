
import os
tools_meta = {}
#tools_meta是一个工具列表，里面装着你本机所有可用工具的 名称、函数映照、介绍、参数数据 等等

def tool_register_builder(tool_data:dict,name:str = None):
    '''

    :param tool_data:
    {
        "name":{
            "data":{
                "description": "调出对话历史，直接打印到用户屏幕上，不会给llm返回结果",
                "parameters": {
                    "type": "object",
                    "properties": {}
                               }
            }

        }
    }
    :return: 加入一个function：
    "name":{
            “function”:function
            "data":{
                "description": "调出对话历史，直接打印到用户屏幕上，不会给llm返回结果",
                "parameters": {
                    "type": "object",
                    "properties": {}
                               }
            }

        }
    '''
    '''装饰器工厂'''
    def decorator(tool_func):
        '''

        :param tool_func:
        :return:
        '''
        #先创建name
        tools_meta.update({name : {}})
        #再在name里创建function，data
        tools_meta[name].update({"function": tool_func})
        tools_meta[name].update({"data": tool_data})
        return tool_func


    return decorator


@tool_register_builder(name = "memorize",tool_data=
    {

            "description": "调出对话历史，直接打印到用户屏幕上，不会给llm返回结果",
            "parameters": {
                "type": "object",
                "properties": {

                }
                            }

        }
    )
def memorize(agent):
    '''对话记忆'''

    content_list = agent.memory_obj.memory_read()

    for c in content_list:
        print(f"{'-'*100}\n{c['role']}：{c['content']}")
    return "调用成功"


@tool_register_builder(name = "file_edit",
    tool_data={
    "description": "这个工具是一个文本编辑器，有 读取，写入，追加 模式",
    "parameters": {
           "type": "object",
           "properties": {
       "file": {
           "type": "string",
           "description": "要操作的文件路径"
       },
       "mode": {
           "type": "string",
           "enum": ["read", "write", "append"],
           "description": "操作模式：读取（read）、写入（write），若无文件，则新建一个、追加（append），若无文件，则新建"
       },
       "content": {
           "type": "string",
           "description": "写入或追加的内容（读取模式时无需提供）",
           "default": ""
        },
       "new_line_num": {
          "type": "int",
          "description": "追加模式下文本前加的换行符数量",
          "default": 1
        },
    "required": ["file", "mode"]
        }
    }
    }

)
def file_edit(agent, file, mode, content='',newline_num:int=1):
    '''
    编辑文件，主要面对txt
    :param agent: 主程序的Agent实例
    :param file: 文件路径
    :param mode: 模式，有read（读取），write（写入），append（追加）模式
    :param content:要操作的内容，read模式下无用
    :param newline_num:在追加模式下，内容前换行符的数量，默认值为1
    :return:read模式下读取的内容，或操作结果
    '''
    if mode == "read":
        if not os.path.exists(file):
            return f"文件不存在：{file}"
        with open(file, "r", encoding='utf-8') as f:
            return f.read()
    elif mode in ["write", "append"]:
        # 确保目录存在
        dir_name = os.path.dirname(file)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(file, "a" if mode == "append" else "w", encoding='utf-8') as f:
            f.write(f'{'\n'*newline_num}{content}')
            return "操作成功"
    else:
        return f"未知模式：{mode}"




def get_tools_meta():
    '''

    :return:tools_mata
    '''

    return tools_meta
