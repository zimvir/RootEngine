import json
from sys import exception

from openai import OpenAI
import os
import sys
import time
import ast
import importlib
'''-----------------------------函数--------------------------------'''
def print_system(content):
    print(f"系统：{content}")
ps = print_system

# 返回openai的字典格式
def oa(role, content):
    return {'role': role, 'content': content}
def oat(role, content,tool_calls):
    return {'role': role, 'content': content,'tool_calls': tool_calls}
#询问是否退出程序
def ask_exit():
    while 1:
        a = input("是否退出程序(Y/N）:")
        if a == 'N':
            pass
        elif a == 'Y':
            print(f"[{'-' * 100}AI_assistant v0.1.0: 再见{'-' * 100}]")
            sys.exit()
        else:
            print("请重新输入")
            break
p = print


def get_current_time_main():
    """返回当前时间的字符串（格式：YYYY-MM-DD HH:MM:SS）"""
    return time.strftime("%Y-%m-%d %H:%M:%S")



#快捷操作
def quick(input_data):
    while 1:
        if input_data == 'q':
            ask_exit()
            return "ok"
        elif input_data == 'g':
            intro='''
           p:退出
           g:菜单
           time:现在的时间 
            '''
            ps(intro)
            return "ok"
        elif input_data == time:
            time1 = get_current_time_main()
            ps(f"当前时间{time1}")
            return "ok"

        else:
            return '未知快捷键'


'''---------------------------主程序函数-----------------------------------'''


def universal_params_parser(raw_input):
    """
    通用参数解析函数：自适应处理任意层级转义，最终返回字典
    解决 "argument after ** must be a mapping, not str" 报错
    """
    # 步骤1：统一处理输入（不管输入是字符串/字典，先转成字符串再清理）
    if isinstance(raw_input, dict):
        return raw_input  # 如果已经是字典，直接返回
    input_str = str(raw_input).strip()

    # 步骤2：循环清理转义符，直到没有多余的反斜杠（自适应任意层级转义）
    cleaned_str = input_str
    while '\\' in cleaned_str:
        cleaned_str = cleaned_str.replace('\\', '')  # 删掉所有反斜杠

    # 步骤3：去掉外层的引号（单/双引号都处理）
    cleaned_str = cleaned_str.strip('"').strip("'")

    # 步骤4：智能解析成字典（优先JSON，兜底ast）
    try:
        # 尝试JSON解析（标准格式）
        result = json.loads(cleaned_str)
    except json.JSONDecodeError:
        try:
            # JSON解析失败，用ast解析Python风格字典
            result = ast.literal_eval(cleaned_str)
        except Exception as e:
            raise RuntimeError(
                f"参数解析失败（无法转成字典）：{e}\n原始输入：{raw_input}\n清理后：{cleaned_str}"
            )

    # 步骤5：验证最终类型（必须是字典，否则抛错）
    if not isinstance(result, dict):
        raise TypeError(f"解析结果不是字典（mapping），而是 {type(result)}，无法用**解包")

    return result



'''------------------------------类-----------------------------------'''


