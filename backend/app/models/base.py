from sqlalchemy.orm import DeclarativeBase, declared_attr


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
