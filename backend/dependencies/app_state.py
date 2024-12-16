from starlette.requests import Request

from app_state import AppState, get_state as get_app_state


def get_state(request: Request) -> AppState:
    return get_app_state(request.app)