from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base


class LoadBatch(Base):
    """Таблица истории ежедневных загрузок."""

    __tablename__ = 'load_batch'
