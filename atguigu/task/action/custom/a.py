from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult
from atguigu.task.action.custom.shared import fetch_logistics

from atguigu.task.action.custom.lookup_order_status import LookupOrderStatusAction


class A(Action):

    name = "action_a"

    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:

       pass
