# atguigu/engine/builder.py

from pathlib import Path

from atguigu.chitchat.handler import ChitChatHandler
from atguigu.chitchat.responder import ChitChatResponder
from atguigu.clarify.responder import ClarifyResponder
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.knowledge.handler import KnowledgeHandler
from atguigu.knowledge.intents import KNOWLEDGE_INTENTS
from atguigu.knowledge.providers import ProductAPIProvider, OrderAPIProvider, FAQProvider, RAGProvider
from atguigu.knowledge.registry import KnowledgeProviderRegistry
from atguigu.knowledge.responder import KnowledgeResponder
from atguigu.plan.turn_planner import TurnPlanner
from atguigu.plan.turn_validator import TurnPlanValidator
from atguigu.task.action.builder import build_action_runner
from atguigu.task.command.processor import CommandProcessor
from atguigu.task.flow.executor import FlowExecutor
from atguigu.task.flow.loader import FlowLoader
from atguigu.task.handler import TaskHandler


def build_dialogue_engine():
    base_path = Path(__file__).parents[2]
    user_flow_path = base_path / "flow_config" / "user_flows.yml"
    system_flow_path = base_path / "flow_config" / "system_flows.yml"
    loader = FlowLoader()
    flows_list = loader.load_many([user_flow_path, system_flow_path])

    return DialogueEngine(

        turn_planner=TurnPlanner(),
        task_handler=TaskHandler(
            flows=flows_list,
            command_processor=CommandProcessor(),
            action_runner=build_action_runner(),
            flow_executor=FlowExecutor()),

        knowledge_handler=KnowledgeHandler(

            knowledge_intents=KNOWLEDGE_INTENTS,

            # TODO 优化成动态读取KnowledgeProvider的子类的形式
            provider_registry = KnowledgeProviderRegistry(providers = [
                ProductAPIProvider(),OrderAPIProvider(),FAQProvider(),RAGProvider()
            ]),

            knowledge_responder = KnowledgeResponder()

        ),
        chitchat_handler=ChitChatHandler(ChitChatResponder()),
        clarify_responder=ClarifyResponder(),
        turn_plan_validator=TurnPlanValidator(),
    )