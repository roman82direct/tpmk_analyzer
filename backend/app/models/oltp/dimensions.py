from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date, ForeignKey, Integer, Numeric, SmallInteger, String

from backend.app.models.base import Base, CommonMixin


class Product(CommonMixin, Base):
    """Таблица товаров."""

    articul: Mapped[str] = mapped_column(String, index=True, unique=True)
    quantity_in_box: Mapped[int] = mapped_column(Integer, nullable=True,
                                                 default=0)                  # Кол. в кор.
    min_opt_batch: Mapped[int] = mapped_column(Integer,
                                               nullable=True, default=0)     # Мин. партия ОПТ
    min_gm_batch: Mapped[int] = mapped_column(Integer,
                                              nullable=True, default=0)      # Мин. партия ГМ
    cost_price: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=True,
                                                default=Decimal('0.00'))     # Себ., руб.
    opt_price10: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=True,
                                                 default=Decimal('0.00'))    # Оптовая Цена10, руб.
    sp_opt_price: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=True,
                                                  default=Decimal('0.00'))   # СП Опт Цена10, руб.
    so_opt_price: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=True,
                                                  default=Decimal('0.00'))   # СО Цена10, руб.
    krmpr_price: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=True,
                                                 default=Decimal('0.00'))    # КрМПР Цена10, руб.'
    fr_price: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=True,
                                              default=Decimal('0.00'))       # Партнерская Цена10
    gm_price: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=True,
                                              default=Decimal('0.00'))       # Продажа Цена ГМ, руб.
    arrival_date: Mapped[date] = mapped_column(Date, nullable=True)          # Дата вв.
    next_delivery_date: Mapped[date] = mapped_column(Date, nullable=True)    # Дата сл.п.
    opt_end_date: Mapped[date] = mapped_column(Date, nullable=True,)         # Дата окончания продаж ОПТ
    gm_end_date: Mapped[date] = mapped_column(Date, nullable=True,)          # Дата окончания продаж ГМ


class Group(CommonMixin, Base):
    """Таблица групп товаров."""

    parent_id: Mapped[int | None] = mapped_column(ForeignKey('group.id'))
    level: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class Assortment(CommonMixin, Base):
    """Таблица ассортиментов ОПТа."""


class AssortmentGM(CommonMixin, Base):
    """Таблица ассортиментов ГМ."""

    __tablename__ = 'assortment_gm'


class Brand(CommonMixin, Base):
    """Таблица брендов."""


class Country(CommonMixin, Base):
    """Таблица стран."""


class Store(CommonMixin, Base):
    """Таблица лавок."""
