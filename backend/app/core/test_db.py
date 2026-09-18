import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from backend.app.config.settings import backend_settings
from backend.app.core.db import create_clickhouse_engine


async def test_postgres():
    """Проверка подключения к PostgreSQL."""
    engine = create_async_engine(backend_settings.postgres_url)

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text('SELECT 1 AS check'))
            row = result.fetchone()
            print(f'PostgreSQL: подключено, check={row.check}')
    except Exception as exc:
        print(f'PostgreSQL: ошибка подключения — {exc}')
        raise
    finally:
        await engine.dispose()


def test_clickhouse() -> None:
    """Проверяет ClickHouse через общий cached Engine."""
    engine = create_clickhouse_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text('SELECT * FROM balances_total LIMIT 10')
            )

        print(f'ClickHouse: подключено, check={result.first()}')

    except Exception as exc:
        print(
            'ClickHouse: ошибка подключения — '
            f'{type(exc).__name__}: {exc}'
        )
        raise


async def main() -> None:
    # await test_postgres()
    test_clickhouse()


if __name__ == '__main__':
    asyncio.run(main())
