from fastapi import APIRouter

from app.api.v1 import load_xlsx_router


v1_router = APIRouter()

v1_router.include_router(load_xlsx_router,
                         prefix='/load-data',
                         tags=['Загрузка данных из эксель'])
