# 1. 通过API接口将接收到的数据转换成领域模型UserMessage
from atguigu.api.routers.chat_router import _build_user_message
from atguigu.api.schemas import ChatRequest, ChatObject
from atguigu.domain.messages import UserMessage


chat_request: ChatRequest = ChatRequest(
    sender_id="1",
    message_id="1",
    text="你好",
    object=ChatObject(
        type="image",
        id="11",
        title="22",
        attributes={
            "a": "aa"
        }
    )
)
user_message: UserMessage = _build_user_message(chat_request)
print(user_message)