class LlmOpenAI:
    '''
    维护一个大模型的连接
    配置步骤
    配置
    初始化
    配置完成
    '''

    def __init__(self, llm_data):
        '''
        初始化openai客户端
        :param llm_data:大模型配置
        llm_data格式
        {
            "api_key":"",
            "base_url":"",
            "model":""
        }
        '''

        self.api_key = llm_data.get('api_key')
        self.base_url = llm_data.get('base_url')
        self.model = llm_data.get('model')

    # openai客户单初始化
    def llm_start(self):
        # API接口
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        return client

    def llm_message_data(self, role, system_prompt, memory, input_data, tool_result_list=None):
        '''
        :param role角色
        :param system_prompt:系统提示词（str）
        :param memory:历史对话记忆（list）
        :param input_data:要说的话（str）
        :param tool_result_list:如果tool要向llm返回数据，填它，列表形式
        tool_result_list格式：
        [
            {
                "tool_call_id":"",
                "result":''
            }
        ]
        如果你的role是user，你会进入跟llm聊天的模式，此时tool_result_list没用
        如果你的role是tool，你将会进入tool向llm返回结果的模式,此时input_data没用:
        :return:message（消息列表list）
        '''
        # 初始化
        # 系统提示词
        system1 = [oa("system", system_prompt)]

        # 用户、工具提示词
        now = []
        # 如果是user的分支
        if role == "user":
            now.append(oa('user', input_data))
        # 如果是 tool返回数据 的分支
        if role == "tool":
            # 解析tool_call_dict：
            for tool_result in tool_result_list:
                now_dict_tool = {"role": "tool",
                                 'content': str(tool_result['result']),
                                 "tool_call_id": tool_result["tool_call_id"]}
                now.append(now_dict_tool)

        # 构建消息列表
        messages = system1 + memory + now
        return messages

    def llm_chat(self, client, messages, tools=None, tool_choice="auto", ):
        '''
        单词对话
        :param client:（初始化）
        :param role:对话角色（str）
        :param 工具列表（list，json反序列化）
        :param tool_choice:见openai文档

        :return：对象response
        '''

        # 与llm交互
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            stream=False,
            extra_body = {"enable_search": True}
        )
        return response

    def llm_prsm_data(self, response):
        '''

        :param response: llm返回的对象
        :return: reasoning_content:推理过程
                "content":直接回答
                "tool_calls"：tool列表
        '''
        # 解析
        reasoning_content = getattr(response.choices[0].message, "reasoning_content", None)  # 思考过程
        content = response.choices[0].message.content  # 正式回答
        tool_calls = response.choices[0].message.tool_calls

        reply_data = {
            "reasoning_content": reasoning_content,
            "content": content,
            "tool_calls": tool_calls,
            "all":response
        }
        return reply_data

    def llm_tool_register(self, tool_register):
        '''
        把工具注册表转换成openai的格式
        :param tool_register:

        :return:转换好的格式,若没有可用工具（tool是空列表），会返回None
        '''
        tools = []
        for id in tool_register:  #这里id就是name。  type(id) = str
            tool = {
                "type": "function",
                "function": {
                    "name": id,
                    "description": tool_register[id]["data"]["description"],
                    "parameters": tool_register[id]["data"]["parameters"]
                }
            }
            tools.append(tool)
        if tools == []:
            return None
        else:
            return tools


class Memory:
    '''
    维护一个以文档为单位的记忆库
    '''

    def __init__(self, path):
        '''
        创建一个记忆库
        :param path: 文件路径
        '''
        self.id = id
        self.path = path

    def memory_creat(self):
        # 确保文件存在
        open(self.path, mode='a', encoding='utf-8').close()

        # 确保文件是json格式
        with open(self.path, mode='r', encoding='utf-8') as f:

            con = f.read()
            # 防止新建文件为空
            if not con:
                f1 = open(self.path, mode='w', encoding='utf-8')
                json.dump([], f1, ensure_ascii=False, indent=4)
                f1.close()
                ps("已新建记忆文件")
            else:
                # 防止文件格式错误

                try:
                    json.loads(con)
                except json.JSONDecodeError:
                    ps("记忆文件不符合json格式")

    def memory_save(self, role,content,other=None):
        '''
        将一条角色和文本对应的记忆保存起来
        :param:role:此文本的角色user/tool/assistant
        :param content:user:用户说的话，tool:tool_result_list,assistant:llm返回时的content文本
        :param other role=user不用填，
                role=tool填tool_result_list,是列表
                role=assistant填tool_calls,是一个列表，
        :return:ok
        '''
        # 读取记忆文件

        with open(self.path, mode='r', encoding='utf-8') as f:
            content_list = json.load(f)
        #更新
            #user
            if role == "user":
                content_list.append(oa('user', content))
            #tool
            elif role == "tool":
                tool_result_list = other
                #遍历tool_result_list得到每个tool的id和result
                for tool_result in tool_result_list:
                    a3 = {'role': 'tool',
                          'content':str(tool_result['result']),
                          "tool_call_id":tool_result['tool_call_id']
                          }
                    content_list.append(a3)
            #assistant
            elif role == "assistant":
                tool_calls = other
                #不调用工具
                if tool_calls is None:
                    content_list.append({'role': 'assistant', "content": content})
                else :
                    # 将 tool_calls 对象转换为可 JSON 序列化的字典列表
                    tool_calls_dicts = []
                    for tc in tool_calls:
                        tool_calls_dicts.append({
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        })
                    content_list.append({
                        'role': 'assistant',
                        "content": None,
                        'tool_calls': tool_calls_dicts
                    })




        #重新写入
        with open(self.path, mode='w', encoding='utf-8') as f:
            json.dump(content_list, f, ensure_ascii=False, indent=4)
        return 'ok'

    def memory_read(self):
        '''
        读取记忆文件
        :return:对应文件的list格式
        '''
        # 防止记忆文件不存在
        open(self.path, mode='a', encoding='utf-8').close()
        # 防止记忆文件格式错误
        with open(self.path, mode='r', encoding='utf-8') as f:
            try:
                content_list = json.load(f)
                return content_list
            except json.JSONDecodeError:
                ps('记忆文件不符合json格式')
                sys.exit()


