from datetime import date
from decimal import Decimal

from sqlalchemy import BigInteger, Date, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base

# Для объёмов (11M строк/год) добавь в миграциях составной индекс:
# (snapshot_date, product_id)


class InventoryDailySnapshot(Base):
    """
    Таблица BI-показателей.

    Получает данные при ежедневной загрузке показателей из xlsx.
    """

    __tablename__ = 'fact_inventory_daily_snapshot'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    snapshot_date: Mapped[date] = mapped_column(Date, index=True)
    load_batch_id: Mapped[int] = mapped_column(ForeignKey('load_batch.id'),
                                               index=True)
    # dimensions
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'),
                                            index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'),
                                            index=True)
    assortment_id: Mapped[int] = mapped_column(ForeignKey('assortment.id'),
                                               index=True)
    assortment_gm_id: Mapped[int] = mapped_column(
        ForeignKey('assortment_gm.id'), index=True
    )
    group1_id: Mapped[int] = mapped_column(ForeignKey('group1.id'), index=True)
    group2_id: Mapped[int] = mapped_column(ForeignKey('group2.id'), index=True)
    group3_id: Mapped[int] = mapped_column(ForeignKey('group3.id'), index=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'), index=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey('user.id'), index=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'), index=True)
    # количественные показатели
    kz_rc: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=0.0,
                                           index=True)                     # КЗ остатка РЦ
    total_kz: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=0.0)  # КЗ остатка
    total_kz_plus_path: Mapped[Decimal] = mapped_column(Numeric(6, 2),
                                                        default=0.0)       # КЗ + путь
    current_stock: Mapped[int] = mapped_column(Integer, default=0)         # Остаток (шт)
    wh_stock: Mapped[int] = mapped_column(Integer, default=0)              # Скл. кол. Остаток ОПТа
    stock_sp: Mapped[int] = mapped_column(Integer, default=0)              # В т.ч. Остаток склады СП (шт)
    stock_so: Mapped[int] = mapped_column(Integer, default=0)              # В т.ч. Остаток склады СО (шт)
    in_transit: Mapped[int] = mapped_column(Integer, default=0)            # В пути, кол.
    in_purchase: Mapped[int] = mapped_column(Integer, default=0)           # В закупе, кол.
    reserve_client: Mapped[int] = mapped_column(Integer, default=0)        # Рез. (Кл), шт.
    reserve_transfer: Mapped[int] = mapped_column(Integer, default=0)      # Остатки трансфер, кол.
    reserve_other: Mapped[int] = mapped_column(Integer, default=0)         # Рез. проч., шт.
    # продажи и оборот
    sold_qty: Mapped[int] = mapped_column(Integer, default=0)              # Прод. кол.
    turnover_ss: Mapped[int] = mapped_column(Integer, default=0)           # ТО СС, руб.
    turnover: Mapped[int] = mapped_column(Integer, default=0)              # ТО, руб.

    # cost_price_rub        -- Себ., руб.
    # opt_price10_rub       -- Оптовая Цена10, руб.
    # sp_opt_price          -- СП Опт Цена10, руб.
    # so_opt_price          -- СО Цена10, руб.
