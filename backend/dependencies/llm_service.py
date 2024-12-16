from typing import Annotated

from fastapi import Depends
from llama_cpp import Llama
from functools import lru_cache

from dependencies.settings import SettingsDep
from services.llm_service import LLMInteractionService
from settings import Settings


@lru_cache(maxsize=1)
def get_llm(model_path: str, chat_format: str) -> Llama:
    """
    FastAPI dependency that provides the LLM model instance.
    The lru_cache ensures we only create one instance of the model.
    """
    return Llama(
        model_path=model_path,
        n_ctx=8000,
        n_threads=2,
        n_gpu_layers=0,
        chat_format=chat_format,
    )


def _get_llm_service(settings: SettingsDep) -> LLMInteractionService:
    """
    FastAPI dependency that provides the LLM interaction service.
    The lru_cache ensures we only create one instance of the service.
    """
    return LLMInteractionService(get_llm(settings.MODEL_PATH.as_posix(), settings.CHAT_FORMAT))


LLMServiceDep = Annotated[LLMInteractionService, Depends(_get_llm_service)]