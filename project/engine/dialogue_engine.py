"""
@Author:叶枫
@Time:2026/9/9
@Desc: 聊天引擎层
        处理用户消息，根据历史记录和用户问题，返回机器人回复
"""
import time
import uuid
from pathlib import Path

from project.domain.message import UserMessage, ProcessResult, MessageType, BotMessage
from project.domain.state import DialogueState, Turn
from project.plan.models import TurnPlan, TurnPlanValidationResult
from project.plan.turn_plan import TurnPlanner
from project.plan.turn_plan_validation import TurnPlanValidation
from project.task.flow.loader import FlowLoader
from project.task.flow.models import FlowCatalog


class DialogueEngine:
    def __init__(self,turn_planner:TurnPlanner,
                 turn_plan_validation:TurnPlanValidation
    ):
        self.turn_planner = turn_planner
        self.turn_plan_validation = turn_plan_validation



    async def process_user_message(self, state: DialogueState, user_message: UserMessage) -> ProcessResult:
        """
        处理用户消息，根据历史记录和用户问题，返回机器人回复
        :param state: 当前用户会话状态
        :param user_message: 用户消息
        :return: 处理结果
        """
        # 1.准备当前session
        self._prepare_current_session(state)

        # 2.判断消息类型
        ## 2.1 文本类型消息
        if user_message.type == MessageType.TEXT:
            # 处理文本消息
            messages: list[BotMessage] = await self._execute_text_message(user_message,state)

        ## 2.2 对象类型消息
        else:
            # 处理对象消息
            messages: list[BotMessage] = await self._execute_object_message(user_message)

        # 3.更新state状态
        # 封装一轮对话：一问一答或者一问多答
        turn = Turn(
            turn_id=str(uuid.uuid4()),
            user_message=user_message,
        )
        turn.bot_message.extend(messages)

        state.shared.sessions[-1].turns.append(turn)

        # 4.返回处理结果

    def _prepare_current_session(self, state: DialogueState):
        """
        准备当前session
        :param state: 当前用户会话状态
        :return:
        """
        # 1.判断当前是否有session
        if not state.shared.sessions:
            # 没有session，创建新session
            state.shared.create_session()

        # 2.有session，更新session最后一次活跃时间，判断是否过期
        else:
            # 获取当前session对象
            current_session = state.shared.sessions[-1]
            # 获取当前时间
            now = time.time()
            # 判断是否过期
            if now - current_session.last_activity_at > 60 * 60:
                # 过期，关闭当前session
                state.shared.close_current_session()
                # 过期，创建新session
                state.shared.create_session()
                # 未过期，更新session最后一次活跃时间
            else:
                # 最后一次活跃时间更新为当前时间
                current_session.last_activity_at = now

    async def _execute_text_message(self, user_message,state:DialogueState)->list[BotMessage]:
        yaml_path = Path(__file__).parents[2] / 'flow_config' / 'user_flows.yml'
        flow_catalog: FlowCatalog = FlowLoader().load(yaml_path)

        # 1 根据用户输入的问题，调用TurnPlanner模块，获取意图识别结果
        # 调用LLM，使用参数数据构建提示词
        # 参数：用户问题 历史数据 流程数据 知识检索数据
        turn_plan:TurnPlan = await self.turn_planner.plan(user_message,state,flow_catalog)
        # 2 根据意图识别结果，调用TurnPlanValidation模块，校验意图识别结果
        validation_result:TurnPlanValidationResult = (
            self.turn_plan_validation.validation(turn_plan, state, flow_catalog)
        )

        # 3 校验没有通过，执行反问澄清回复组件
        if not validation_result.valid:
            pass
        # 4 校验通过，根据意图识别结果，执行不同轨道

        ## 任务流程

        ## 知识检索

        ## 闲聊

        # 5 根据不同轨道返回结果
    async def _execute_object_message(self, user_message):
        pass
