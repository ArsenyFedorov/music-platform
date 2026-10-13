from fastapi import APIRouter

from app.modules.users.routers import router as user_router
from app.modules.artist.routers import router as artist_router
from app.modules.tracks.routers import router as track_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(artist_router)
api_router.include_router(track_router)


