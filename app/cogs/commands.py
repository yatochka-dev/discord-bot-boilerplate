from disnake.ext.commands import Cog, slash_command

from app import Bot, md
from app.embedding import Embed
from app.types import CommandInteraction


class Command(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()
    async def ping(self, interaction: CommandInteraction) -> None:
        await interaction.send(
            embed=Embed(
                title="Pong!",
                description=f"{md('Latency'):bold}:"
                f" {self.bot.latency * 1000:.2f} "
                f"ms",
                user=interaction.user,
            ).default
        )


def setup(bot: Bot):
    bot.add_cog(Command(bot))
