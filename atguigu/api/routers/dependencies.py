from pathlib import Path

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from atguigu.clarify.responder import ClarifyResponder
from atguigu.engine.dialogue_engine import DialogueEngine

# 必须通过这种方式引入database，需要的时候再获取： database.async_session()
from atguigu.infrastructure import database
from atguigu.knowledge.handler import KnowledgeHandler
from atguigu.knowledge.intents import KNOWLEDGE_INTENTS
from atguigu.plan.turn_planner import TurnPlanner
from atguigu.plan.turn_validator import TurnPlanValidator

# 不要通过这种方式引入async_session，会是一个NoneType
# from atguigu.infrastructure.database import async_session
from atguigu.repository.dialogue_state_repository import DialogueStateRepository
from atguigu.service.dialogue_service import DialogueService
from atguigu.task.command.processor import CommandProcessor
from atguigu.task.flow.loader import FlowLoader
from atguigu.task.handler import TaskHandler

"""
1. 请求从前端交给FastAPI，FastAPI作为Web层调用Service层
2. Service层调用Repository层
3. Repository初始化的时候先通过get_session()方法将self.session进行依赖注入
4. 执行 async with async_session() as session:
5. 从数据库连接池中取出一个session对象： yield session
6. yield 使当前 get_session() 停止执行，把session对象向外提供，交给Repository使用
7. 一直到此次调用中相关的Repository，Service，Web全部逻辑执行完成，返回响应之后，程序会回到yield下方
8. 退出 async with，session关闭/归还给数据库连接池

总结：yield之前 = 创建资源阶段，yield向外层交付资源。请求处理完毕后，执行yield上下文的资源清理工作，释放资源

"""
# 创建session实例
async def get_session():
    # 异步方式获取session对象
    async with database.async_session() as session:

        # 通过 yield 将session返回，使程序停留在此位置，直到外层调用执行完毕
        yield session

# 创建Repository的实例
async def get_dialogue_state_repository(session: AsyncSession = Depends(get_session)):

    return DialogueStateRepository(session)

# 创建引擎实例
async def get_engine():
    base_path = Path(__file__).parents[3]
    user_flow_path = base_path / "flow_config" / "user_flows.yml"
    system_flow_path = base_path / "flow_config" / "system_flows.yml"
    loader = FlowLoader()
    flows_list = loader.load_many([user_flow_path, system_flow_path])

    return DialogueEngine(
        turn_planner=TurnPlanner(),
        task_handler=TaskHandler(flows=flows_list, command_processor=CommandProcessor()),
        knowledge_handler=KnowledgeHandler(knowledge_intends=KNOWLEDGE_INTENTS),
        clarify_responder=ClarifyResponder(),
        turn_plan_validator=TurnPlanValidator(),
    )

# 创建Service的实例
async def get_dialogue_service(
        dialogue_state_repository: DialogueStateRepository = Depends(get_dialogue_state_repository),
        dialogue_engine: DialogueEngine = Depends(get_engine)
):
    return DialogueService(
        dialogue_state_repository=dialogue_state_repository,
        dialogue_engine=dialogue_engine
    )

