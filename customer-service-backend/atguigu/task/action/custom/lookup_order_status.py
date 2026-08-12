from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult
from atguigu.infrastructure.shared import fetch_order


class LookupOrderStatusAction(Action):

    name = "action_lookup_order_status"

    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:

        # 1. 获取上一个步骤填充的槽位信息（订单号）
        order_number = state.active_task.slots.get("order_number")

        # 2. 根据订单号查询订单
        data = await  fetch_order(order_number)

        # 3. 更新槽位信息（ActionResult 的 slot_updates）
        if data is None:
            # 查询失败
            return ActionResult(
                slot_updates = {
                    "order_status": "查询失败" ,
                    "order_summary": "暂时无法查询到订单信息，请稍后再试"
                }
            )

        amount = data.get("amount")
        items = data.get("items")

        # 订单标题
        suffix = "" if len(items) == 1 else "等"
        title_part = f"包含商品：{items[0].get('title')}{suffix}"
        order_summary = f"订单金额 ¥{amount}, {title_part}"

        # 查询成功
        return ActionResult(
            slot_updates={
                "order_status":  data.get("status_desc") or data.get("status"),
                "order_summary": order_summary
            }
        )


