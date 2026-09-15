"""
@Author:叶枫
@Time:2026/9/15
@Desc:聊天组件
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from domain.message import UserMessage, BotMessage
from domain.state import DialogueState
from prompts.history_builder import HistoryBuilder
from prompts.loader import load_prompt
from utils.llm_client import llm


class Chitchat:
    async def handle(self,
                     user_message:UserMessage,
                     state:DialogueState,
                     )->list[BotMessage]:
        # 1.根据用户消息，调用LLM模型，生成回复
        prompt_text = load_prompt("chitchat_respond")
        prompt = PromptTemplate.from_template(prompt_text,template_format='jinja2')


        chain = prompt | llm | StrOutputParser()

        response = await chain.ainvoke({
            "history":HistoryBuilder.build(state.shared.sessions[-1].turns),
            "user_message":HistoryBuilder.render_user_message(user_message)
            }
        )
        return [BotMessage(text=response)]

