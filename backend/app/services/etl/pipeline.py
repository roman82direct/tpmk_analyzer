import logging

from backend.app.config.logging_config import logging_setup
from backend.app.config.settings import backend_settings
from backend.app.services.etl.extractors.base import BaseExtractor
from backend.app.services.etl.extractors.xlsx import XlsxExtractor
from backend.app.services.etl.transformers.inventory import InventoryTransformer

logger = logging.getLogger(__name__)


class ETLPipeline:
    """Класс сценария загрузки, обработки, сохранения в БД данных."""

    def __init__(
            self,
            extractor: BaseExtractor,
            transformer: InventoryTransformer,
            loader=None
    ) -> None:
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self):
        logger.info('ETL pipeline запущен')
        rows = self.extractor.extract()
        dto_rows = self.transformer.transform_many(rows)
        logger.info('ETL pipeline завершён')
        return rows, dto_rows


def main():
    logging_setup()

    file_path = backend_settings.storage_input_dir / 'tpmk_new_01.01.2001.xlsx'

    pipeline = ETLPipeline(XlsxExtractor(file_path),
                           InventoryTransformer())

    try:
        data = pipeline.run()
    except Exception:
        logger.exception('Ошибка при обработке excel-файла: %s', file_path)
        return

    print(data[0][5])
    for key, value in data[0][5].items():
        print(f'excel_row: {key} -> {value}')

    print(data[1][5])


if __name__ == '__main__':
    main()

#  python -m backend.app.services.etl.pipeline
