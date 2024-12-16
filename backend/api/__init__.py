from fastapi import APIRouter

from .model_info import router as model_info_router
from .chat_completion import router as chat_completion_router

router = APIRouter()
router.include_router(model_info_router)
router.include_router(chat_completion_router)