import functools

import disnake
from disnake.ext.commands import InvokableApplicationCommand

from .types import CommandInteraction


def db_required(coro):
    @functools.wraps(coro)
    async def wrapper(self, interaction: CommandInteraction, *args, **kwargs):
        invoked_guild = interaction.guild
        invoked_user = (
            interaction.user
            if isinstance(interaction.user, disnake.User)
            else interaction.user._user
        )
        invoked_member = (
            interaction.member
            if isinstance(interaction.user, disnake.Member)
            else None
        )





        await coro(self, interaction, *args, **kwargs)

    return wrapper
