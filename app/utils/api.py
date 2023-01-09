import asyncio

from starlette.requests import Request

from app import Bot


def get_bot_from_request(request: Request) -> Bot:
    bot: Bot = request.app.state.bot

    if not bot.is_ready():
        asyncio.run(bot.wait_until_ready())

    return bot
