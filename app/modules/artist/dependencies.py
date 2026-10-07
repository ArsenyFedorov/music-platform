from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.artist.service import ArtistService
from app.db.session import get_db_session


def get_artist_service(
    session: AsyncSession = Depends(get_db_session)
) -> ArtistService:
    return ArtistService(session=session)