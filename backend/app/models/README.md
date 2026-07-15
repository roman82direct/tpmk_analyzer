## ER-диаграмма данных (Kimball)

```mermaid
    erDiagram
        PRODUCT {
            int id PK
            string name "Название товара (уникально)"
            string articul "Артикул (уникально)"
            int quantity_in_box "Кол-во в коробке"
            int min_opt_batch "Мин. партия ОПТ"
            int min_gm_batch "Мин. партия ГМ"
            numeric cost_price "Себестоимость, руб."
            numeric opt_price10 "Оптовая цена10, руб."
            numeric sp_opt_price "СП оптовая цена10, руб."
            numeric so_opt_price "СО цена10, руб."
            date arrival_date "Дата ввоза"
            date next_delivery_date "Дата следующего прихода"
            date opt_end_date "Дата окончания продаж ОПТ"
            date gm_end_date "Дата окончания продаж ГМ"
        }

        GROUP {
            int id PK
            string name "Название группы (уникально)"
            int parent_id FK "Родительская группа"
            smallint level "Уровень иерархии"
        }

        ASSORTMENT {
            int id PK
            string name "Ассортимент ОПТа (уникально)"
        }

        ASSORTMENT_GM {
            int id PK
            string name "Ассортимент ГМ (уникально)"
        }

        BRAND {
            int id PK
            string name "Бренд (уникально)"
        }

        COUNTRY {
            int id PK
            string name "Страна (уникально)"
        }

        STORE {
            int id PK
            string name "Лавка/магазин (уникально)"
        }

        LOAD_BATCH {
            int id PK
            datetime loaded_at "Момент загрузки"
            date snapshot_date "Дата snapshot'a"
            string source_file_name "Имя исходного файла"
            string source_file_hash "Хэш файла"
            string status "Статус загрузки"
            int rows_count "Кол-во строк"
            string error_message "Сообщение об ошибке"
        }

        INVENTORY_DAILY_SNAPSHOT {
            int id PK
            date snapshot_date "Дата snapshot'a"
            int load_batch_id FK "Загрузка"
            int product_id FK "Товар"
            int country_id FK "Страна"
            int assortment_id FK "Ассортимент ОПТа"
            int assortment_gm_id FK "Ассортимент ГМ"
            int group1_id FK "Группа 1"
            int group2_id FK "Группа 2"
            int group3_id FK "Группа 3"
            int brand_id FK "Бренд"
            int store_id FK "Лавка/магазин"
            numeric kz_rc "КЗ остатка РЦ"
            numeric total_kz "КЗ остатка"
            numeric total_kz_plus_path "КЗ + путь"
            int current_stock "Остаток (шт)"
            int wh_stock "Складской остаток ОПТа"
            int stock_sp "Остаток склады СП (шт)"
            int stock_so "Остаток склады СО (шт)"
            int in_transit "В пути, кол."
            int in_purchase "В закупе, кол."
            int reserve_client "Резерв клиента, шт."
            int reserve_transfer "Остатки трансфер, кол."
            int reserve_other "Резерв прочий, шт."
            int sold_qty "Продано, шт."
            int turnover_ss "ТО СС, руб."
            int turnover "ТО, руб."
        }

        %% Иерархия групп
        GROUP ||--o{ GROUP : "родитель -> дочерние группы"

        %% Факт и измерения
        LOAD_BATCH ||--o{ INVENTORY_DAILY_SNAPSHOT : "загрузка содержит snapshot-строки"
        PRODUCT ||--o{ INVENTORY_DAILY_SNAPSHOT : "товар в snapshot"
        COUNTRY ||--o{ INVENTORY_DAILY_SNAPSHOT : "страна в snapshot"
        ASSORTMENT ||--o{ INVENTORY_DAILY_SNAPSHOT : "ассортимент ОПТа в snapshot"
        ASSORTMENT_GM ||--o{ INVENTORY_DAILY_SNAPSHOT : "ассортимент ГМ в snapshot"
        BRAND ||--o{ INVENTORY_DAILY_SNAPSHOT : "бренд в snapshot"
        STORE ||--o{ INVENTORY_DAILY_SNAPSHOT : "лавка/магазин в snapshot"

        GROUP ||--o{ INVENTORY_DAILY_SNAPSHOT : "group1_id"
        GROUP ||--o{ INVENTORY_DAILY_SNAPSHOT : "group2_id"
        GROUP ||--o{ INVENTORY_DAILY_SNAPSHOT : "group3_id"
```

**Kimball** — это подход к построению хранилищ данных и BI-систем с акцентом не на “идеально централизованной” модели, а на понятных бизнесу витринах данных, собранных вокруг процессов и измерений. Его главная идея: сначала проектировать аналитику от нужд бизнеса, а уже потом подбирать структуру данных под эти задачи.

**Суть подхода:**
Методология Кимбалла строится вокруг dimensional modeling — размерной модели данных. В такой модели есть фактовые таблицы, где лежат измеряемые события, и таблицы-измерения, которые описывают контекст этих событий.

**Из чего состоит:**
Классическая архитектура по Кимбаллу обычно включает:

- staging area — зона первичной загрузки;
- ETL/ELT-процессы;
- фактовые таблицы;
- таблицы измерений;
- витрины данных для отдельных направлений бизнеса.


**Kimball vs Inmon**
- Kimball — начинаем с витрин и размерной модели, быстро даем пользу бизнесу.
- Inmon — начинаем с централизованного корпоративного хранилища, а витрины строим позже


