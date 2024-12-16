from typing import Annotated

from fastapi import Depends

from app_state import AppState
from dependencies.app_state import get_state
from settings import Settings


def _get_settings(app_state: AppState = Depends(get_state)) -> Settings:
    return app_state.settings


SettingsDep = Annotated[Settings, Depends(_get_settings)]