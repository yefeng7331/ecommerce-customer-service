"""
@Author:叶枫
@Time:2026/9/8
@Desc:创建FastAPI对象
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from project.api.chat_router import chat_router
from project.utils.database import init_db_engine, close_engine


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     init_db_engine()
#     try:
#         yield
#     finally:
#         await close_engine()


app = FastAPI()

app.include_router(chat_router)
