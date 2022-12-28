from fastapi import APIRouter

from app.db import prisma

router = APIRouter()


@router.get("/guilds")
async def getGuilds():
    return await prisma.guild.find_many()
