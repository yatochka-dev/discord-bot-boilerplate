from fastapi import APIRouter

from .guilds import router as authRouter
from .messaging import router as messagingRouter

__all__ = [
    "apis",
]
apis = APIRouter()
apis.include_router(authRouter)
apis.include_router(messagingRouter)
