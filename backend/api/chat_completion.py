from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from starlette.responses import StreamingResponse

from dependencies.llm_service import LLMServiceDep

router = APIRouter()


class ChatHistoryItem(BaseModel):
    role: str
    content: str


class ChatHistory(BaseModel):
    messages: list[ChatHistoryItem]


@router.post("/chat-completion")
async def chat_completion(data: ChatHistory, llm_service: LLMServiceDep):
    history = [{
        "role": item.role,
        "content": item.content
    } for item in data.messages]

    return StreamingResponse(llm_service.generate_response(history))
