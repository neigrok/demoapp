from fastapi import APIRouter
from pydantic import BaseModel

from dependencies.llm_downloader import ModelDownloadServiceDep
from dependencies.settings import SettingsDep

router = APIRouter()

class ModelInfo(BaseModel):
    progress: float
    model_name: str

@router.get("/model-info", response_model=ModelInfo)
async def model_info(model_downloader: ModelDownloadServiceDep, settings: SettingsDep) -> ModelInfo:
    return ModelInfo(
        progress=model_downloader.get_progress(),
        model_name=settings.MODEL_NAME,
    )
