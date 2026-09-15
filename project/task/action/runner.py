"""
@Author:叶枫
@Time:2026/9/15
@Desc:action运行器
这个模块对外调用
再FlowExecutor的action类型步骤调用这个模块方法实现
"""
from domain.state import DialogueState
from task.action.base import ActionCall, Action, ActionResult
from task.action.register import ActionRegister



class ActionRunner:
    def __init__(self,register:ActionRegister):
        self.register = register


    # 对外提供的方法
    # 参数 action_call:action步骤里面的action属性值
    async def run(self,action_call:ActionCall,state:DialogueState)->ActionResult:
        # 1 根据yaml文件中action步骤里面的action属性值找到对应action对象
        action_name = action_call.action_name
        action:Action = self.register.get_action(action_name)

        # 2 找到action对象之后，执行方法远程调用
        result = await action.run(state)

        # 3 远程调用之后，返回结果
        return result
