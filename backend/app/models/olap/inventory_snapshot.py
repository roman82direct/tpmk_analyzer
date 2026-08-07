from datetime import date
from decimal import Decimal

from sqlalchemy import (Date, ForeignKey, Index, Integer, Numeric,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base


class InventoryDailySnapshot(Base):
    """
    Таблица BI-показателей.

    Получает данные при ежедневной загрузке показателей из xlsx.
    """

    __tablename__ = 'fact_inventory_daily_snapshot'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    snapshot_date: Mapped[date] = mapped_column(Date, index=True)
    load_batch_id: Mapped[int] = mapped_column(ForeignKey('load_batch.id'),
                                               index=True)
    # dimensions
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'),
                                            index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'),
                                            nullable=True, index=True)
    assortment_id: Mapped[int] = mapped_column(ForeignKey('assortment.id'),
                                               index=True)
    assortment_gm_id: Mapped[int] = mapped_column(
        ForeignKey('assortment_gm.id'), index=True
    )
    group1_id: Mapped[int] = mapped_column(ForeignKey('group.id'), index=True)
    group2_id: Mapped[int] = mapped_column(ForeignKey('group.id'), index=True)
    group3_id: Mapped[int] = mapped_column(ForeignKey('group.id'), index=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'),
                                          nullable=True, index=True)
    # buyer_id: Mapped[int] = mapped_column(ForeignKey('user.id'), index=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'),
                                          nullable=True, index=True)
    # количественные показатели
    kz_rc: Mapped[Decimal] = mapped_column(Numeric(10, 2),
                                           default=Decimal('0.00'),
                                           index=True)                     # КЗ остатка РЦ
    total_kz: Mapped[Decimal] = mapped_column(Numeric(10, 2),
                                              default=Decimal('0.00'))     # КЗ остатка
    total_kz_plus_path: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=Decimal('0.00')
    )                                                                      # КЗ + путь
    current_stock: Mapped[int] = mapped_column(Integer, default=0)         # Скл. кол.
    current_stock_rub: Mapped[int] = mapped_column(Integer, default=0)     # Склад сумма, руб.
    opt_stock: Mapped[int] = mapped_column(Integer, default=0)             # Остаток (шт) Остаток ОПТа
    opt_stock_rub: Mapped[int] = mapped_column(Integer, default=0)         # Остаток (руб.)
    opt_stock_sp: Mapped[int] = mapped_column(Integer, default=0)          # В т.ч. Остаток склады СП (шт)
    opt_stock_so: Mapped[int] = mapped_column(Integer, default=0)          # В т.ч. Остаток склады СО (шт)
    in_transit: Mapped[int] = mapped_column(Integer, default=0)            # В пути, кол.
    in_purchase: Mapped[int] = mapped_column(Integer, default=0)           # В закупе, кол.
    reserve_client: Mapped[int] = mapped_column(Integer, default=0)        # Рез. (Кл), шт.
    reserve_transfer: Mapped[int] = mapped_column(Integer, default=0)      # Остатки трансфер, кол.
    reserve_other: Mapped[int] = mapped_column(Integer, default=0)         # Рез. проч., шт.
    # продажи и оборот
    sold_qty: Mapped[int] = mapped_column(Integer, default=0)              # Прод. кол.
    turnover_ss: Mapped[int] = mapped_column(Integer, default=0)           # ТО СС, руб.
    turnover: Mapped[int] = mapped_column(Integer, default=0)              # ТО, руб.
    # продажи и оборот ОПТ
    opt_sold_qty: Mapped[int] = mapped_column(Integer, default=0)          # Продано (шт)
    opt_turnover_ss: Mapped[int] = mapped_column(Integer, default=0)       # ТО СС, руб..1
    opt_turnover: Mapped[int] = mapped_column(Integer, default=0)          # ТО, руб..1
    # продажи и оборот КрМПР
    krmpr_sold_qty: Mapped[int] = mapped_column(Integer, default=0)        # Продано (шт).1
    krmpr_turnover_ss: Mapped[int] = mapped_column(Integer, default=0)     # ТО СС, руб..2
    krmpr_turnover: Mapped[int] = mapped_column(Integer, default=0)        # ТО, руб..2
    # продажи и оборот ФР
    fr_sold_qty: Mapped[int] = mapped_column(Integer, default=0)           # Продано (шт).2
    fr_turnover_ss: Mapped[int] = mapped_column(Integer, default=0)        # ТО СС, руб..3
    fr_turnover: Mapped[int] = mapped_column(Integer, default=0)           # ТО, руб..3
    # продажи и оборот ГМ
    gm_sold_qty: Mapped[int] = mapped_column(Integer, default=0)           # Продано (шт).3
    gm_turnover_ss: Mapped[int] = mapped_column(Integer, default=0)        # ТО СС, руб..4
    gm_turnover: Mapped[int] = mapped_column(Integer, default=0)           # ТО, руб..4

    __table_args__ = (
        UniqueConstraint(
                'snapshot_date', 'product_id',
                name='uq_inventory_snapshot_business_key',
            ),
        # Индекс для запросов 'дай мне snapshot на дату по группе и статусу'
        Index('idx_inventory_snapshot_date_group_assortment',
              'snapshot_date', 'group1_id', 'assortment_id'),
    )
