from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InventoryRowDTO(BaseModel):
    '''
    Нормализованная и валидированная строка из Excel.

    - Pydantic-модель;
    - описание схемы входной строки;
    - контракт между Transformer и Loader.
    '''

    model_config = ConfigDict(validate_by_alias=True, extra='forbid',)

    # Товар
    articul: str | None = Field(validation_alias='Код', min_length=1)
    product_name: str | None = Field(validation_alias='Товар', min_length=1)
    quantity_in_box: int | None = Field(default=None,
                                        validation_alias='Кол. в кор.')
    min_opt_batch: int | None = Field(default=None,
                                      validation_alias='Мин. партия ОПТ')
    min_gm_batch: int | None = Field(default=None,
                                     validation_alias='Мин. партия ГМ')
    cost_price: Decimal | None = Field(default=None,
                                       validation_alias='Себ., руб.')
    opt_price10: Decimal | None = Field(
        default=None, validation_alias='Оптовая Цена10, руб.'
    )
    sp_opt_price: Decimal | None = Field(
        default=None, validation_alias='СП Опт\nЦена10, руб.'
    )
    so_opt_price: Decimal | None = Field(
        default=None, validation_alias='Старые остатки Цена10, руб.'
    )
    krmpr_price: Decimal | None = Field(
        default=None, validation_alias='КрМПР Цена10, руб.'
    )
    fr_price: Decimal | None = Field(default=None,
                                     validation_alias='Партнерская Цена10')
    gm_price: Decimal | None = Field(
        default=None, validation_alias='Продажа Цена ГМ, руб.'
    )
    arrival_date: date | None = Field(
        default=None, validation_alias='Дата вв.'
    )
    next_delivery_date: date | None = Field(
        default=None, validation_alias='Дата сл.п.'
    )
    opt_end_date: date | None = Field(
        default=None, validation_alias='Дата окончания продаж ОПТ'
    )
    gm_end_date: date | None = Field(
        default=None, validation_alias='Дата окончания продаж ГМ'
    )

    # Измерения
    group1_name: str | None = Field(default=None, validation_alias='Группа 1')
    group2_name: str | None = Field(default=None, validation_alias='Группа 2')
    group3_name: str | None = Field(default=None, validation_alias='Группа 3')
    brand_name: str | None = Field(default=None, validation_alias='Бренд')
    assortment_name: str | None = Field(default=None,
                                        validation_alias='Ассортимент')
    assortment_gm_name: str | None = Field(default=None,
                                           validation_alias='Ассортимент ГМ')
    country_name: str | None = Field(default=None, validation_alias='Стр.')
    store_name: str | None = Field(default=None,
                                   validation_alias='Магазин / Лавка')
    buyer_name: str | None = Field(default=None, validation_alias='Закупщик')

    # Общие показатели
    kz_rc: Decimal | None = Field(default=None,
                                  validation_alias='КЗ остатка РЦ')
    total_kz: Decimal | None = Field(default=None,
                                     validation_alias='КЗ остатка')
    total_kz_plus_path: Decimal | None = Field(default=None,
                                               validation_alias='КЗ+ путь')
    current_stock: int | None = Field(default=None,
                                      validation_alias='Скл. кол.')
    current_stock_rub: Decimal | None = Field(
        default=None, validation_alias='Склад сумма, руб.'
    )
    in_transit: int | None = Field(default=None,
                                   validation_alias='В\nпути,\nкол.')
    in_purchase: int | None = Field(default=None,
                                    validation_alias='В закупе, кол.')
    reserve_client: int | None = Field(default=None,
                                       validation_alias='Рез. (Кл), шт.')
    reserve_other: int | None = Field(default=None,
                                      validation_alias='Рез. проч., шт.')
    reserve_transfer: int | None = Field(
        default=None, validation_alias='Остатки трансфер, кол.'
    )
    sold_qty: int | None = Field(default=None, validation_alias='Прод. кол.')
    turnover_ss: Decimal | None = Field(default=None,
                                        validation_alias='ТО СС, руб.')
    turnover: Decimal | None = Field(default=None, validation_alias='ТО, руб.')

    # Оптовые показатели
    opt_stock: int | None = Field(default=None,
                                  validation_alias='Остаток (шт)')
    opt_stock_rub: Decimal | None = Field(default=None,
                                          validation_alias='Остаток (руб.)')
    opt_stock_sp: int | None = Field(
        default=None, validation_alias='"В т.ч.  Остаток  склады СП (шт)"'
    )
    opt_stock_so: int | None = Field(
        default=None, validation_alias='"В т.ч.  Остаток  склады СО (шт)"'
    )
    opt_sold_qty: int | None = Field(default=None,
                                     validation_alias='Продано (шт)')
    opt_turnover_ss: Decimal | None = Field(default=None,
                                            validation_alias='ТО СС, руб._1')
    opt_turnover: Decimal | None = Field(default=None,
                                         validation_alias='ТО, руб._1')

    # КрМПР
    krmpr_sold_qty: int | None = Field(default=None,
                                       validation_alias='Продано (шт)_1')
    krmpr_turnover_ss: Decimal | None = Field(default=None,
                                              validation_alias='ТО СС, руб._2')
    krmpr_turnover: Decimal | None = Field(default=None,
                                           validation_alias='ТО, руб._2')

    # ФР
    fr_sold_qty: int | None = Field(default=None,
                                    validation_alias='Продано (шт)_2')
    fr_turnover_ss: Decimal | None = Field(default=None,
                                           validation_alias='ТО СС, руб._3')
    fr_turnover: Decimal | None = Field(default=None,
                                        validation_alias='ТО, руб._3')

    # ГМ
    gm_sold_qty: int | None = Field(default=None,
                                    validation_alias='Продано (шт)_3')
    gm_turnover_ss: Decimal | None = Field(default=None,
                                           validation_alias='ТО СС, руб._4')
    gm_turnover: Decimal | None = Field(default=None,
                                        validation_alias='ТО, руб._4')
