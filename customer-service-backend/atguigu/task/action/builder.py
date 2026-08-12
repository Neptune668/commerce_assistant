import importlib
import inspect
import pkgutil

from atguigu.task.action.base import Action
from atguigu.task.action.builtin.action_listen import ActionListen
from atguigu.task.action.builtin.action_response import ActionResponse
from atguigu.task.action.registry import ActionRegistry
from atguigu.task.action.runner import ActionRunner


def register_builtin_actions(action_runner: ActionRunner):
    """手动注册内置action"""

    action_listen = ActionListen()
    action_response = ActionResponse()
    action_runner.registry.register(action_listen)
    action_runner.registry.register(action_response)


def register_custom_actions(action_runner: ActionRunner):

    # 获取custom包
    package = importlib.import_module("atguigu.task.action.custom")

    # 在path路径下找到前缀是prefix的所有模块
    for _, module_name, is_pkg in pkgutil.iter_modules(path=package.__path__, prefix=f"{package.__name__}."):

        # 只处理模块，不处理子包
        if is_pkg:
            continue

        # 拿到当前模块
        module = importlib.import_module(module_name)

        # 获取当前模块下的所有成员
        for _, clz in inspect.getmembers(module, inspect.isclass):

            # 只过滤Action 的子类，也不要Action
            if not issubclass(clz, Action) or clz is Action:
                continue

            if clz.__module__ != module.__name__:
                continue

            # 将当前clz注册到注册表
            action_runner.registry.register(clz())


def build_action_runner() -> ActionRunner:

    # 初始化action_runner
    action_runner = ActionRunner(ActionRegistry())

    # 注册内置action
    register_builtin_actions(action_runner)

    # 注册自定义action
    register_custom_actions(action_runner)

    return action_runner

if __name__ == '__main__':

    build_action_runner()

    print(123)

    # # 获取custom包
    # package = importlib.import_module("atguigu.task.action.custom")
    #
    # # 迭代custom包下的子包和模块
    # for _, module_name, is_pkg in pkgutil.iter_modules(path=package.__path__, prefix=f"{package.__name__}."):
    #
    #     # 只处理模块，不处理子包
    #     if is_pkg:
    #         continue
    #
    #     # 拿到当前模块
    #     module = importlib.import_module(module_name)
    #
    #     # 获取当前模块下的所有成员
    #     for _, obj in inspect.getmembers(module, inspect.isclass):
    #
    #         # 只过滤Action 的子类，也不要Action
    #         if not issubclass(obj, Action) or obj is Action:
    #             continue
    #
    #         if obj.__module__ != module.__name__:
    #             continue
    #
    #         # 将当前obj注册到注册表



