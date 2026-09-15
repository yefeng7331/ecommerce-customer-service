"""
@Author:叶枫
@Time:2026/9/15
@Desc:这个模块是实现澄清回复的模块
# 校验失败返回结果，通过这个模块返回内容给用户
"""
import json
from dataclasses import asdict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from domain.message import BotMessage, UserMessage
from domain.state import DialogueState
from plan.models import ClarifyReason
from prompts.history_builder import HistoryBuilder
from prompts.loader import load_prompt
from utils.llm_client import llm


class ClarifyResponse:
    async def responder(self,
                        reason:ClarifyReason,
                        state:DialogueState,
                        user_message:UserMessage,
                        )->list[BotMessage]:
        # 加载提示词模版
        prompt_text = load_prompt("clarify_respond")
        # 渲染提示词模版
        prompt = PromptTemplate.from_template(
            prompt_text,template_format='jinja2'
        )
        # 创建调用链
        chain = prompt | llm | StrOutputParser()

        # 调用方法
        res = await chain.ainvoke(
                {
                    "reason": reason.value,
                    "clarify_message": self.build_response(reason=reason,state=state),
                    "focused_object":json.dumps(asdict(state.shared.focused_object)
                                                if state.shared.focused_object else None),
                    "history":HistoryBuilder.build(state.shared.sessions[-1].turns),
                    "user_message":HistoryBuilder.render_user_message(user_message)
            }
        )
        return [BotMessage(text=res)]

    def build_response(self, reason:ClarifyReason,state:DialogueState)->str:
        if reason is ClarifyReason.MULTIPLE_TRACKS:
            return (
                "您的问题有多个轨道，我需要您分别回答每个轨道的问题。"
            )
        if reason is ClarifyReason.MISSING_TRACK:
            return (
                "您的问题缺少一个轨道，我需要您补充完整。"
            )

        if reason is ClarifyReason.MISSING_TASK_COMMANDS:
            return (
                "您的问题缺少任务命令，我需要您补充完整。"
            )
        if reason is ClarifyReason.MISSING_KNOWLEDGE_INTENT:
            return (
                "您的问题缺少知识意图，我需要您补充完整。"
            )
        if reason is ClarifyReason.MISSING_FOCUSED_OBJECT:
            return (
                "您的问题缺少聚焦对象，我需要您补充完整。"
            )
        if reason is ClarifyReason.OBJECT_REQUIRES_INTENT:
            return (
                "您的问题缺少聚焦对象的意图，我需要您补充完整。"
            )
        if reason is ClarifyReason.INVALID_TASK_COMMAND:
            return (
                "您的问题缺少任务命令，我需要您补充完整。"
            )
        if reason is ClarifyReason.UNKNOWN_KNOWLEDGE_INTENT:
            return (
                "您的问题缺少知识意图，我需要您补充完整。"
            )
