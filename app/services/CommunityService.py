from typing import overload, NamedTuple

import disnake
from prisma import models

from .GuildService import GuildService
from .UserService import UserService


class GuildAndUser(NamedTuple):
    guild: models.Guild
    user: models.User


class CommunityService(GuildService, UserService):
    async def process_guild(self, guild: disnake.Guild):
        if not isinstance(guild, disnake.Guild):
            raise TypeError("guild must be a disnake.Guild")

        guild_ = await self.get_guild(guild_id=guild.id)

        if isinstance(guild_, models.Guild):
            return guild_

        return await self.add_guild(guild)

    async def process_user(self, user: disnake.User):
        if not isinstance(user, disnake.User):
            raise TypeError("user must be a disnake.User")

        user_ = await self.get_user(user_id=user.id)

        if isinstance(user_, models.User):
            return user_

        return await self.add_user(user)

    async def process_member(
        self, guild: disnake.Guild = None, user: disnake.User = None, member: disnake.Member = None
    ):
        if not isinstance(member, disnake.Member):
            raise TypeError("member must be a disnake.Member")

        processed_guild = await self.process_guild(guild)
        processed_user = await self.process_user(user)

        exists = await self.bot.prisma.member.find_first(
            where={
                "guild": {"snowflake": processed_guild.snowflake},
                "user": {"snowflake": processed_user.snowflake},
            },
            include={"guild": True, "user": True},
        )

        if exists or False:
            return exists

        return await self.bot.prisma.member.create(
            data={
                "guild": {"connect": {"snowflake": processed_guild.snowflake}},
                "user": {"connect": {"snowflake": processed_user.snowflake}},
            }
        )

    @overload
    async def process(self) -> None:
        ...

    @overload
    async def process(self, guild: disnake.Guild) -> models.Guild:
        ...

    @overload
    async def process(self, user: disnake.User) -> models.User:
        ...

    @overload
    async def process(self, guild: disnake.Guild, user: disnake.User) -> GuildAndUser:
        ...

    @overload
    async def process(
        self, guild: disnake.Guild, user: disnake.User, member: disnake.Member
    ) -> models.Member:
        ...

    async def process(
        self, guild: disnake.Guild = None, user: disnake.User = None, member: disnake.Member = None
    ):
        """
        This function process is an asynchronous method that processes different inputs and
        returns different outputs depending on the parameters provided. The method has several
        overloads:

            If no parameter is provided, the method returns None
            If a single guild parameter of type disnake.Guild is provided, the method returns a
            models.Guild object
            If a single user parameter of type disnake.User is provided, the method returns a
            models.User object
            If both guild and user parameters of type disnake.Guild and disnake.User respectively
            are
            provided, the method returns a GuildAndUser object
            If all three parameters guild, user, and member of type disnake.Guild, disnake.User,
            and disnake.Member respectively are provided, the method returns a models.Member object
            However, when the member parameter is provided, guild and user parameters must also be
            provided, otherwise, a ValueError will be raised.
        """
        if member:
            if not guild or not user:
                raise ValueError("guild and user must be provided if member is provided")

            return await self.process_member(guild=guild, user=user, member=member)
        else:
            if guild:
                guild = await self.process_guild(guild)
            elif user:
                user = await self.process_user(user)

            if guild and user:
                return GuildAndUser(guild, user)

            return guild or user
