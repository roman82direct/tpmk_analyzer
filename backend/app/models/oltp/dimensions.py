from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, SmallInteger

from backend.app.models.base import Base, CommonFieldsMixin, CommonMixin


class Product(CommonMixin, Base):
    """Таблица товаров."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    autoincrement=True)
    articul: Mapped[str] = mapped_column(String, nullable=False,
                                         index=True, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    quantity_in_box: Mapped[int] = mapped_column(Integer, default=0)         # Кол. в кор.
    min_opt_batch: Mapped[int] = mapped_column(Integer, default=0)           # Мин. партия ОПТ
    min_gm_batch: Mapped[int] = mapped_column(Integer, default=0)            # Мин. партия ГМ
    cost_price: Mapped[Decimal] = mapped_column(Numeric(8, 2),
                                                default=Decimal('0.00'))     # Себ., руб.
    opt_price10: Mapped[Decimal] = mapped_column(Numeric(8, 2),
                                                 default=Decimal('0.00'))    # Оптовая Цена10, руб.
    sp_opt_price: Mapped[Decimal] = mapped_column(Numeric(8, 2),
                                                  default=Decimal('0.00'))   # СП Опт Цена10, руб.
    so_opt_price: Mapped[Decimal] = mapped_column(Numeric(8, 2),
                                                  default=Decimal('0.00'))   # СО Цена10, руб.
    arrival_date: Mapped[date] = mapped_column(Date)                         # Дата вв.
    next_delivery_date: Mapped[date] = mapped_column(Date)                   # Дата сл.п. / Дата п.п.
    opt_end_date: Mapped[date] = mapped_column(Date)                         # Дата окончания продаж ОПТ
    gm_end_date: Mapped[date] = mapped_column(Date)                          # Дата окончания продаж ГМ


class Group(CommonMixin, Base):
    """Таблица групп товаров."""

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('group.id'))
    level: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class Assortment(CommonFieldsMixin, Base):
    """Таблица ассортиментов ОПТа."""


class AssortmentGM(CommonFieldsMixin, Base):
    """Таблица ассортиментов ГМ."""

    __tablename__ = 'assortment_gm'


class Country(CommonFieldsMixin, Base):
    """Таблица стран."""


class Store(CommonFieldsMixin, Base):
    """Таблица лавок."""
