from typing import Annotated

from fastapi import Depends

from app_state import AppState
from dependencies.app_state import get_state
from services.llm_downloader import ModelDownloadService


async def _get_downloader(state: AppState = Depends(get_state)) -> ModelDownloadService:
    return state.model_download


ModelDownloadServiceDep = Annotated[ModelDownloadService, Depends(_get_downloader)]
