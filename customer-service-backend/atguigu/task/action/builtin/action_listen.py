import asyncio
from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult


class ActionListen(Action):
    """什么都不做，只监听用户的输入"""

    name = "action_listen"

    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:
        # pass
        print("action_listen")
        return ActionResult()


if __name__ == '__main__':

    action = ActionListen()
    asyncio.run(action.run(None, None))



