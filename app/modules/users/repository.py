from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.modules.users.models import User


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.id == user_id)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    def create_user(self, user: User) -> None:
        self.session.add(user)


    async def delete(self, user: User) -> None:
        await self.session.delete(user)