"""
@Author:叶枫
@Time:2026/9/12
@Desc: 这个模块是TaskHandler组件
    作用：根据意图识别结果，更新对应State里面数据
    返回任务状态变化对象TaskEvent,为了后面组件生成中文提示


"""
from domain.state import DialogueState, TaskInstance
from task.command.models import Command, StartFlowCommand, ResumeTaskCommand, SetSlotsCommand, CancelTaskCommand
from task.flow.models import FlowCatalog, Flow
from task.lifecycle.models import TaskEvent


class CommandProcessor:
    async def run(self,
                  commands:list[Command],
                  state:DialogueState,
                  flows:FlowCatalog
                  )->list[TaskEvent]:
        events: list[TaskEvent] = []
        # 遍历意图识别结果列表，得到每个command，根据不同类型command不同处理
        for command in commands:
            event:TaskEvent = self._execute_command(command,state,flows)
            if event:
                events.append(event)
        return events

    # 处理每个command
    def _execute_command(self, command:Command, state:DialogueState, flows:FlowCatalog)->TaskEvent:
        # 判断Command类型
        if isinstance(command,StartFlowCommand):
            flow_id = command.flow
            # 根据流程id，获取流程对象
            flow:Flow = flows.get_flow_by_id(flow_id)
            # 获取开始类型步骤
            start_step = flow.get_start_step()
            # 创建当前任务对象
            task = TaskInstance(
                flow_id=flow_id,
                step_id=start_step.id,
            )

            # 更新state对象里面TaskStatus属性值active和paused
            event:TaskEvent = state.tasks.start(task)
            return event

        # 设置槽位数据前提条件：当前任务存在
        if isinstance(command,SetSlotsCommand):
            if state.tasks.active:
                state.tasks.active.slots.update(command.slots)
                return None
        if isinstance(command,ResumeTaskCommand):
            event:TaskEvent = state.tasks.resume(command.task_id)
            return event
        if isinstance(command,CancelTaskCommand):
            event:TaskEvent = state.tasks.cancel(command.task_id)
            return event

