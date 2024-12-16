from functools import cached_property
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # address to download the model from
    MODEL_URI: str = "https://huggingface.co/second-state/Llava-v1.5-7B-GGUF/resolve/main/llava-v1.5-7b-Q4_K_M.gguf"
    # a path that the model will be downloaded to
    MODEL_FOLDER: Path = "models"
    # setting for the model inference
    CHAT_FORMAT: str = "vicuna"

    @cached_property
    def MODEL_PATH(self) -> Path:
        filename = self.MODEL_URI.split("/")[-1]
        path = self.MODEL_FOLDER / filename
        return path

    @cached_property
    def MODEL_NAME(self) -> str:
        filename = self.MODEL_URI.split("/")[-1]
        model_name = filename.removesuffix(".gguf")
        return model_name
