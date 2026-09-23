import logging

from fastapi import APIRouter, HTTPException, UploadFile, status

from backend.app.core.db import PGSession
from backend.app.services.etl.pipeline import ETLPipeline
from backend.app.services.etl.extractors.xlsx import XlsxExtractor
from backend.app.services.etl.loaders.postgres import PGLoader
from backend.app.services.etl.transformers.inventory import InventoryTransformer

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post('')
async def upload_file(file: UploadFile, session: PGSession) -> dict:
    """
    Получить данные из xlsx.

    Ежедневная загрузка данных о продажах.

    Только для админа.
    """
    logger.info('Получен файл: %s, size=%s', file.filename, file.size)

    content = await file.read()
    pipeline = ETLPipeline(XlsxExtractor(content),
                           InventoryTransformer(),
                           PGLoader(session))

    try:
        data = await pipeline.run()
    except Exception as error:
        logger.exception('Ошибка при обработке: %s', error)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'Ошибка извлечения данных: {error}',
        )

    return {'status': 'ok', 'rows': data[12]}
