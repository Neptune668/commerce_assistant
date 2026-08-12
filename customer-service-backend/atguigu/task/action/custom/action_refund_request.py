# atguigu/task/action/custom/action_refund_request.py
from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.infrastructure.shared import submit_refund_request
from atguigu.task.action.base import Action, ActionResult


class RefundRequestAction(Action):

    name = "action_refund_request"

    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:

        # 1. 获取上一个步骤填充的槽位信息
        order_number = state.active_task.slots.get("order_number")
        refund_reason = state.active_task.slots.get("refund_reason")

        # 2. 根据订单号查询物流
        data = await submit_refund_request(order_number, refund_reason)

        # 3. 更新槽位信息（ActionResult 的 slot_updates）
        if data is None:
            # 查询失败
            return ActionResult(
                slot_updates={
                    "order_number": "查询失败",
                    "refund_reason": "查询失败",
                }
            )

        return ActionResult()