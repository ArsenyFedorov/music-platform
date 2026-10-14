from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID


from app.modules.artist.repository import ArtistRepository
from app.modules.artist.schemas import ArtistCreate, ArtistUpdate
from app.modules.artist.models import Artist, ArtistFollower
from app.core.exceptions import NotFoundError, FollowerAlreadeExistsError, ArtistNameAlreadeExistsError
from app.modules.users.repository import UserRepository





class ArtistService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.artist_repository = ArtistRepository(session=session)
        self.user_repository = UserRepository(session=session)


    def is_none(self, new_arg, old_arg):
            if new_arg is not None:
                return new_arg
    
            return old_arg


    async def create_artist(self, data: ArtistCreate) -> Artist:
        name_existing = self.artist_repository.get_artist_by_name(data.name)
        if name_existing is not None:
            raise ArtistNameAlreadeExistsError("ARTIST WITH THAT NAME ALREADY EXISTS")


        artist = Artist(
            name=data.name,
            description=data.description,
        )

        self.artist_repository.create_artist(artist=artist)

        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            if "uq_artists_name" in str(exc.orig):
                raise ArtistNameAlreadeExistsError(detail="ARTIST WITH THAT NAME ALREADY EXISTS")
            else:
                raise
        
        

        return artist


    async def get_artist(self, artist_id: UUID) -> Artist:
        artist = await self.artist_repository.get_artist(artist_id=artist_id)

        if not artist:
            raise NotFoundError(detail="ARTIST NOT FOUND =(")

        return artist

    async def get_artists(self) -> list[Artist]:
        artist_list = await self.artist_repository.get_artists()

        return artist_list
    


    async def follow_artist(self, user_id: UUID, artist_id: UUID) -> None:
        await self.get_artist(artist_id=artist_id)
 


        user = await self.user_repository.get_by_id(user_id=user_id)
        if not user:
            raise NotFoundError(detail="USER NOT FOUND")
        


        existrs_follower = await self.artist_repository.get_follower(user_id=user_id, artist_id=artist_id)
        if existrs_follower:
            raise FollowerAlreadeExistsError(detail="YOU FOLLOW THIS ARTIST")

        follower = ArtistFollower(
            artist_id=artist_id,
            user_id=user_id,
        )

        self.artist_repository.follow_artist(follower=follower)

        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            if "uq_artist_followers_artist_id_user_id" in str(exc.orig):
                raise FollowerAlreadeExistsError(detail="YOU FOLLOW THIS ARTIST")
            else:
                raise
                
        await self.session.commit()


    async def unfollow_artist(self, user_id: UUID, artist_id: UUID) -> None:
        await self.get_artist(artist_id=artist_id)

        user = await self.user_repository.get_by_id(user_id=user_id)
        if not user:
            raise NotFoundError(detail="USER NOT FOUND")
       
        
        follower = await self.artist_repository.get_follower(user_id=user_id, artist_id=artist_id)
        if not follower:
            raise NotFoundError(detail="YOU NOT FOLLOW THIS ARTIST")

        await self.artist_repository.unfollow_artist(follower=follower)
        await self.session.commit()


    async def get_artist_followers_count(self, artist_id: UUID) -> int:
        await self.get_artist(artist_id=artist_id)

        followers_count = await self.artist_repository.get_artist_followers_count(artist_id=artist_id)
        return followers_count


    async def update(self, artist_id: UUID, data: ArtistUpdate) -> Artist:
        name_existing = self.artist_repository.get_artist_by_name(artist_name=data.name)
        if name_existing is not None:
            raise ArtistNameAlreadeExistsError("ARTIST WITH THAT NAME ALREADY EXISTS")

        artist = await self.get_artist(artist_id=artist_id)
        artist.name = self.is_none(data.name, artist.name)
        artist.description = self.is_none(data.description, artist.description)

        await self.session.commit()
        await self.session.refresh(artist)

        return artist



    async def delete(self, artist_id: UUID) -> None:
        artist = await self.get_artist(artist_id=artist_id)

        await self.artist_repository.delete(artist)
        await self.session.commit()


        

        