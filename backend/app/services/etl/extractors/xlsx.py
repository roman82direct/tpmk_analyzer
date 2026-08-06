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

    REQUIRED_COLUMNS = ('Код', 'Товар', 'Стр.', 'Дата вв.', 'Дата сл.п.',
                        'Рез. (Кл), шт.', 'Рез. проч., шт.',
                        'Остатки трансфер, кол.', 'Скл. кол.',
                        'Склад сумма, руб.', 'В т.ч. ост. товаров на комиссии, шт.',
                        'В\nпути,\nкол.', 'В закупе, кол.',
                        'Просроченные (В закупе), кол.',
                        'Подпис закуп, кол.', 'Проблемные, кол',
                        'Себ., руб.', 'Прод. кол.', 'ТО СС, руб.', 'ТО, руб.',
                        'Дата п.п.', 'Кол. в кор.', 'Себ. куба',
                        'Мин. партия ОПТ', 'Мин. партия ГМ',
                        'КЗ остатка', 'КЗ остатка РЦ', 'КЗ+ путь',
                        'КЗ + закуп', 'Закупщик', 'Магазин / Лавка',
                        'Ассортимент', 'Ассортимент ГМ',
                        'Дата окончания продаж ГМ', 'Кат. КУБ',
                        'Дата окончания продаж ОПТ',
                        'Бренд', 'Группа 1', 'Группа 2', 'Группа 3',
                        # опт
                        'Остаток (шт)', 'Остаток (руб.)',
                        '"В т.ч.  Остаток  склады СП (шт)"',
                        '"В т.ч.  Остаток  склады СО (шт)"',
                        'Продано (шт)', 'ТО СС, руб..1', 'ТО, руб..1',
                        'Оптовая Цена10, руб.', 'СП Опт\nЦена10, руб.',
                        'Старые остатки Цена10, руб.',
                        # КрМПР
                        'Продано (шт).1', 'ТО СС, руб..2',
                        'ТО, руб..2', 'КрМПР Цена10, руб.',
                        # ФР
                        'Продано (шт).2', 'ТО СС, руб..3',
                        'ТО, руб..3', 'ВП, руб..3',
                        'Партнерская Цена10',
                        # ГМ
                        'Продано (шт).3', 'ТО СС, руб..4', 'ТО, руб..4',
                        'Продажа Цена ГМ, руб.')

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def extract(self) -> list[dict[Hashable, Any]]:
        started_at = perf_counter()
        try:
            df = pd.read_excel(
                self.file_path,
                usecols=self.REQUIRED_COLUMNS,
                header=2
            )
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

        records = df.to_dict(orient='records')
        elapsed = perf_counter() - started_at

        logger.info(
            'Данные из Excel извлечены: file=%s, rows=%d,'
            ' columns=%d, elapsed=%.3fs',
            self.file_path, len(df), len(df.columns), elapsed,
        )

        return records
