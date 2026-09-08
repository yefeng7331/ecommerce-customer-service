"""
@Author:叶枫
@Time:2026/9/8
@Desc:创建聊天路由
"""
import uuid

from fastapi import APIRouter

from project.api.schemas import ChatRequest, ChatResponse, ChatMessage

chat_router = APIRouter()

#todo: 聊天路由
@chat_router.post("/api/chat")
async def chat(chat_request: ChatRequest)->ChatResponse:
    #1.接收前端请求数据,封装成ChatRequest模型

    #2.把API层ChatRequest对象转换为service层ChatRequest对象

    #3.注入service对象，调用service层方法

    #4.获取service方法返回结果，把service返回类型转换为ChatResponse类型

    #5.返回ChatResponse对象
    return ChatResponse(
        sender_id=chat_request.sender_id,
        message_id=str(uuid.uuid4()),
        messages=[
            ChatMessage(
                text="hello",
                object=None
            )
        ]
    )





