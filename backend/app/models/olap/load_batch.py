from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class LoadBatch(Base):
    """Таблица истории ежедневных загрузок."""

    __tablename__ = 'load_batch'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    loaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    source_file_name: Mapped[str] = mapped_column(String)
    source_file_hash: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, nullable=False)
    rows_count: Mapped[int] = mapped_column(Integer)
    error_message: Mapped[str] = mapped_column(String)
