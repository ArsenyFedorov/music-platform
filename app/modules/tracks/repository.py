from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.modules.tracks.models import Track



class TrackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_tracks(self, artist_id: UUID) -> list[Track]:
        query = select(Track).where(Track.artist_id == artist_id)
        result = await self.session.execute(query)

        return list(result.scalars().all())

    async def get_track(self, track_id: UUID) -> Track | None:
        query = select(Track).where(Track.id == track_id)

        return await self.session.scalar(query)

    def create(self, track: Track) -> None:
        self.session.add(track)

    async def delete(self, track: Track) -> None:
        await self.session.delete(track)