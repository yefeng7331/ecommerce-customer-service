"""
@Author:叶枫
@Time:2026/9/8
@Desc: 聊天数据访问层
    当前这个模块主要是负责和数据库交互，实现对聊天记录的增删改查
"""
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from domain.state import DialogueState

# 序列化和反序列化
## 对象==>json字符串 jump_json
## json字符串==>对象 validate_json
# 使用类型适配器实现序列化和反序列化
DIALOGUE_STATE_ADAPTER = TypeAdapter(DialogueState)

class DialogueRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 1 根据sender_id查询当前用户历史会话记录
    # 查询数据库返回json字符串，反序列化为DialogueState对象
    async def load_state(self, sender_id):
        pass

    # 2 保存当前用户历史会话记录
    async def save_state(self, state):
        pass
