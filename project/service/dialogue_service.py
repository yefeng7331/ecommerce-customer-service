"""
@Author:叶枫
@Time:2026/9/8
@Desc: 聊天服务层
"""
from domain.message import BotMessage
from domain.state import DialogueState
from engine.dialogue_engine import DialogueEngine
from project.domain.message import UserMessage, ProcessResult
from repository.dialogue_repository import DialogueRepository



class DialogueService:
    def __init__(self, repository: DialogueRepository, engine: DialogueEngine):
        self.engine = engine
        self.repository = repository

    async def process_user_message(self, user_message:UserMessage)->ProcessResult:
        # 1 根据api层传递sender_id,调用repository层查询当前用户历史会话记录
        sender_id = user_message.sender_id
        state:DialogueState = await self.repository.load_state(sender_id)

        # todo 2 根据查询历史记录 + 用户问题 调用engine层处理用户消息
        # self.engine.process_user_message(state, user_message)

        # 3 把当前这一次对话，调用repository层保存数据库里面
        await self.repository.save_state(state)

        # 4 返回engine层处理结果
        return ProcessResult(
            sender_id=sender_id,
            message_id=user_message.message_id,
            messages=[BotMessage(
                text="你好",
                object=None
            )]

        )



"""
1 根据api层传递sender_id,调用repository层查询当前用户历史会话记录
2 根据查询历史记录 + 用户问题 调用engine层处理用户消息
3 把当前这一次对话，调用repository层保存数据库里面
4 返回engine层处理结果 
"""
