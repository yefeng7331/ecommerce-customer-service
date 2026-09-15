"""
@Author:叶枫
@Time:2026/9/15
@Desc:查询订单状态操作类
"""
from config.config import Settings
from domain.state import DialogueState
from task.action.base import Action, ActionResult
from utils import http_client


# 查询订单状态
class ActionLookupOrderStatus(Action):
    name = 'action_lookup_order_status'
    async def run(self, state: DialogueState):
        # 从state中获取订单号
        order_number = state.tasks.active.slots.get('order_number')
        if not order_number:
            raise '未查到订单号'

        # 拼接中台查询订单状态接口地址
        url = f'{Settings.commerce_api_base_url}/orders/{order_number}'

        response = await http_client.http_client.get(url)
        data = await response.json().get('data','未知订单状态')
        return ActionResult(slot_updates={
            'order_status': data.get('order_status','未知状态'),
            'order_summary': data.get('order_summary','未知订单摘要'),
        })
