import uuid

from fastapi import APIRouter, Depends

from atguigu.api.routers.dependencies import get_dialogue_service
from atguigu.api.schemas import ChatRequest, ChatResponse, ChatBotMessage, ChatObject, HistoryResponse, HistoryMessage
from atguigu.domain.messages import ProcessResult, UserMessage, MessageType, FocusedObject
from atguigu.service.dialogue_service import DialogueService

router = APIRouter()


@router.post("/api/chat")
async def chat(
        chat_request: ChatRequest,
        dialogue_service: DialogueService = Depends(get_dialogue_service)
) -> ChatResponse:

    # 1. 通过API接口将接收到的数据转换成领域模型UserMessage
    user_message: UserMessage = _build_user_message(chat_request)
    # 2. 调用业务层处理: 传入领域模型UserMessage，获得领域模型ProcessResult
    process_result: ProcessResult = await dialogue_service.process_message(user_message)
    # 3. 通过API接口将领域模型ProcessResult转换成响应数据ChatResponse
    chat_response: ChatResponse = _build_chat_response(process_result)
    return chat_response

def _build_user_message(chat_request: ChatRequest) -> UserMessage:
    """
    将请求数据模型转换为领域数据模型 供业务使用
    :param chat_request:
    :return:
    """
    return UserMessage(
        sender_id=chat_request.sender_id,
        message_id=chat_request.message_id if chat_request.message_id else str(uuid.uuid4()),
        type=MessageType.TEXT if chat_request.text else MessageType.OBJECT,
        text=chat_request.text,
        # 解构时目标对象必须是mapping（例如dict），使用model_dump()将对象转成字典
        object=FocusedObject(**chat_request.object.model_dump(mode="json")) if chat_request.object else None
    )


def _build_chat_response(process_result: ProcessResult) -> ChatResponse:

    return ChatResponse(

        sender_id=process_result.sender_id,
        message_id=process_result.message_id,

        messages=[
            ChatBotMessage(
                text=bot_msg.text,
                # 解构时目标对象必须是mapping（例如dict），使用model_dump()将对象转成字典
                object=ChatObject(**bot_msg.object.model_dump(mode="json")) if bot_msg.object else None
            )
            for bot_msg in process_result.messages
        ]
    )

@router.get("/api/chat/history")
# request: Request 当uvicorn启动时 Request 对象会被自动注入
async def get_history(
        sender_id: str,
        dialogue_service: DialogueService = Depends(get_dialogue_service)) -> HistoryResponse:

    chat_message_response: list[HistoryMessage] = await dialogue_service.load_chat_history(sender_id)
    return HistoryResponse(sender_id=sender_id, messages=chat_message_response)
