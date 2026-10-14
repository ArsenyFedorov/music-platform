from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID


from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserLogin, UserUpdate
from app.modules.users.models import User
from app.core.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError, InvalidCredentialsError, NotFoundError
from app.core.security import hash_password, verify_password, create_access_token




class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session=session)

    def is_none(self, new_arg, old_arg):
            if new_arg is not None:
                return new_arg
    
            return old_arg


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


    async def login(self, data: UserLogin) -> str:
        user = await self.user_repository.get_by_email(data.email)

        if not user:
            raise InvalidCredentialsError(detail="НЕПРАВИЛЬНЫЙ EMAIL ИЛИ PASSWORD")
        
        if not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError(detail="НЕПРАВИЛЬНЫЙ EMAIL ИЛИ PASSWORD")
        
        return create_access_token(user.id)


    async def delete(self, user_id: UUID) -> None:
        user = await self.user_repository.get_by_id(user_id=user_id)
        if user is None: 
            raise NotFoundError(detail="USER NOT FOUND =(")

        await self.user_repository.delete(user=user)
        await self.session.commit()


    async def update(self, user_id: UUID, data: UserUpdate) -> User:
        user = await self.user_repository.get_by_id(user_id=user_id)
        if user is None:
            raise NotFoundError(delattr="USER NOT FOUND =(")

        name_existing = self.user_repository.get_by_username(data.username)
        if name_existing is not None:
            raise UsernameAlreadyExistsError(detail="USER WITH THAT NAME ALREADE EXISTS =(")

        user.username = self.is_none(data.username, user.username)
        user.password_hash = self.is_none(hash_password(data.password), user.password_hash)

        self.session.commit()
        self.session.refresh(user)

        return user



        