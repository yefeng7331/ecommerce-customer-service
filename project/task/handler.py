"""
@Author:叶枫
@Time:2026/9/14
@Desc:任务处理模块
"""
from project.domain.message import UserMessage, BotMessage
from project.domain.state import DialogueState
from project.task.command.models import Command
from project.task.command.processor import CommandProcessor
from project.task.flow.executor import FlowExecutor
from project.task.flow.models import FlowCatalog
from project.task.lifecycle.models import TaskEvent
from project.task.lifecycle.responder import TaskLifecycleResponder


class TaskHandler:
    # 注入
    # 处理任务命令，根据任务生命周期，执行任务
    def __init__(self,command_processor:CommandProcessor
                 ,task_lifecycle:TaskLifecycleResponder,
                 flow_executor:FlowExecutor,
                 ):
        self.flow_executor = flow_executor
        self.command_processor = command_processor
        self.task_lifecycle = task_lifecycle

    async def handle(self,commands:list[Command],
                     state:DialogueState,
                     flows:FlowCatalog,
                     user_message:UserMessage)->list[BotMessage]:
        """
        处理任务命令，根据任务生命周期，执行任务
        :param user_message: 用户消息
        :param commands: 意图识别结果列表
        :param state: 当前用户会话状态
        :param flows: 流程目录
        :return: 机器人回复列表
        """
        # 1根据意图识别结果，调用CommandProcessor更新state状态
        events:list[TaskEvent] = await self.command_processor.run(
            commands=commands,
            state=state,
            flows=flows,
        )
        # 2根据CommandProcessor返回结果,调用TaskLifecycleResponder生成不同的中文提示
        messages:list[BotMessage] = await self.task_lifecycle.responder(
            events=events,
            flow_catalog=flows,
        )

        # todo 3 调用FlowExecutor执行流程
        bot_messages:list[BotMessage] = await self.flow_executor.run_step(
            state=state,
            flows=flows,
        )
        messages.extend(bot_messages)
        return messages
