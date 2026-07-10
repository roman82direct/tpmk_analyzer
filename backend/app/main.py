from fastapi import FastAPI

from backend.app.api.v1.routers import v1_router
from backend.app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(v1_router)