class Tool:
    '''
    据一个工具注册表操作
    注册表格式：

[{

    "name" : "工具函数实际名",
    "func_name":适配器函数名（实际函数映射）,
    "description":"描述",
    "parameters":{
        "type":"数据类型(填str/list...)",
        properties:{
                "参数名": {"type":"数据类型（str/list...)"}
                    }
    },

}]

    '''

    def __init__(self, tools_register,agent):
        '''

        :param tools_register:工具注册表(list)
        :param agent 传agent实例
        工具接口：
        尽量返回str
        '''
        self.tools_register = tools_register
        self.agent = agent

    def tool_call_deal(self, tool_calls):
        '''
        搜索并执行工具
        :param tool_calls:
        :return:
        '''
        # 判断是否调用工具
        if tool_calls:

            tool_result_list = []
            ps('调用工具中')
            #遍历tool_calls
            for ii in tool_calls:
                abc = 0
                tool_name = ii.function.name


                try:
                    #解析arguments
                    arg = ii.function.arguments
                    #arguments = universal_params_parser(ii.function.arguments)  #用自己的解析函数
                    arguments = json.loads(arg)
                    print(f"参数：{arguments}")

                    # 调用工具
                    try:
                        result = self.tools_register[tool_name]["function"](agent=self.agent, **arguments)
                    except Exception as e:
                        ps(f'工具{tool_name}执行出错: {e}')
                        result = f'工具{tool_name}执行出错: {str(e)}'

                except Exception as e:
                    #参数解码问题
                    result = f"工具参数解码错误：{e}"
                    ps(e)
                tool_call_id = ii.id


                #生成工具调用结果
                tool_result_list.append({"tool_call_id": tool_call_id, "result": result})

            return tool_result_list
        else:
            #无工具调用终止工具调用进程
            return []




