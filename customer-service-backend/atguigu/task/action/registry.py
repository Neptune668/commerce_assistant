from atguigu.task.action.base import Action


class ActionRegistry:

    def __init__(self) -> None:
        self._actions: dict[str, Action] = {}

    def register(self, action: Action) -> None:
        """注册一个action"""
        self._actions[action.name] = action

    def get(self, name: str) -> Action:
        """获取一个action"""
        if name not in self._actions:
            raise KeyError(f"未知action: {name}")
        return self._actions[name]