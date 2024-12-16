import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import router
from app_state import set_state


@asynccontextmanager
async def lifespan(app: FastAPI):
    state = set_state(app)
    download_model_coroutine = state.model_download.download_model(state.settings.MODEL_URI, state.settings.MODEL_PATH)

    asyncio.create_task(download_model_coroutine)  # noqa

    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