class Agent:
    '''
    维护一个智能体
    '''
    '''llm'''


    def __init__(self,
                 agent_name,
                 agent_id,
                 llm_data,
                 system_prompt,
                 memory_path,
                 tool_register,
                 ):
        '''

        :param agent_name: 智能体名称（str）
        :param agent_id: 智能体id，id不可以重复，凭id找智能体(str)
        :param llm_data: 大模型的数据（dict）
        :param system_prompt: 系统提示词（str）
        :param memory_path:记忆文件的路径(str)
        :param: tool_register:工具注册表（list）
        agent_llm格式：
        {
            "api_key":"",
            "base_url":"",
            "model":""
        }

        '''
        self.agent_name = agent_name
        self.agent_id = agent_id
        self.memory_path = memory_path
        self.llm_data = llm_data
        self.system_prompt = system_prompt
        self.tool_register = tool_register
        #创建实例
        self.llm = LlmOpenAI(self.llm_data)
        self.client = self.llm.llm_start()
        ps("chat completion API初始化")

        self.memory_obj = Memory(memory_path)
        self.memory_obj.memory_creat()
        ps("memory文件初始化")

        self.tool = Tool(self.tool_register,agent = self)
        ps('tool初始化')
    def agent_base_chat(self,role,input_data,tool_result_list=None,tool_choice = 'auto'):
        '''
        与大模型基本的输入，输出
        :param role:
        :param input_data:user输入的东西，role=tool时无效（str）
        :param tool_result_list:工具返回结果role = user时无效（str）
        :param tool_choice:见openai官方文档
        :return: reply_data重要数据

        '''
        # 读取记忆
        memory = self.memory_obj.memory_read()

        #与llm交互
        #构建message
        messages = self.llm.llm_message_data(
            role = role,
            system_prompt = self.system_prompt,
            memory = memory,
            input_data = input_data,
            tool_result_list=tool_result_list
        )

        #开始交互
        response =  self.llm.llm_chat(client = self.client,
                                      messages = messages,
                                      tools = self.llm.llm_tool_register(self.tool_register),
                                      tool_choice=tool_choice
                                      )

        #解析数据
        reply_data = self.llm.llm_prsm_data(response)

        #保存记忆

        self.memory_obj.memory_save(role, input_data,tool_result_list)
        self.memory_obj.memory_save("assistant",reply_data["content"],reply_data["tool_calls"])

        return reply_data

    def agent_deal(self,reply_data):
        '''
        处理主循环除了网络反面的部分
        :param reply_data: 重要数据的字典，也是上面那个函数的返回值
        :return: 若llm直接跟user说话（没有tool要返回结果），没有返回ok，若tool要返回result，返回tool_result_list
        '''
        reasoning_content = reply_data.get("reasoning_content",'')
        content = reply_data["content"]
        tool_calls = reply_data["tool_calls"]
        #user分支
        if tool_calls is None:
            #直接打印给user面板,无工具调用
            return None
        #走tool分支
        else:

            tool_result_list = self.tool.tool_call_deal(tool_calls)

            return tool_result_list

    def agent_llm_with_tool_chat(self,user_input):
        '''
        组合了llm和tool调用，实现了user给llm发出指令，llm与tool交互完成后由llm将结果返回给user
        :param user_input:用户输入
        :return:llm与tool交互完，llm给用户返回的结果
        '''
        input_data = user_input
        tool_result_list = None
        role = 'user'
        while 1:
            # tool的result给返回llm
            # 交互
            reply_data = self.agent_base_chat(
                role=role,
                input_data=input_data,
                tool_result_list=tool_result_list,
                tool_choice='auto',

            )

            # 工具调用
            tool_result_list = self.agent_deal(reply_data)
            # 处理分支（返回user/llm给tool参数，tool结果返回llm）
            if tool_result_list is not None:
                #将若有工具调用，则将调用结果作为输入返回给llm
                role = "tool"
            else:
                #返回user
                return reply_data["content"]



    def agent_get_memory_path(self,):
        '''衔接memorize工具函数'''
        return self.memory_path


class Start:
    def __init__(self,config_file_name,tools_file_name):
        self.config_file = importlib.import_module(config_file_name)
        self.tools_file = importlib.import_module(tools_file_name)


    def start_tool_register(self):
        '''
        通过对工具文件、配置文件的解析，合成带函数映射的tool注册表
        :param tools_file: 工具文件
        :param config_file: 配置文件
        :return: 完好的工具注册表（带函数映射）
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

        # 拿到映射表
        tools_meta = self.tools_file.get_tools_meta()  #
        # 获取原注册表
        tools_usable_list = self.config_file.tools_usable_list
        tool_register = {}
        for usable in tools_usable_list:
            try:
                #将tool_usable_list中可用的工具名，
                tool_register[usable] = tools_meta[usable]
            except Exception as e:
                raise e
        return tool_register

    def start_all(self):
        start_dict = {}
        start_dict["llm_data"] = self.config_file.llm_data
        start_dict["memory_path"] = self.config_file.memory_path
        start_dict["system_prompt"] = self.config_file.system_prompt
        start_dict["tool_register"] = self.start_tool_register()
        return start_dict





'''示例，对话Agent'''


#初始化
start = Start("config","tools")
start_dict = start.start_all()

#创建Agent实例

ass2 = Agent(
    llm_data = start_dict["llm_data"],
    agent_name= "check",
    agent_id= 1,
    memory_path= start_dict["memory_path"],
    system_prompt = start_dict["system_prompt"],
    tool_register = start_dict["tool_register"]
)

#主循环
while 1:
    user_input = input("你：")
    while 1:
        reply_content = ass2.agent_llm_with_tool_chat(user_input)
        print(f"助手：{reply_content}")
        break














