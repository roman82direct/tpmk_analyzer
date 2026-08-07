import logging
from collections.abc import Hashable
from pathlib import Path
from time import perf_counter
from typing import Any

import pandas as pd

from .base import BaseExtractor

logger = logging.getLogger(__name__)


class XlsxExtractor(BaseExtractor[list[dict[Hashable, Any]]]):
    """Получение данных из xlsx."""

    REQUIRED_COLUMNS: tuple[str, ...] = (
        'Код', 'Товар', 'Кол. в кор.', 'Мин. партия ОПТ', 'Мин. партия ГМ',
        'Группа 1', 'Группа 2', 'Группа 3', 'Бренд',
        'Ассортимент', 'Ассортимент ГМ',
        'Стр.', 'Дата вв.', 'Дата сл.п.',
        'Дата окончания продаж ОПТ', 'Дата окончания продаж ГМ',
        'Кат. КУБ', 'Себ., руб.', 'Оптовая Цена10, руб.',
        'СП Опт\nЦена10, руб.', 'Старые остатки Цена10, руб.',
        'КрМПР Цена10, руб.', 'Партнерская Цена10', 'Продажа Цена ГМ, руб.',
        'КЗ остатка', 'КЗ остатка РЦ', 'КЗ+ путь', 'КЗ + закуп',
        'Скл. кол.', 'Склад сумма, руб.', 'Рез. (Кл), шт.', 'Рез. проч., шт.',
        'Остатки трансфер, кол.', 'В т.ч. ост. товаров на комиссии, шт.',
        'В\nпути,\nкол.', 'В закупе, кол.', 'Просроченные (В закупе), кол.',
        'Подпис закуп, кол.', 'Проблемные, кол',
        'Прод. кол.', 'ТО СС, руб.', 'ТО, руб.',
        'Дата п.п.', 'Закупщик', 'Магазин / Лавка',
        # опт
        'Остаток (шт)', 'Остаток (руб.)', '"В т.ч.  Остаток  склады СП (шт)"',
        '"В т.ч.  Остаток  склады СО (шт)"', 'Продано (шт)',
        'ТО СС, руб..1', 'ТО, руб..1',
        # КрМПР
        'Продано (шт).1', 'ТО СС, руб..2', 'ТО, руб..2',
        # ФР
        'Продано (шт).2', 'ТО СС, руб..3', 'ТО, руб..3', 'ВП, руб..3',
        # ГМ
        'Продано (шт).3', 'ТО СС, руб..4', 'ТО, руб..4',
    )

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def _read_dataframe(self) -> pd.DataFrame:
        return pd.read_excel(
            self.file_path,
            usecols=self.REQUIRED_COLUMNS,
            header=2
        )

    def extract(self) -> list[dict[Hashable, Any]]:
        started_at = perf_counter()

        try:
            df = self._read_dataframe()
        except FileNotFoundError:
            logger.error('Excel-файл %s не найден', self.file_path)
            raise
        except PermissionError:
            logger.error('Нет доступа к Excel-файлу: %s', self.file_path)
            raise
        except ValueError:
            logger.error('Некорректная структура Excel-файла: %s',
                         self.file_path)
            raise
        except Exception:
            logger.error('Ошибка при чтении Excel-файла: %s',
                         self.file_path)
            raise

        df = df[list(self.REQUIRED_COLUMNS)]
        records = df.to_dict(orient='records')

        elapsed = perf_counter() - started_at
        logger.info(
            'Данные из Excel извлечены: file=%s, rows=%d,'
            ' columns=%d, elapsed=%.3fs',
            self.file_path, len(df), len(df.columns), elapsed,
        )
        return records
