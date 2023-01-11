import disnake
from prisma import models

from .index import CRUDXService


class GuildService(CRUDXService):

    async def add_guild(self, guild: disnake.Guild) -> models.Guild:
        self.bot.logger.debug(
            f"Adding guild: {guild.name} (ID: " f"{guild.id})"
        )
        return await self.bot.prisma.guild.create(
            data={"snowflake": guild.snowflake}
        )

    async def get_guild(self, guild_id: int) -> models.Guild:
        self.bot.logger.debug(f"Getting guild by id: {guild_id}")
        guild: models.Guild = await self.bot.prisma.guild.find_first(
            where={"snowflake": self.to_safe_snowflake(guild_id)}
        )

        return guild

    async def remove_guild(self, guild: disnake.Guild):
        self.bot.logger.debug(f"Removing guild: {guild.name} (ID: {guild.id})")
        return await self.bot.prisma.guild.delete(
            where={"snowflake": guild.snowflake}
        )

    async def exists_guild(self, guild_id: int) -> bool:
        self.bot.logger.debug(f"Checking if guild exists: {guild_id}")
        return (
                await self.bot.prisma.guild.find_first(
                    where={"snowflake": self.to_safe_snowflake(guild_id)}
                )
                is not None
        )


    async def get_all_guilds(self) -> list[models.Guild]:
        self.bot.logger.debug("Getting guilds list")
        return await self.bot.prisma.guild.find_many()
