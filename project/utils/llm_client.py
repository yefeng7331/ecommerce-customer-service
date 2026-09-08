"""
@Author:叶枫
@Time:2026/9/8
@Desc: LLM客户端
        模块作用：封装LLM接口，提供调用接口
"""
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage

from project.config.config import settings

llm:BaseChatModel = init_chat_model(
    model=settings.LLM_MODEL,
    model_provider="openai",
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url,
    # 模型参数(温度)
    temperature=0
)

if __name__ == "__main__":
    print(llm.invoke("你好").content.strip())

