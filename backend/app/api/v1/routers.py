from fastapi import APIRouter

from app.api.v1 import upload_router


v1_router = APIRouter()

v1_router.include_router(upload_router, prefix='/load-data',
                         tags=['Загрузка данных из эксель'])
