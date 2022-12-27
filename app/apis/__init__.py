from fastapi import APIRouter
from .guilds import router as authRouter

apis = APIRouter()
apis.include_router(authRouter)
__all__ = ["apis"]
