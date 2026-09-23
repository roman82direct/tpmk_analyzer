import logging
from typing import Any

from pydantic import ValidationError

from backend.app.services.etl.dto.inventory import InventoryRowDTO

logger = logging.getLogger(__name__)


class InventoryTransformer:
    '''Преобразование нормализованных строк Excel в DTO.'''

    def transform(self, row: dict[str, Any]) -> InventoryRowDTO:
        return InventoryRowDTO.model_validate(row)

    def transform_many(
        self,
        rows: list[dict[str, Any]]
    ) -> list[InventoryRowDTO]:
        result: list[InventoryRowDTO] = []

        for row_number, row in enumerate(rows, start=4):
            try:
                dto = self.transform(row)
            except ValidationError as error:
                logger.error('Ошибка валидации строки %s Excel: %s', row_number, error)

            result.append(dto)

        logger.info(
            'Данные из Excel провалидированы и преобразованы в DTO: rows=%d', len(result)
        )
        return result
