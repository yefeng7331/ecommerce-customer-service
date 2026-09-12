"""
@Author:叶枫
@Time:2026/9/11
@Desc: 意图识别模块
"""
import json
from dataclasses import asdict

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from project.domain.message import UserMessage
from project.domain.state import DialogueState
from project.plan.models import TurnPlan
from project.prompts.history_builder import HistoryBuilder
from project.prompts.loader import load_prompt
from project.task.flow.models import FlowCatalog, Flow
from project.utils.llm_client import llm

"""
    这个模块是用户问题意图识别
"""


# 提示词工程模板
# RAFT
## Role: 明确告诉LLM当前身份角色是什么
## Action: 明确告诉LLM当前任务是什么
## Formate: 明确告诉LLM当前任务的格式是什么，输出示例，如：{"command": "track", "object": "1233"}等
## Tone: 明确告诉LLM当前任务的语气是什么，如：正式、非正式、专业、非专业等

class TurnPlanner:
    async def plan(self, user_message: UserMessage, state: DialogueState, flow_catalog: FlowCatalog) -> TurnPlan:
        # 加载提示词
        prompt_text = load_prompt("turn_plan")
        prompt = PromptTemplate.from_template(
            prompt_text,
            template_format='jinja2'
        )

        # 创建调用链 langchain
        chain = prompt | llm | JsonOutputParser()

        user_message = HistoryBuilder.render_user_message(user_message)

        #最近一次session里面多轮对话记录
        turns = state.shared.sessions[-1].turns
        # 对话历史
        conversation_history = HistoryBuilder.build(turns)
        # 对象类型消息
        focused_object_json = json.dumps(asdict(state.shared.focused_object) if state.shared.focused_object else None)
        #任务流程中特有数据
        task_commands_json = json.dumps(asdict(state.tasks) if state.tasks else None)
        # flows_json yaml文件流程数据
        ## 把yaml文件流程数据flow_catalog,不包含步骤数据
        flows:dict[str,Flow] = flow_catalog.flows
        # 把flows字典进行遍历，得到其中的每个flow,去掉每个flow的steps
        flows_json = [
            {
                k:v for k,v in asdict(flow).items() if k != 'step'
            }
            for flow in flows.values()

        ]
        # todo 执行前需要获取一下提示词里面的数据，包括用户问题 历史数据 流程数据 知识检索数据
        # 执行invoke方法，得到结果
        plan = await chain.ainvoke({
            "user_message": user_message, # 用户问题
            "flows_json": flows_json, # 流程数据
            "knowledge_intents_json": {}, # 知识检索数据 后续完善
            "task_state_json": task_commands_json, # 任务状态
            "focused_object_json": focused_object_json, # 焦点对象
            "conversation_history": conversation_history # 对话历史
        })
        # 把LLM返回JSON字符串转换为TurnPlan对象
        return TurnPlan.from_dict(plan)

