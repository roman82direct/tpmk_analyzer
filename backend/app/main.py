from fastapi import FastAPI

from backend.app.api.v1.routers import v1_router
from app_config.config import backend_settings

app = FastAPI(title=backend_settings.app_name)

app.include_router(v1_router)
