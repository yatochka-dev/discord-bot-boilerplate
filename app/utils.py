import asyncio

import disnake
from fastapi import Request

from .bot import Bot
from .loggs import logger


def convert_text_to_bold(string: str, /) -> str:
    return "\033[1m" + string + "\033[0m"


def get_member_by_id(member_id: int, /):
    member = disnake.Object(member_id)

    if not isinstance(member, disnake.Member):
        logger.warn(
            f"Member with id {member_id} not found, returned "
            f"{type(member)!r} instead"
        )

    return member


def get_bot_from_request(request: Request) -> Bot:
    bot: Bot = request.app.state.bot

    if not bot.is_ready():
        asyncio.run(bot.wait_until_ready())

    return bot
