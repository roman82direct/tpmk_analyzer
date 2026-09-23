from sqlalchemy import Integer, String
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

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
