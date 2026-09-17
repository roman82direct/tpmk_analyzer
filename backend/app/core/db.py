from functools import lru_cache
from typing import Annotated, AsyncGenerator, Iterator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.config.settings import backend_settings

async_session_maker = async_sessionmaker(
    create_async_engine(backend_settings.postgres_url, pool_pre_ping=True),
    expire_on_commit=False
)


async def get_pg_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор асинхронной postgres-сессии."""
    async with async_session_maker() as session:
        yield session


@lru_cache(maxsize=1)
def create_clickhouse_engine() -> Engine:
    """Создаёт один синхронный ClickHouse Engine на процесс."""
    secure = backend_settings.clickhouse_secure
    ca_cert = backend_settings.clickhouse_ca_cert

    if secure and ca_cert is None:
        raise ValueError(
            'Для TLS-подключения к ClickHouse требуется CLICKHOUSE_CA_CERT.'
        )

    connect_args: dict[str, object] = {
        'secure': secure,
        'verify': secure,
    }

    if secure:
        connect_args['ca_cert'] = str(ca_cert)

    return create_engine(
        backend_settings.clickhouse_url,
        connect_args=connect_args,
    )


def get_clickhouse_connection() -> Iterator[Connection]:
    engine = create_clickhouse_engine()

    with engine.connect() as connection:
        yield connection


PGSession = Annotated[AsyncSession, Depends(get_pg_async_session)]
CHConnection = Annotated[Connection, Depends(get_clickhouse_connection)]
