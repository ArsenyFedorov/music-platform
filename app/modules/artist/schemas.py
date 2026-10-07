from pydantic import BaseModel, Field
from uuid import UUID


class ArtistCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    description: str | None = Field(default=None, max_length=1_000)


class ArtistRead(BaseModel):
    id: UUID
    name: str
    description: str | None 
    followers: int
