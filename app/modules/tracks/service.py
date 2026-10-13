from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.modules.tracks.schemas import TrackCreate, TrackRead, TrackUpdate
from app.modules.tracks.models import Track
from app.modules.tracks.repository import TrackRepository
from app.modules.artist.repository import ArtistRepository
from app.core.exceptions import NotFoundError



class TrackService:
    def __init__(self,session: AsyncSession):
        self.session = session
        self.track_repository = TrackRepository(session=session)
        self.artist_repository = ArtistRepository(session=session)

    def is_none(self, new_arg, old_arg):
        if new_arg is not None:
            return new_arg

        return old_arg

    async def get_track(self, track_id: UUID) -> Track:
        track = await self.track_repository.get_track(track_id=track_id)
        if track is None:
            raise NotFoundError(detail="TRACK NOT FOUND =(")

        return track

    async def get_tracks(self, artist_id: UUID) -> list[Track]:
        artist_existing = await self.artist_repository.get_artist(artist_id=artist_id)
        if artist_existing is None:
            raise NotFoundError(detail="ARTIST NOT FOUND =(")


        return await self.track_repository.get_tracks(artist_id=artist_id)


    async def create(self, data: TrackCreate) -> Track:
        artist_existing = await self.artist_repository.get_artist(artist_id=data.artist_id)
        if artist_existing is None:
            raise NotFoundError(detail="ARTIST NOT FOUND =(")

        track = Track(
            title=data.title,
            artist_id=data.artist_id,
            duration_seconds=data.duration_seconds,
            audio_url=str(data.audio_url),
            cover_url=str(data.cover_url)
        )

        self.track_repository.create(track=track)

        await self.session.commit()

        return track

    async def delete(self, track_id: UUID) -> None:
        track = await self.track_repository.get_track(track_id=track_id)
        if track is None:
            raise NotFoundError(detail="TRACK NOT FOUND =(")

        await self.track_repository.delete(track=track)
        await self.session.commit()


    async def update(self, track_id: UUID, data: TrackUpdate) -> Track:
        track = await self.get_track(track_id=track_id)

        track.title = self.is_none(data.title,track.title)
        track.duration_seconds = self.is_none(data.duration_seconds, track.duration_seconds)
        track.audio_url = str(self.is_none(data.audio_url, track.audio_url))
        track.cover_url = str(self.is_none(data.cover_url, track.cover_url))

        await self.session.commit()
        await self.session.refresh(track)

        return track

