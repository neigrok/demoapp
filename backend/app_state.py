from fastapi import FastAPI

from services.llm_downloader import ModelDownloadService
from settings import Settings
from utils.downloader import AsyncFileDownloader


class AppState:
    __slots__ = ("settings", "model_download")

    def __init__(self, settings: Settings, model_download: ModelDownloadService):
        self.settings: Settings = settings
        self.model_download: ModelDownloadService = model_download


def set_state(app: FastAPI) -> AppState:
    settings = Settings()

    state = AppState(
        settings=settings,
        model_download=ModelDownloadService(
            downloader=AsyncFileDownloader(settings.MODEL_URI, settings.MODEL_PATH)
        )
    )

    app.state.state = state

    return state


def get_state(app: FastAPI) -> AppState:
    return app.state.state