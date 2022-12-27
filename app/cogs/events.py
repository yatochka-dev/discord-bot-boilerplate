import os

from disnake.ext.commands import Cog

from app import Bot
from app.services.GuildService import GuildService


class Events(Cog, GuildService):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener(
        "on_ready",
    )
    async def on_ready(self):
        self.bot.logger.info(
            f"Logged in as {self.bot.user} (ID: {self.bot.user.id})"
        )
        self.bot.logger.info(
            f"Started bot in {os.getenv('STATE_NAME').title()} mode."
        )
        self.bot.logger.info("------")

        for guild in self.bot.guilds:
            if not await self.is_guild_exists(guild.id):
                await self.add_guild(guild)
                self.bot.logger.info(
                    f"Added guild: {guild.name} (ID: {guild.id})"
                )
            else:
                self.bot.logger.info(
                    f"Guild already exists: {guild.name} (ID: {guild.id})"
                )

    @Cog.listener(
        "on_guild_join",
    )
    async def on_guild_join(self, guild):
        await self.add_guild(guild)
        self.bot.logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")

    @Cog.listener(
        "on_guild_remove",
    )
    async def on_guild_remove(self, guild):
        await self.remove_guild(guild)
        self.bot.logger.info(f"Left guild: {guild.name} (ID: {guild.id})")


def setup(bot: Bot):
    bot.add_cog(Events(bot))
