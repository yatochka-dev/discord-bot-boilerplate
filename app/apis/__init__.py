from fastapi import APIRouter

from .guilds import router as authRouter

__all__ = [
    "apis",
]
apis = APIRouter()
apis.include_router(authRouter)
