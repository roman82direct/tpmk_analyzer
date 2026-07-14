from sqlalchemy import String, Integer
from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, Mapped, mapped_column
)


class Base(DeclarativeBase):
    pass


class CommonMixin:
    """
    Миксин с общими полями для справочников.

    Именует таблицы по именам классов моделей.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
