from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID

from app.db.base import Base, IdMixin


class Artist(IdMixin, Base):
    __tablename__ = "artists"

    __table_args__ = (
    UniqueConstraint("name", name="uq_artists_name"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1_000), nullable=True)


class ArtistFollower(IdMixin, Base):
    __tablename__ = "artist_followers"

    __table_args__ = (
        UniqueConstraint(
            "artist_id",
            "user_id",
            name="uq_artist_followers_artist_id_user_id",
        ),
    )

    artist_id: Mapped[UUID] = mapped_column(ForeignKey("artists.id", ondelete="CASCADE"),nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)