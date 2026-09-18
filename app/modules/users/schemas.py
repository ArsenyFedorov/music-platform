from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=255)
    username: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=255)


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    username: str