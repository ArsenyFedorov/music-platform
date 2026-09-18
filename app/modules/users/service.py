from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate
from app.modules.users.models import User
from app.core.exeptions import EmailAlreadyExistsError, UsernameAlreadyExistsError



class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session=session)


    async def register(self, data: UserCreate) -> User:
        existing_email = await self.user_repository.get_by_email(email=data.email)
        if existing_email:
            raise EmailAlreadyExistsError("Пользователь с таким email уже есть")

        existing_username = await self.user_repository.get_by_username(username=data.username)
        if existing_username:
            raise UsernameAlreadyExistsError("Пользователь с таким username уже есть")

        user = User(username=data.username, password_hash=data.password, email=data.email)
        self.user_repository.create_user(user=user)

        await self.session.flush()
        await self.session.commit()

        return user