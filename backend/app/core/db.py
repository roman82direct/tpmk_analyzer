from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.config.settings import backend_settings

async_session_maker = async_sessionmaker(
    create_async_engine(backend_settings.postgres_url),
    expire_on_commit=False
)


async def get_pg_async_session():
    """Генератор асинхронной postgres-сессии."""
    async with async_session_maker() as session:
        yield session


PGSession = Annotated[AsyncSession, Depends(get_pg_async_session)]


async def get_clickhouse_session():
    """Генератор clickhouse-сессии."""
