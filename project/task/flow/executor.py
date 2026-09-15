"""
@Author:叶枫
@Time:2026/9/14
@Desc:任务流程执行器
        这个模块的作用适用于推进流程的步骤
"""
from project.domain.message import BotMessage, UserMessage
from project.domain.state import DialogueState
from project.task.action.base import ActionCall, ActionResult
from project.task.action.runner import ActionRunner
from project.task.flow.links import FlowStepLink, ConditionalLink, FallbackLink
from project.task.flow.models import FlowCatalog, Flow
from project.task.flow.steps import FlowStep, StartFlowStep, ResponseFlowStep, CollectSlotStep, ActionFlowStep, EndFlowStep
from project.task.response.render import ResponseTemplateRender


class FlowExecutor:
    def __init__(self, response_render: ResponseTemplateRender, action_runner: ActionRunner):
        self.action_runner: ActionRunner = action_runner
        self.response_render: ResponseTemplateRender = response_render

    async def run_step(self,
                       state: DialogueState,
                       flows: FlowCatalog,
                       ) -> list[BotMessage]:
        """
        执行任务流程的步骤
        :param state: 状态对象
        :param flows: 任务流程目录
        :return: 客服回复
        """
        bot_messages: list[BotMessage] = []

        # 没有任务在执行，直接返回空列表
        if not state.tasks.active:
            return bot_messages

        # 有活跃任务
        # 约定限制每个任务流程最多执行100次
        for _ in range(100):
            # 从当前活跃任务中获取步骤数据
            flow: Flow = flows.get_flow_by_id(state.tasks.active.flow_id)
            step: FlowStep = flow.get_step_by_id(state.tasks.active.step_id)
            # 判断不同类型的步骤
            # 五种
            if isinstance(step, StartFlowStep):
                """
                
                StartFlowStep
                从当前任务中获取任务流程数据
                从聚焦对象中获取到任务流程数据
                从聚焦对象中获取到用户消息
                """
                self._run_next_step(state, step)
                continue

            if isinstance(step, ResponseFlowStep):
                """
                ResponseFlowStep
                渲染客服回复
                jinja2模板
                """
                # todo 渲染客服回复
                bot_message: BotMessage = self.response_render.render_response(
                    step.template,
                    state
                )
                # 放到当前bot_messages中
                bot_messages.append(bot_message)
                # 推进下一步
                self._run_next_step(state, step)
                continue

            if isinstance(step, CollectSlotStep):
                """
                CollectSlotStep
                收集槽槽位
                从当前任务中获取槽位数据
                从聚焦对象中获取到槽位数据
                """
                # 调用方法，返回Bool，约定需要用户输入 true,不需要用户输入 false
                need_user_input: bool = self._run_collect_step(state, step, bot_messages)
                # 判断
                if need_user_input:
                    return bot_messages

                else:  # 有槽位数据，不需要用户输入
                    self._run_next_step(state, step)
                    continue

            if isinstance(step, ActionFlowStep):
                """
                ActionFlowStep
                执行具体业务的方法，调用中台系统的接口实现具体功能
                """
                action_name = step.action
                action_call = ActionCall(action_name=action_name)

                # 调用action运行器
                action_result:ActionResult = await self.action_runner.run(state=state, action_call=action_call)


                # 为了后面从槽位获取数据渲染
                state.tasks.active.slots.update(action_result.slot_updates)

                # 推进到下一步
                self._run_next_step(state, step)
                continue

            if isinstance(step, EndFlowStep):
                """
                EndFlowStep
                当前流程结束
                """
            state.tasks.active = None
            return bot_messages

    def _run_next_step(self, state, step):
        # 获取当前步骤next的属性值
        next_step_id = self._get_next_step(state, step.next)
        # 把获取next属性值变成当前步骤id
        state.tasks.active.step_id = next_step_id

    # next属性值的方法
    def _get_next_step(self, state:DialogueState, next:list[FlowStepLink])->str:
        """
        获取next属性值
        :param state: 状态对象
        :param next: next属性值
        :return: next属性值
        """
        # 如果next字符串，无条件跳转
        if len(next)==1:
            return next[0].target
        # 如果next是表达式，需要根据表达式判断跳转 if then else
        # next列表遍历
        for link in next:
            if isinstance(link, ConditionalLink):
                # 判断表达式是否成立
                result: bool = bool(eval(link.condition,{},
                          {"slots":state.tasks.active.slots}))
                if result:
                    return link.target
                continue


            if isinstance(link, FallbackLink):
                return link.target

    def _run_collect_step(self, state:DialogueState, step:CollectSlotStep, bot_messages:list[BotMessage])->bool:
        #1 从当前活跃的任务中是否有槽位数据
        slots:dict = state.tasks.active.slots
        slot_value = slots.get(step.slot_name)
        # 2 如果活跃任务没有槽位数据，到focused_object
        # 如果找到了槽位数据，将其放到active里面
        if not slot_value:
            self.get_focused_object_slot_value(step,state)

        # 3 在上面两个地方找槽位数据，如果都没有找到，需要用户输入
        slot_value = state.tasks.active.slots.get(step.slot_name)
        if not slot_value:
            # 把等待用户输入的提示信息返回给用户，渲染一下返回信息
            bot_message:BotMessage = (self.response_render.render_response(step.template,state))
            bot_messages.append(bot_message)
            return True
        else: # 如果找到了，就不需要用户输入了
            return False




    def get_focused_object_slot_value(self, step, state):
        # focused_object是否为空
        # 如果找到了放到active里面
        if not state.shared.focused_object:
            return
        # 如果focused_object不为空，从focused_object中获取槽位数据
        if step.slot_name=='order_number' and state.shared.focused_object.type=='order':
            # 从order中获取槽位数据
            state.tasks.active.slots.update({step.slot_name:state.shared.focused_object.id})
            return
        if step.slot_name=='product_id' and state.shared.focused_object.type=='product':
            # 从product中获取槽位数据
            state.tasks.active.slots.update({step.slot_name:state.shared.focused_object.id})
            return




# eval方法
if __name__ == "__main__":
    data = {
        "slots":{
            "product_id":"abcd"
        }
    }
    res = bool(eval("slots.get('product_id')",{},data))
    print(res)
