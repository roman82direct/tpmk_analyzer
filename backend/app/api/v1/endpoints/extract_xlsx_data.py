from fastapi import APIRouter


router = APIRouter()


@router.get('/')
async def extract_data():
    """
    Получить данные из xlsx.

    Ежедневная загрузка данных о продажах.

    Только для админа.
    """
    return {'message': '... loading data ...'}
