from fastapi import APIRouter, Depends

from app.services.GuildService import GuildService

router = APIRouter()


@router.get("/guilds/")
async def getGuilds(service: GuildService = Depends(GuildService)):
    return await service.get_all()


@router.get("/guilds/{guild_id}")
async def is_guild_exists(
        guild_id: int, service: GuildService = Depends(GuildService)
):
    return await service.exists(guild_id)


@router.get("/guilds/{guild_id}/")
async def get_guild_by_id(
        guild_id: int, service: GuildService = Depends(GuildService)
):
    return await service.get(guild_id)
