from typing import Mapping

import disnake
from prisma import models

from .index import CRUDXService


class UserService(CRUDXService):
    async def add_user(self, user: disnake.User) -> models.Guild:
        if not isinstance(user, disnake.User):
            raise TypeError(f"user must be a disnake.User, and not {user.__class__.__name__!r}")
        self.bot.logger.debug(f"Adding user: {user} (ID: " f"{user.id})")
        return await self.bot.prisma.user.create(
            data={"snowflake": self.to_safe_snowflake(user.id)}
        )

    async def get_user(self, user_id: int, include: Mapping[str, bool] = None) -> models.User:
        self.bot.logger.debug(f"Getting user by id: {user_id}")
        user: models.User = await self.bot.prisma.user.find_first(
            where={"snowflake": self.to_safe_snowflake(user_id)},
            include=include,
        )

        return user

    # remove
    async def remove_user(self, user: disnake.User | disnake.Member):
        self.bot.logger.debug(f"Removing user: {user} (ID: {user.id})")
        return await self.bot.prisma.user.delete(
            where={"snowflake": self.to_safe_snowflake(user.id)},
            include={
                "members": True,
            },
        )

    async def exists_user(self, user_id: int) -> bool:
        self.bot.logger.debug(f"Checking if guild exists: {user_id}")
        return (
            await self.bot.prisma.user.find_first(
                where={"snowflake": self.to_safe_snowflake(user_id)}
            )
            is not None
        )
