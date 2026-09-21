from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserLogin
from app.modules.users.models import User
from app.core.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError, InvalidCredentialsError
from app.core.security import hash_password, verify_password



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

        user = User(username=data.username, password_hash=hash_password(data.password), email=data.email)

        try:
            self.user_repository.create_user(user=user)

            await self.session.flush()
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            if exc.orig.constraint_name == "uq_users_email":
                raise EmailAlreadyExistsError(
                    "Пользователь с таким email уже есть"
                    ) from exc
            
            elif exc.orig.constraint_name == "uq_users_username":
                raise UsernameAlreadyExistsError(
                    "Пользователь с таким username уже есть"
                    ) from exc
            
            else:
                raise 

        return user


    async def login(self, data: UserLogin) -> User:
        user = await self.user_repository.get_by_email(data.email)

        if not user:
            raise InvalidCredentialsError(detail="НЕПРАВИЛЬНЫЙ EMAIL ИЛИ PASSWORD")
        
        if verify_password(data.password, user.password_hash):
            ...
        else:
            raise InvalidCredentialsError(detail="НЕПРАВИЛЬНЫЙ EMAIL ИЛИ PASSWORD")