from fastapi import APIRouter, Depends, status
from uuid import UUID

from app.modules.tracks.dependencies import get_track_service
from app.modules.tracks.schemas import TrackCreate, TrackUpdate, TrackRead
from app.modules.tracks.service import TrackService
from app.modules.users.dependencies import get_current_user
from app.modules.users.models import User


router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("/{track_id}", response_model=TrackRead)
async def get_track(
    track_id: UUID,
    _: User = Depends(get_current_user),
    track_service: TrackService = Depends(get_track_service)
) -> TrackRead:
    track = await track_service.get_track(track_id=track_id)
    return TrackRead.model_validate(track)


@router.get("/artist/{artist_id}", response_model=list[TrackRead])
async def get_tracks(
    artist_id: UUID,
    _: User = Depends(get_current_user),
    track_service: TrackService = Depends(get_track_service)

) -> list[TrackRead]:
    tracks = await track_service.get_tracks(artist_id=artist_id)
    return [TrackRead.model_validate(track) for track in tracks]


@router.post("", response_model=TrackRead, status_code=status.HTTP_201_CREATED)
async def create_track(
    data: TrackCreate,
    _: User = Depends(get_current_user),
    track_service: TrackService = Depends(get_track_service)
) -> TrackRead:
    track = await track_service.create(data=data)
    return TrackRead.model_validate(track)

@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_track(
    track_id: UUID,
    _: User = Depends(get_current_user),
    track_service: TrackService = Depends(get_track_service)
) -> None:
    await track_service.delete(track_id=track_id)


@router.patch("/{track_id}", response_model=TrackRead)
async def update_track(
    track_id: UUID,
    data: TrackUpdate,
    _: User = Depends(get_current_user),
    track_service: TrackService = Depends(get_track_service)
) -> TrackRead:
    track = await track_service.update(track_id=track_id, data=data)
    return TrackRead.model_validate(track)