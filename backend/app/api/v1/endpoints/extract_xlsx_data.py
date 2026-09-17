import logging

from fastapi import APIRouter, HTTPException, UploadFile, status

from backend.app.services.etl.pipeline import ETLPipeline
from backend.app.services.etl.extractors.xlsx import XlsxExtractor
from backend.app.services.etl.transformers.inventory import InventoryTransformer

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post('')
async def upload_file(file: UploadFile) -> dict:
    """
    Получить данные из xlsx.

    Ежедневная загрузка данных о продажах.

    Только для админа.
    """
    logger.info('Получен файл: %s, size=%s', file.filename, file.size)

    content = await file.read()
    pipeline = ETLPipeline(XlsxExtractor(content), InventoryTransformer())

    try:
        data = pipeline.run()
    except Exception as exc:
        logger.exception('Ошибка при обработке: %s', exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'Ошибка извлечения данных: {exc}',
        )

    return {'status': 'ok', 'rows': data[12]}
