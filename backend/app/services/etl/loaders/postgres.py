import logging
from datetime import date
from time import perf_counter
from typing import Any, TypeVar

from sqlalchemy.dialects.postgresql import insert

from backend.app.core.db import PGSession
from backend.app.models import (
    Assortment, AssortmentGM, Brand, Country, Group,
    InventoryDailySnapshot, Product, Store
)
from backend.app.services.etl.dto.inventory import InventoryRowDTO

logger = logging.getLogger(__name__)

DimensionModel = TypeVar('DimensionModel', Brand, Assortment, AssortmentGM, Country, Store,)


class PGLoader:
    """Сохраняет валидированные данные DTO в БД Postgres."""

    def __init__(self, session: PGSession) -> None:
        self.session = session

    @staticmethod
    def _clean_name(value: str | None) -> str | None:
        if value is None:
            return None

        value = ' '.join(value.split())
        return value or None

    async def _get_or_create_named_dimension(
        self,
        model: type[DimensionModel],
        raw_name: str | None,
    ) -> int | None:
        name = self._clean_name(raw_name)

        if name is None:
            return None

        stmt = (
            insert(model)
            .values(name=name)
            .on_conflict_do_update(
                index_elements=[model.name],
                set_={'name': name},
            )
            .returning(model.id)
        )

        return await self.session.scalar(stmt)

    async def _get_or_create_group(
        self,
        raw_name: str | None,
        parent_id: int | None,
        level: int,
    ) -> int | None:
        name = self._clean_name(raw_name)

        if name is None:
            return None

        stmt = (
            insert(Group)
            .values(
                name=name,
                parent_id=parent_id,
                level=level,
            )
            .on_conflict_do_update(
                index_elements=[Group.name],
                set_={'level': level},
            )
            .returning(Group.id)
        )

        return await self.session.scalar(stmt)

    async def _resolve_group_id(self, row: InventoryRowDTO) -> int | None:
        group1_id = await self._get_or_create_group(
            raw_name=row.group1_name,
            parent_id=None,
            level=1,
        )

        group2_id = None
        if group1_id is not None:
            group2_id = await self._get_or_create_group(
                raw_name=row.group2_name,
                parent_id=group1_id,
                level=2,
            )

        group3_id = None
        if group2_id is not None:
            group3_id = await self._get_or_create_group(
                raw_name=row.group3_name,
                parent_id=group2_id,
                level=3,
            )

        return group3_id or group2_id or group1_id

    async def _upsert_product(self, row: InventoryRowDTO) -> int:
        if row.articul is None:
            raise ValueError('Нельзя загрузить товар без артикула.')

        values: dict[str, Any] = {
            'articul': row.articul.strip(),
            'name': self._clean_name(row.product_name),
            'quantity_in_box': row.quantity_in_box,
            'min_opt_batch': row.min_opt_batch,
            'min_gm_batch': row.min_gm_batch,
            'cost_price': row.cost_price,
            'opt_price10': row.opt_price10,
            'sp_opt_price': row.sp_opt_price,
            'so_opt_price': row.so_opt_price,
            'krmpr_price': row.krmpr_price,
            'fr_price': row.fr_price,
            'gm_price': row.gm_price,
            'arrival_date': row.arrival_date,
            'next_delivery_date': row.next_delivery_date,
            'opt_end_date': row.opt_end_date,
            'gm_end_date': row.gm_end_date,
        }

        stmt = insert(Product).values(**values)

        update_values = {
            key: value
            for key, value in values.items()
            if key != 'articul' and value is not None
        }

        stmt = (
            stmt.on_conflict_do_update(
                index_elements=[Product.articul],
                set_=update_values,
            )
            .returning(Product.id)
        )

        product_id = await self.session.scalar(stmt)

        if product_id is None:
            raise RuntimeError(
                f'Не удалось получить id товара с артикулом {row.articul!r}.'
            )

        return product_id

    async def _upsert_snapshot(
        self,
        row: InventoryRowDTO,
        product_id: int,
        store_id: int | None,
        snapshot_date: date | None = None,
    ) -> None:
        if snapshot_date is None:
            snapshot_date = date.today()

        values = {
            'snapshot_date': snapshot_date,
            'product_id': product_id,
            'store_id': store_id,
            'kz_rc': row.kz_rc,
            'total_kz': row.total_kz,
            'total_kz_plus_path': row.total_kz_plus_path,
            'current_stock': row.current_stock,
            'current_stock_rub': row.current_stock_rub,
            'in_transit': row.in_transit,
            'in_purchase': row.in_purchase,
            'reserve_client': row.reserve_client,
            'reserve_other': row.reserve_other,
            'reserve_transfer': row.reserve_transfer,
            'sold_qty': row.sold_qty,
            'turnover_ss': row.turnover_ss,
            'turnover': row.turnover,
            'opt_stock': row.opt_stock,
            'opt_stock_rub': row.opt_stock_rub,
            'opt_stock_sp': row.opt_stock_sp,
            'opt_stock_so': row.opt_stock_so,
            'opt_sold_qty': row.opt_sold_qty,
            'opt_turnover_ss': row.opt_turnover_ss,
            'opt_turnover': row.opt_turnover,
            'krmpr_sold_qty': row.krmpr_sold_qty,
            'krmpr_turnover_ss': row.krmpr_turnover_ss,
            'krmpr_turnover': row.krmpr_turnover,
            'fr_sold_qty': row.fr_sold_qty,
            'fr_turnover_ss': row.fr_turnover_ss,
            'fr_turnover': row.fr_turnover,
            'gm_sold_qty': row.gm_sold_qty,
            'gm_turnover_ss': row.gm_turnover_ss,
            'gm_turnover': row.gm_turnover,
        }

        stmt = insert(InventoryDailySnapshot).values(**values)

        await self.session.execute(
            stmt.on_conflict_do_update(
                constraint='uq_inventory_snapshot_business_key',
                set_={
                    key: value
                    for key, value in values.items()
                    if key not in {'snapshot_date', 'product_id', 'store_id'}
                },
            )
        )

    async def load(
        self,
        dto_rows: list[InventoryRowDTO],
    ) -> None:
        started_at = perf_counter()
        counter = 0

        async with self.session.begin():
            for row in dto_rows:
                if row.articul is None:
                    continue

                group_id = await self._resolve_group_id(row)

                brand_id = await self._get_or_create_named_dimension(
                    Brand, row.brand_name,
                )
                assortment_id = await self._get_or_create_named_dimension(
                    Assortment, row.assortment_name,
                )
                assortment_gm_id = await self._get_or_create_named_dimension(
                    AssortmentGM, row.assortment_gm_name,
                )
                country_id = await self._get_or_create_named_dimension(
                    Country, row.country_name,
                )
                store_id = await self._get_or_create_named_dimension(
                    Store, row.store_name,
                )

                # # Нужна модель User со столбцами id/name.
                # buyer_id = await self._get_or_create_named_dimension(
                #     User,
                #     row.buyer_name,
                # )

                product_id = await self._upsert_product(
                    row=row,
                    # group_id=group_id,
                    # brand_id=brand_id,
                    # assortment_id=assortment_id,
                    # assortment_gm_id=assortment_gm_id,
                    # country_id=country_id,
                    # store_id=store_id,
                    # buyer_id=buyer_id,
                )

                await self._upsert_snapshot(
                    row=row,
                    product_id=product_id,
                    store_id=store_id
                )
                counter += 1
        elapsed = perf_counter() - started_at
        logger.info(
            'Данные из объекта DTO сохранены в БД: записей=%d, elapsed=%.3fs', counter, elapsed
        )
