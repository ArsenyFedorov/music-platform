from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.modules.tracks.service import TrackService


def get_track_service(
    session: AsyncSession = Depends(get_db_session)
) -> TrackService:
    return TrackService(session=session)