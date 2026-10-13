from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID



class TrackCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    artist_id: UUID
    duration_seconds: int = Field(gt=0)
    audio_url: HttpUrl = Field(max_length=1024)
    cover_url: HttpUrl = Field(max_length=1024)



class TrackUpdate(BaseModel):
    title: str | None = Field(max_length=255, default=None)
    duration_seconds: int | None = Field(gt=0, default=None)
    audio_url: HttpUrl | None = Field(max_length=1024, default=None)
    cover_url: HttpUrl | None = Field(max_length=1024, default=None)


class TrackRead(BaseModel):
    id: UUID
    title: str
    artist_id: UUID
    duration_seconds: int
    audio_url: HttpUrl
    cover_url: HttpUrl 

