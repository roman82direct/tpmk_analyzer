from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.app.core.config import settings

async_session_maker = async_sessionmaker(
    create_async_engine(settings.database_url),
    expire_on_commit=False
)


async def get_async_session():
    """Генератор асинхронной db-сессии."""
    async with async_session_maker() as session:
        yield session
