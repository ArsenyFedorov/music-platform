from sqlalchemy import String, CheckConstraint, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID

from app.db.base import Base, IdMixin


class Track(IdMixin, Base):
    __tablename__ = "tracks"

    __table_args__ = (
        CheckConstraint(
            "duration_seconds > 0",
            name="ck_tracks_duration_positive",
        ),
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    artist_id: Mapped[UUID] = mapped_column(ForeignKey("artists.id", ondelete="CASCADE"), nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    audio_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    cover_url: Mapped[str] = mapped_column(String(1024), nullable=False)