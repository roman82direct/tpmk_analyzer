from fastapi import APIRouter

router = APIRouter()


@router.post('/')
async def upload_data():
    """
    Получить данные из xlsx.

    Ежедневная загрузка данных о продажах.

    Только для админа.
    """
    return {'message': '... loading data ...'}
