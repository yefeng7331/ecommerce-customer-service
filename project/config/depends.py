"""
@Author:叶枫
@Time:2026/9/9
@Desc: 依赖注入层
"""


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project.engine.dialogue_engine import DialogueEngine
from project.plan.turn_plan import TurnPlanner
from project.plan.turn_plan_validation import TurnPlanValidation
from project.service.dialogue_service import DialogueService
from project.repository.dialogue_repository import DialogueRepository
from project.utils import database


"""
依赖注入层
    api -- service -- repository -- session
              |
              |
            engine -- ?
"""

# 创建引擎层对象
async def get_dialogue_engine():
    turn_planner = TurnPlanner()
    turn_plan_validation = TurnPlanValidation()
    return DialogueEngine(
        turn_planner=turn_planner,
        turn_plan_validation=turn_plan_validation
    )

# 数据库操作session对象
async def get_session():
    async with database.async_session() as session:
        # 暂停执行，等待调用者使用session
        yield session

# 创建仓库层对象
async def get_repository(session: AsyncSession = Depends(get_session)):
    return DialogueRepository(session=session)


async def get_dialogue_service(
        repository: DialogueRepository=Depends(get_repository),
        engine: DialogueEngine=Depends(get_dialogue_engine),
):
    return DialogueService(repository=repository, engine=engine)


