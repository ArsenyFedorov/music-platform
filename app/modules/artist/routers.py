from fastapi import APIRouter, Depends, status
from uuid import UUID

from app.modules.artist.schemas import ArtistCreate, ArtistRead, ArtistUpdate
from app.modules.artist.service import ArtistService
from app.modules.artist.dependencies import get_artist_service
from app.modules.users.models import User
from app.modules.users.dependencies import get_current_user



router = APIRouter(prefix="/artists", tags=["artists"])


@router.post("", response_model=ArtistRead)
async def create_artist(
    data: ArtistCreate,
    artist_service: ArtistService = Depends(get_artist_service)
) -> ArtistRead:
    artist = await artist_service.create_artist(data=data)
    followers = await artist_service.get_artist_followers_count(artist.id)

    artist_model = ArtistRead(
            id=artist.id,
            name=artist.name,
            description=artist.description,
            followers=followers,
            )

    return artist_model


@router.get("/{artist_id}", response_model=ArtistRead)
async def get_artist(
    artist_id: UUID,
    artist_service: ArtistService = Depends(get_artist_service)
) -> ArtistRead:
    artist = await artist_service.get_artist(artist_id=artist_id)
    followers = await artist_service.get_artist_followers_count(artist_id=artist_id)

    artist_model = ArtistRead(
                id=artist.id,
                name=artist.name,
                description=artist.description,
                followers=followers,
                )
    
    return artist_model


@router.get("", response_model=list[ArtistRead])
async def get_artists(
    artist_service: ArtistService = Depends(get_artist_service)
) -> list[ArtistRead]:
    artists = await artist_service.get_artists()
    followers = [await artist_service.get_artist_followers_count(artist.id) for artist in artists]

    responce_data = []

    for i in range(len(artists)):
        artist_model = ArtistRead(
                id=artists[i].id,
                name=artists[i].name,
                description=artists[i].description,
                followers=followers[i],
                )
        responce_data.append(artist_model)

    return responce_data


@router.post("/{artist_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def follow_artist(
    artist_id: UUID,
    current_user: User = Depends(get_current_user),
    artist_service: ArtistService = Depends(get_artist_service)
) -> None:
    
    await artist_service.follow_artist(user_id=current_user.id, artist_id=artist_id)


@router.delete("/{artist_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_artist(
    artist_id: UUID,
    current_user: User = Depends(get_current_user),
    artist_service: ArtistService = Depends(get_artist_service)
) -> None:
    
    await artist_service.unfollow_artist(user_id=current_user.id, artist_id=artist_id)

@router.get("/{artist_id}/followers/count")
async def get_followers_count(
    artist_id: UUID,
    artist_service: ArtistService = Depends(get_artist_service)
) -> int:

    return await artist_service.get_artist_followers_count(artist_id=artist_id)



@router.patch("/{artist_id}", response_model=ArtistRead)
async def update_artist(
    data: ArtistUpdate,
    artist_id: UUID,
    _: User = Depends(get_current_user),
    artist_service: ArtistService = Depends(get_artist_service)
) -> ArtistRead:
    artist = await artist_service.update(artist_id=artist_id, data=data)
    return ArtistRead.model_validate(artist)



@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(
    artist_id: UUID,
    _: User = Depends(get_current_user),
    artist_service: ArtistService = Depends(get_artist_service)
) -> None:
    await artist_service.delete(artist_id=artist_id)

    
