from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult


class B(Action):

    name = "action_b"

    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:

       pass
