from io import BytesIO
import logging
from collections.abc import Hashable
from time import perf_counter
from typing import Any

import pandas as pd

from .base import BaseExtractor

logger = logging.getLogger(__name__)


class XlsxExtractor(BaseExtractor[list[dict[Hashable, Any]]]):
    """Получение данных из xlsx."""

    HEADER_ROW = 2

    REQUIRED_COLUMNS: tuple[str, ...] = (
        'Код', 'Товар', 'Кол. в кор.', 'Мин. партия ОПТ', 'Мин. партия ГМ',
        'Группа 1', 'Группа 2', 'Группа 3', 'Бренд',
        'Ассортимент', 'Ассортимент ГМ',
        'Стр.', 'Дата вв.', 'Дата сл.п.',
        'Дата окончания продаж ОПТ', 'Дата окончания продаж ГМ',
        # 'Кат. КУБ',
        'Себ., руб.', 'Оптовая Цена10, руб.',
        'СП Опт\nЦена10, руб.', 'Старые остатки Цена10, руб.',
        'КрМПР Цена10, руб.', 'Партнерская Цена10', 'Продажа Цена ГМ, руб.',
        'КЗ остатка', 'КЗ остатка РЦ', 'КЗ+ путь',
        # 'КЗ + закуп',
        'Скл. кол.', 'Склад сумма, руб.', 'Рез. (Кл), шт.', 'Рез. проч., шт.',
        'Остатки трансфер, кол.',
        # 'В т.ч. ост. товаров на комиссии, шт.',
        'В\nпути,\nкол.', 'В закупе, кол.',
        # 'Подпис закуп, кол.', 'Проблемные, кол',
        'Прод. кол.', 'ТО СС, руб.', 'ТО, руб.',
        # 'Дата п.п.',
        'Закупщик', 'Магазин / Лавка',
        # опт
        'Остаток (шт)', 'Остаток (руб.)', '"В т.ч.  Остаток  склады СП (шт)"',
        '"В т.ч.  Остаток  склады СО (шт)"', 'Продано (шт)',
        'ТО СС, руб..1', 'ТО, руб..1',
        # КрМПР
        'Продано (шт).1', 'ТО СС, руб..2', 'ТО, руб..2',
        # ФР
        'Продано (шт).2', 'ТО СС, руб..3', 'ТО, руб..3',
        # ГМ
        'Продано (шт).3', 'ТО СС, руб..4', 'ТО, руб..4',
    )

    def __init__(self, file_content: bytes | BytesIO):
        self.file_content = file_content

    def _read_dataframe(self) -> pd.DataFrame:
        """Чтение данных из эксель."""
        if isinstance(self.file_content, bytes):
            self.file_content = BytesIO(self.file_content)

        return pd.read_excel(
            self.file_content,
            usecols=self.REQUIRED_COLUMNS,
            header=self.HEADER_ROW
        )

    def extract(self) -> list[dict[Hashable, Any]]:
        """Получение и нормализация данных из эксель."""
        started_at = perf_counter()

        try:
            df = self._read_dataframe()
        except PermissionError as error:
            logger.error('Нет доступа к Excel-файлу: %s', error)
            raise error
        except ValueError as error:
            logger.error('Некорректная структура Excel-файла: %s', error)
            raise error
        except Exception as error:
            logger.error('Ошибка при чтении Excel-файла: %s', error)
            raise error

        # Исключаем последнюю строку
        df = df.iloc[:-1].reset_index(drop=True)

        df = df[list(self.REQUIRED_COLUMNS)]
        records = df.to_dict(orient='records')

        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, pd.Timestamp):
                    record[key] = value.date()

        elapsed = perf_counter() - started_at
        logger.info(
            'Данные из Excel извлечены и нормализованы: rows=%d, columns=%d, elapsed=%.3fs',
            len(df), len(df.columns), elapsed,
        )
        return records
