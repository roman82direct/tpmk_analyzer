import asyncio
import httpx

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from backend.app.config.settings import backend_settings


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


async def test_clickhouse_http():
    """Проверка подключения к ClickHouse через HTTP."""
    # url = 'http://roman.papenov%40constanta-t.ru:bRHeL%402u6SF2urHo@10.193.49.32:8124/?database=edu'
    url = backend_settings.clickhouse_url
    print(f'ClickHouse URL: {url}')

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                content='SELECT 1 AS check',
                timeout=5.0,
            )
            response.raise_for_status()
            print(f'ClickHouse HTTP: подключено, ответ: {response.text.strip()}')
        except httpx.HTTPError as exc:
            print(f'ClickHouse HTTP: ошибка — {exc}')
            raise
        except Exception as exc:
            print(f'ClickHouse HTTP: ошибка — {exc}')
            raise

if __name__ == '__main__':
    # asyncio.run(test_postgres())
    asyncio.run(test_clickhouse_http())
