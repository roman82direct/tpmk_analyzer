from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer

from backend.app.models.base import Base, CommonMixin


class Product(CommonMixin, Base):
    """Таблица товаров."""

# articul
# name
# quantity_in_box       # Кол. в кор.
# min_opt_batch         # Мин. партия ОПТ

# cost_price_rub        # Себ., руб.
# opt_price10_rub       # Оптовая Цена10, руб.
# sp_opt_price          # СП Опт Цена10, руб.
# so_opt_price          # СО Цена10, руб.

# arrival_date          # Дата вв.
# next_delivery_date    # Дата сл.п. / Дата п.п.

# opt_end_date          # Дата окончания продаж ОПТ
# gm_end_date           # Дата окончания продаж ГМ
# FKeys to other dimensions

# min_gm_batch          # Мин. партия ГМ
