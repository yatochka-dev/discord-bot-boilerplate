import disnake

from .index import CogService


class GuildService(CogService):
    async def is_guild_exists(self, guild_id: int) -> bool:
        self.bot.logger.debug(f"Checking if guild exists: {guild_id}")
        return (
            await self.bot.prisma.guild.find_first(where={"id": str(guild_id)})
            is not None
        )

    async def add_guild(self, guild: disnake.Guild):
        self.bot.logger.debug(f"Adding guild: {guild.name} (ID: {guild.id})")
        return await self.bot.prisma.guild.create(data={"id": str(guild.id)})

    async def remove_guild(self, guild: disnake.Guild):
        self.bot.logger.debug(f"Removing guild: {guild.name} (ID: {guild.id})")
        return await self.bot.prisma.guild.delete(where={"id": str(guild.id)})
