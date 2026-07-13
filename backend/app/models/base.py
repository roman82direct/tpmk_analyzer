from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, Mapped, mapped_column
)


class Base(DeclarativeBase):
    pass


class CommonMixin:
    """Именует таблицы по именам классов моделей."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class CommonFieldsMixin(CommonMixin):
    """Миксин с общими полями моделей."""

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
