# atguigu/task/flow/executor.py

from atguigu.domain.state import DialogueState
from atguigu.task.flow.flows import FlowsList
from atguigu.task.action.runner import ActionRunner

class FlowExecutor:
    """
    流程执行器：推进yaml中定义的业务任务流程以及系统任务流程
    """

    async def run_task(self,state: DialogueState,flows: FlowsList,action_runner: ActionRunner):

        pass