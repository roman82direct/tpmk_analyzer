from typing import Any

from pydantic import ValidationError

from backend.app.services.etl.dto.inventory import InventoryRowDTO


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
            except ValidationError as exc:
                raise ValueError(
                    f'Ошибка валидации строки Excel: {row_number}'
                ) from exc

            result.append(dto)

        return result
