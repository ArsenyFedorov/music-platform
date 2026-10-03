from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


from app.modules.users.service import UserService
from app.modules.users.repository import UserRepository
from app.db.session import get_db_session
from app.core.security import decode_access_token
from app.modules.users.models import User
from app.core.exceptions import InvalidTokenError, NotFoundError


def get_user_service(
        session: AsyncSession = Depends(get_db_session)
) -> UserService:
    return UserService(session)

def get_user_repository(
        session: AsyncSession = Depends(get_db_session)
) -> UserRepository:
    return UserRepository(session)


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    repository: UserRepository = Depends(get_user_repository),
) -> User:

    token = credentials.credentials

    data = decode_access_token(token)

    try:
        user_id = UUID(data["sub"])
    except (KeyError, ValueError):
        raise InvalidTokenError(detail="Некоректный JWT") from None

    user = await repository.get_by_id(user_id)

    if not user:
        raise NotFoundError(detail="NOT FOUND USER")

    return user
    