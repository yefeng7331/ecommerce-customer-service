"""
@Author:叶枫
@Time:2026/9/14
@Desc:渲染客服回复
        这个模块作用是response类型步骤，数据渲染到客服回复中去
"""
from jinja2 import Template

from domain.message import BotMessage
from domain.state import DialogueState
from task.response.models import ResponseTemplate, ResponseMode


class ResponseTemplateRender:
    # 渲染
    def render_response(self,
                        template: ResponseTemplate,
                        state: DialogueState) -> BotMessage:
        # jinja2
        if template.mode == ResponseMode.STATIC:
            # 先判断活跃任务是否存在，避免空指针
            if not state.tasks.active:
                raise RuntimeError("渲染静态模板时必须存在活跃任务")
            template_obj = Template(template.text)
            rendered_text = template_obj.render(slots=state.tasks.active.slots)
            return BotMessage(text=rendered_text)
        elif template.mode == ResponseMode.REPHRASE:
            # 后续实现重写逻辑
            raise NotImplementedError("REPHRASE模式暂未实现")
        elif template.mode == ResponseMode.GENERATE:
            # 后续实现生成逻辑
            raise NotImplementedError("GENERATE模式暂未实现")
        else:
            # 处理未知模式，避免返回None
            raise ValueError(f"不支持的响应模式: {template.mode}")
