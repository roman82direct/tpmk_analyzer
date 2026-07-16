import asyncio
import logging
import re
from datetime import datetime, date
from pathlib import Path


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

FILENAME_RE = re.compile(r'^tpmk_new_(?P<date>\d{2}\.\d{2}\.\d{4})\.xlsx$')

storage = Path('storage/input')


async def load_to_db(filepath: Path, snapshot_date: date):
    """Загружает данные из файла в таблицы Postgres."""
    logger.info('load_to_db is working')


async def batch_exists(filename: str, snapshot_date: date) -> bool:
    """Проверяет грузился ли файл в БД или нет."""
    logger.info('batch_exists is working')
    return False


async def register_batch(filename: str, snapshot_date: date) -> None:
    """Заполняет данные о загрузке в таблице load_batch."""
    logger.info('register_batch is working')


async def mark_batch_loaded(filename: str, snapshot_date: date) -> None:
    """Помечает batch как успешно загруженный в load_batch."""
    logger.info('mark_batch_loaded is working')


async def process_file(file: Path) -> None:
    """
    Обрабатывает эксель-файл.

    - Проверяет соответствие имени заданному шаблону.
    - Формирует значение даты для даты актуальности данных.
    - Проверяет грузился ли файл ранее.
    - Вносит запись в load_batch.
    - Загружает содержимое файла в БД.
    - Помечает load_batch как обработанный со статусом и доп. инфо.
    """
    valid_name = FILENAME_RE.match(file.name)
    if valid_name is None:
        logger.error('Filename error: %s', file)
        return

    snapshot_date = datetime.strptime(valid_name['date'], '%d.%m.%Y').date()

    if await batch_exists(file.name, snapshot_date):
        logger.info('Файл %s для даты %s уже загружен, пропускаем',
                    file.name, snapshot_date)
        return

    await register_batch(file.name, snapshot_date)

    try:
        await load_to_db(file, snapshot_date)
    except Exception as error:
        logger.exception('Ошибка загрузки файла %s в БД: %s', file.name, error)
        return
    else:
        await mark_batch_loaded(file.name, snapshot_date)
        logger.info('Файл %s загружен для даты %s', file.name, snapshot_date)


async def upload_xlsx_to_db(storage: Path) -> None:
    """Загружает данные из эксель-файлов в БД."""
    files = [file for file in storage.iterdir() if file.is_file()]
    if not files:
        logger.warning('Файлы для загрузки отсутствуют в %s', storage)
        return

    for file in files:
        await process_file(file)


if __name__ == '__main__':
    asyncio.run(upload_xlsx_to_db(storage))
