import functools

import disnake

from .services.CommunityService import CommunityService, GuildAndUser
from .types import CommandInteraction


def db_required(coro):
    @functools.wraps(coro)
    async def wrapper(self, inter: CommandInteraction, *args, **kwargs):
        self.bot.logger.debug(
            "Called db_required decorator for command:  {}".format(
                inter.application_command.name
            )
        )

        invoked_guild = inter.guild

        self.bot.logger.debug("Invoked guild: {}".format(invoked_guild))

        invoked_user = (
            inter.user
            if isinstance(inter.author, disnake.User)
            else inter.user._user
        )

        self.bot.logger.debug("Invoked user: {}".format(invoked_user))

        invoked_member = (
            inter.author if isinstance(inter.user, disnake.Member) else None
        )

        self.bot.logger.debug("Invoked member: {}".format(invoked_member))

        service = CommunityService.set_bot(self.bot)

        data = await service.process(guild=invoked_guild, user=invoked_user, member=invoked_member)

        self.bot.logger.debug("Data: {}".format(data))

        if isinstance(data, GuildAndUser):
            inter.guild_db = data.guild
            inter.user_db = data.user

        else:
            inter.member_db = data
            inter.guild_db = data.guild
            inter.user_db = data.user

        await coro(self, inter, *args, **kwargs)

    return wrapper
