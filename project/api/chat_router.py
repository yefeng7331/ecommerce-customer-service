"""
@Author:叶枫
@Time:2026/9/8
@Desc:创建聊天路由
"""
import uuid
from dataclasses import asdict

from fastapi import APIRouter, Depends

from project.api.schemas import ChatRequest, ChatResponse, ChatMessage, ChatObject
from project.config.depends import get_dialogue_service
from project.domain.message import ProcessResult, UserMessage, MessageObject, MessageType
from project.service.dialogue_service import DialogueService

chat_router = APIRouter()


# 把API层ChatRequest对象转换为service层ChatRequest对象
##   ChatRequest -> UserMessage
def _build_user_message(chat_request: ChatRequest,service:DialogueService=Depends(get_dialogue_service)):
    return UserMessage(
        sender_id=chat_request.sender_id,
        message_id=chat_request.message_id
        if chat_request.message_id else str(uuid.uuid4()),
        type=MessageType.TEXT if chat_request.text else MessageType.OBJECT,
        text=chat_request.text,
        # ChatObject ==> MessageObject
        # object=chat_request.object if UserMessage.object else ChetRequest.object
        object=MessageObject(
            id=chat_request.object.id,
            type=chat_request.object.type,
            title=chat_request.object.title,
            attributes=chat_request.object.attributes
            # 这样写会更好 **asdict(chat_request.object) 因为asdict()方法会自动处理嵌套对象，而直接赋值会报错
        ) if chat_request.object else None
    )


# 把service层ChatResponse对象转换为API层ChatResponse对象
##   ProcessResult -> ChatResponse
def _build_chat_response(process_result: ProcessResult) -> ChatResponse:
    return ChatResponse(
        sender_id=process_result.sender_id,
        message_id=process_result.message_id,
        # 遍历process_result其中messages列表得到每个BotMessage对象
        messages=[
            ChatMessage(
                text=bot_message.text,
                object=ChatObject(
                    **asdict(bot_message.object)
                ) if bot_message.object else None
            )
            for bot_message in process_result.messages
        ]
    )


@chat_router.post("/api/chat")
async def chat(chat_request: ChatRequest) -> ChatResponse:
    # 1.接收前端请求数据,封装成ChatRequest模型

    # 2.把API层ChatRequest对象转换为service层ChatRequest对象
    user_message: UserMessage = _build_user_message(chat_request)
    # 3.注入service对象，调用service层方法
    # todo:完善，注入对象抽取
    service: DialogueService = Depends(get_dialogue_service)
    process_result: ProcessResult = service.process_user_message(user_message)

    # 4.获取service方法返回结果，把service返回类型转换为ChatResponse类型
    chat_response: ChatResponse = _build_chat_response(process_result)
    # 5.返回ChatResponse对象
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
