from fastapi import APIRouter, Depends
from uuid import UUID

from app.modules.users.schemas import UserLogin, UserRead, UserCreate
from app.modules.users.service import UserService
from app.modules.users.dependencies import get_user_service, get_current_user
from app.modules.users.models import User



router = APIRouter(prefix="/users", tags=["users"])



@router.post("/login")
async def login_user(
    data: UserLogin,
    user_service: UserService = Depends(get_user_service)
) -> dict:

    token = await user_service.login(data=data)

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserRead)
async def register(
    data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> UserRead:
    user = await user_service.register(data)

    return UserRead.model_validate(user, from_attributes=True)

@router.get("/me", response_model=UserRead)
async def return_user(
    current_user: User = Depends(get_current_user)
) -> UserRead:

    return UserRead.model_validate(current_user, from_attributes=True)
