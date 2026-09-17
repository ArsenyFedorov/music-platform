from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID, uuid4


class Base(DeclarativeBase):
    ...


class IdMixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True, 
        default=uuid4
    )