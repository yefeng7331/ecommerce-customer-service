"""
@Author:叶枫
@Time:2026/9/12
@Desc: 这个模块是TaskHandler的一个组件
作用：根据返回的TaskEvent对象，返回不同的中文提示


"""
from domain.message import BotMessage
from task.flow.models import FlowCatalog
from task.lifecycle.models import TaskEvent, TaskStarted, TaskSwitched, TaskCanceled, TaskResumed


class TaskLifecycleResponder:
    async def responder(self,events:list[TaskEvent],flow_catalog:FlowCatalog)->list[BotMessage]:
        messages:list[BotMessage]=[]
        for event in events:
            bot_message:BotMessage = self.execute_task_event(event,flow_catalog)
            messages.append(bot_message)
        return messages

    def execute_task_event(self, event:TaskEvent,flow_catalog:FlowCatalog)->BotMessage:
        if isinstance(event,TaskStarted):
            # 获取event里面flow_id 根据flow_id 获取流程名称
            flow = flow_catalog.get_flow_by_id(event.task.flow_id)
            return BotMessage(text=f'好的，现在开始处理{flow.name}')
        if isinstance(event,TaskSwitched):
            previous_flow = flow_catalog.get_flow_by_id(event.previous.flow_id)
            current_flow = flow_catalog.get_flow_by_id(event.current.flow_id)
            return BotMessage(text=f'好的，先把{previous_flow}暂停,'f'现在要开始{current_flow}')

        if isinstance(event,TaskResumed):
            flow = flow_catalog.get_flow_by_id(event.task.flow_id)
            return BotMessage(text=f'好的，继续刚才{flow.name}')
        if isinstance(event,TaskCanceled):
            flow = flow_catalog.get_flow_by_id(event.task.flow_id)
            return BotMessage(text=f'好的，取消{flow.name}')

