import logging

from fastapi import FastAPI

from backend.app.api.v1.routers import v1_router
from backend.app.config.logging_config import logging_setup
from backend.app.config.settings import backend_settings


logging_setup()

logger = logging.getLogger(__name__)

app = FastAPI(title=backend_settings.app_name)

app.include_router(v1_router)
