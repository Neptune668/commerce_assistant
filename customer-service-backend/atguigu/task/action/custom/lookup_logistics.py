from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult
from atguigu.infrastructure.shared import fetch_logistics


class LookupLogisticsAction(Action):

    name = "action_lookup_logistics"

    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:
        # 1. 获取上一个步骤填充的槽位信息（订单号）
        order_number = state.active_task.slots.get("order_number")

        # 2. 根据订单号查询物流
        data = await fetch_logistics(order_number)

        # 3. 更新槽位信息（ActionResult 的 slot_updates）
        if data is None:
            # 查询失败
            return ActionResult(
                slot_updates={
                    "tracking_number": "未知",
                    "logistics_company": "未知",
                    "logistics_status": "暂时无法查到物流信息，请稍后再试。",
                }
            )

        return ActionResult(
            slot_updates={
                "tracking_number": data.get("tracking_number"),
                "logistics_company": data.get("logistics_company"),
                "logistics_status": data.get("status_desc") or data.get("status")
            }
        )
