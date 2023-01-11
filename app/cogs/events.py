import os

import disnake
from disnake.ext.commands import Cog

from app import Bot, Embed, md, CodeBlock
from app.services.GuildService import GuildService
from app.services.MemberService import MemberService


class Events(Cog, GuildService, MemberService):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def get_channel(guild: disnake.Guild):
        for channel in guild.channels:
            if isinstance(channel, disnake.TextChannel):
                can_send = channel.permissions_for(guild.me).send_messages
                if can_send:
                    return channel
                else:
                    continue

    @Cog.listener(
        "on_ready",
    )
    async def is_ready(self):
        self.bot.logger.info(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        self.bot.logger.info(f"Started bot in {os.getenv('STATE_NAME').title()} mode.")
        self.bot.logger.info("------")

        for guild in self.bot.guilds:
            if not await self.exists_guild(guild.id):
                await self.add_guild(guild)
                self.bot.logger.info(f"Added guild: {guild.name} (ID: {guild.id})")
            else:
                self.bot.logger.info(f"Guild already exists: {guild.name} (ID: {guild.id})")

    @Cog.listener(
        "on_guild_join",
    )
    async def joined_guild(self, guild: disnake.Guild):
        await self.add_guild(guild)
        self.bot.logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")

        embed = Embed(
            title="Thanks for adding me!",
            description=f"I'm a template bot for {md('Disnake'):bold}."
            f"\n"
            f"{CodeBlock(f'Start-Process -FilePath {self.bot.APP_SETTINGS.github_link}'):bash}",
            user=guild.me,
        ).info

        channel = await self.get_channel(guild)

        if channel:
            await channel.send(embed=embed)
            await guild.owner.send(embed=embed)
        else:
            await guild.owner.send(embed=embed)

    @Cog.listener(
        "on_guild_remove",
    )
    async def quit_guild(self, guild):
        await self.remove_guild(guild)
        self.bot.logger.info(f"Left guild: {guild.name} (ID: {guild.id})")

    @Cog.listener(
        "on_member_remove",
    )
    async def member_left(self, member: disnake.Member):
        await self.remove_member(member)
        self.bot.logger.info(f"Member left: {member} (ID: {member.id})")


def setup(bot: Bot):
    bot.add_cog(Events(bot))
