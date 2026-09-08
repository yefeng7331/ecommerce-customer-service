"""
@Author:叶枫
@Time:2026/9/8
@Desc:创建FastAPI对象
"""

from fastapi import FastAPI

from project.api.chat_router import chat_router

app = FastAPI()

app.include_router(chat_router)
