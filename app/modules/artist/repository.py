from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID

from app.modules.artist.models import Artist, ArtistFollower


  
class ArtistRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_artist(self, artist_id: UUID) -> Artist | None:
        query = select(Artist).where(
                            Artist.id == artist_id
                        )
        
        return await self.session.scalar(query)

    async def get_artists(self, limit: int = 100, offset: int = 0) -> list[Artist]:
        query = select(Artist).order_by(Artist.name).limit(limit).offset(offset)
        result = await self.session.execute(query)

        return list(result.scalars().all())
    

    def create_artist(self, artist: Artist) -> None:
        self.session.add(artist)


    async def get_follower(self, artist_id: UUID, user_id: UUID) -> ArtistFollower | None:
        query = select(ArtistFollower).where(
            ArtistFollower.artist_id == artist_id,
            ArtistFollower.user_id == user_id,
        )

        return await self.session.scalar(query)


    def follow_artist(self, follower: ArtistFollower) -> None:
        self.session.add(follower)


    async def unfollow_artist(self, follower: ArtistFollower) -> None:
        await self.session.delete(follower)


    async def get_artist_followers_count(self, artist_id: UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(ArtistFollower)
            .where(
                ArtistFollower.artist_id == artist_id
            )
        )

        return await self.session.scalar(stmt) or 0

    