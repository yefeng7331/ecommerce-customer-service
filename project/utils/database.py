"""
@Author:叶枫
@Time:2026/9/8
@Desc: 数据库
        模块作用：封装数据库操作，提供调用接口
"""
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine

from config.config import settings

# 1.定义两个变量
# engine引擎  session会话  ———异步
engine:AsyncEngine | None = None
# async_sessionmaker 异步会话工厂,通过工厂创建异步会话AsyncSession
async_session:async_sessionmaker[AsyncSession]

# 2.两个方法
# 初始化方法
def init_db_engine():
    global engine, async_session
    # 创建引擎
    engine = create_async_engine(settings.database_url,echo=True) #echo=True 打印底层sql语句
    # 创建异步会话工厂
    async_session = async_sessionmaker(engine, expire_on_commit=False) #expire_on_commit=False 不自动过期

# 关闭方法
async def close_engine():
    await engine.dispose()

async def test():
    init_db_engine()
    # 创建与数据库连接，获取会话对象
    async with async_session() as session:
        result = await session.execute(text("select 1"))
        print(result.fetchone())
    await close_engine()



if __name__ == "__main__":
    asyncio.run(test())

