import functools

import disnake

from .services.CommunityService import CommunityService, GuildAndUser
from .types import CommandInteraction


def db_required(coro):
    @functools.wraps(coro)
    async def wrapper(self, interaction: CommandInteraction, *args, **kwargs):
        self.bot.logger.debug(
            "Called db_required decorator for command:  {}".format(
                interaction.application_command.name
            )
        )

        invoked_guild = interaction.guild

        self.bot.logger.debug(
            "Invoked guild: {}".format(invoked_guild)
        )

        invoked_user = (
            interaction.user
            if isinstance(interaction.author, disnake.User)
            else interaction.user._user
        )

        self.bot.logger.debug(
            "Invoked user: {}".format(invoked_user)
        )

        invoked_member = (
            interaction.author
            if isinstance(interaction.user, disnake.Member)
            else None
        )

        self.bot.logger.debug(
            "Invoked member: {}".format(invoked_member)
        )

        service = CommunityService.set_bot(self.bot)

        data = await service.process(
            guild=invoked_guild,
            user=invoked_user,
            member=invoked_member
        )

        self.bot.logger.debug(
            "Data: {}".format(data)
        )

        if isinstance(data, GuildAndUser):
            interaction.guild_db = data.guild
            interaction.user_db = data.user

        else:
            interaction.member_db = data
            interaction.guild_db = data.guild
            interaction.user_db = data.user

        await coro(self, interaction, *args, **kwargs)

    return wrapper
