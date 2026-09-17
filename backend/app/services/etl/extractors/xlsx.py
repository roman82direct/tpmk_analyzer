import logging
from collections.abc import Hashable
from time import perf_counter
from typing import Any

import fastexcel
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

        # ДУБЛЯЖИ - описать обработку
        'ТО СС, руб.', 'ТО, руб.',
        # КрМПР
        'Продано (шт)', 'ТО СС, руб.', 'ТО, руб.',
        # ФР
        'Продано (шт)', 'ТО СС, руб.', 'ТО, руб.',
        # ГМ
        'Продано (шт)', 'ТО СС, руб.', 'ТО, руб.',
    )

    def __init__(self, file_content: bytes):
        self.file_content = file_content

    def _read_dataframe(self) -> pd.DataFrame:
        """Чтение данных из эксель."""
        reader = fastexcel.read_excel(self.file_content)
        sheet = reader.load_sheet(0, header_row=self.HEADER_ROW,)
        df = sheet.to_pandas()
        df = df[list(self.REQUIRED_COLUMNS)]
        return df

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
