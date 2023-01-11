from disnake.ext.commands import Cog, slash_command

from app import Bot, md, EmbedField
from app.decorators import db_required
from app.embedding import Embed
from app.services.GuildService import GuildService
from app.types import CommandInteraction
from app.utils.embeds import create_embeds_from_fields


class Command(Cog, GuildService):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()
    @db_required
    async def ping(self, interaction: CommandInteraction) -> None:
        print("Ping command")
        current_latency = round(self.bot.latency * 1000, 2)

        match current_latency:
            case x if x <= 50:
                color = (0, 255, 0)

            case x if x <= 100:
                color = (255, 255, 0)

            case x if x <= 150:
                color = (255, 165, 0)

            case x if x <= 200:
                color = (255, 0, 0)

            case _:
                color = (0, 0, 0)

        await interaction.send(
            embed=Embed(
                title="Pong!",
                description=f"{md('Latency'):bold}:{current_latency}ms",
                user=interaction.user,
            ).as_color(color)
        )

    @slash_command()
    async def get_guild_info(self, inter: CommandInteraction):
        guild_db = await self.get_guild(guild_id=inter.guild_id, include={"members": True})

        fields = [
            EmbedField(
                name=f"#{index}",
                value=f"{member.user!r}"
            )
            for index, member in enumerate(guild_db.members, 1)
        ]

        embed = Embed(
            title="Guild",
            user=inter.user,
        )

        embeds = create_embeds_from_fields(
            embed, fields
        )



    @slash_command()
    async def guilds(self, interaction: CommandInteraction) -> None:

        guilds = await self.get_all_guilds()

        fields = [
            EmbedField(name=f"#{i}", value=f"{guild.snowflake}")
            for i, guild in enumerate(guilds, 1)
        ]

        await interaction.send(
            embed=Embed(
                title="Guilds",
                description=f"{md('Guilds'):bold}: {len(guilds)}",
                fields=fields,
                user=interaction.user,
            ).info
        )


def setup(bot: Bot):
    bot.add_cog(Command(bot))
