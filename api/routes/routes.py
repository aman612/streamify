from fastapi import APIRouter


from .videos import router as video_router

base_router = APIRouter()

base_router.include_router(video_router, tags=["video"], prefix="/video")
