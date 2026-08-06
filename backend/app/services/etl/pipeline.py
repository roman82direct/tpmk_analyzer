import logging
from collections.abc import Hashable
from typing import Any

from backend.app.config.logging_config import logging_setup
from backend.app.config.settings import backend_settings
from backend.app.services.etl.extractors.base import BaseExtractor
from backend.app.services.etl.extractors.xlsx import XlsxExtractor

logger = logging.getLogger(__name__)


class ETLPipeline:
    """Класс сценария загрузки, обработки, сохранения в БД данных."""

    def __init__(
            self,
            extractor: BaseExtractor[list[dict[Hashable, Any]]],
            transformer=None,
            loader=None
    ) -> None:
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self):
        logger.info('ETL pipeline запущен')
        rows = self.extractor.extract()
        logger.info('ETL pipeline завершён')
        return rows


def main():
    logging_setup()

    file_path = backend_settings.storage_input_dir / 'tpmk_new_01.01.2001.xlsx'

    pipeline = ETLPipeline(XlsxExtractor(file_path))

    try:
        data = pipeline.run()
    except Exception:
        logger.exception('Ошибка при обработке excel-файла: %s', file_path)
        return

    for item in data[:3]:
        print('-' * 30)
        print(item)


if __name__ == '__main__':
    main()




#  python -m backend.app.services.etl.pipeline
