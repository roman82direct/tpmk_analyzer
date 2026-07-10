from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, Mapped, mapped_column
)

from backend.app.core.config import settings


async_session_maker = async_sessionmaker(
    create_async_engine(settings.database_url),
    expire_on_commit=False
)


async def get_async_session():
    with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass


class CommonMixin:
    """
    Миксин с общими полями моделей.

    Именует таблицы по именам классов моделей.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
