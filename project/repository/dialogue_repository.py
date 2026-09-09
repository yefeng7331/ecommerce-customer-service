"""
@Author:叶枫
@Time:2026/9/8
@Desc: 聊天数据访问层
    当前这个模块主要是负责和数据库交互，实现对聊天记录的增删改查
"""
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from domain.state import DialogueState
from repository.orm.dialogue_state import DialogueStateRecord

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
        # sql实现
        # sql = "SELECT * FROM dialogue_states WHERE sender_id = :sid"
        # result = await self.session.execute(sql, {"sid": sender_id})

        # orm实现
        # 不需要编写sql语句，直接使用sqlalchmy封装的方法实现
        sql = select(DialogueStateRecord).where(
            DialogueStateRecord.sender_id == sender_id)
        result = await self.session.execute(sql)
        record = result.scalar_one_or_none()
        if record:
            # 因为state_json是json字符串，所以需要反序列化为DialogueState对象
            return DIALOGUE_STATE_ADAPTER.validate_json(record.state_json)
        else:
            return DialogueState(sender_id=sender_id)

    # 2 保存当前用户历史会话记录
    async def save_state(self, state:DialogueState):
        # 1. 转换为json字符串
        state_json = DIALOGUE_STATE_ADAPTER.dump_json(state).decode(encoding="utf-8")
        # 2. 保存到数据库,创建添加的语句
        sql = insert(DialogueStateRecord).values(
            sender_id=state.sender_id,
            state_json=state_json
        )
        # 判断表面是否存在sender_id记录
        # 如果存在，更新记录
        # 如果不存在，添加记录
        ## sqlalchemy.dialects.mysql中封装了该类型方法
        on_duplicate_key = sql.on_duplicate_key_update(state_json=state_json)

        await self.session.execute(on_duplicate_key)

        await self.session.commit()

