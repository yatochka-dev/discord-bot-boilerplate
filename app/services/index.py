import disnake
from starlette.requests import Request

from ..bot import Bot
from ..types import SupportsIntCast
from ..utils import get_bot_from_request


class AppService:
    bot: Bot

    def __init__(self, request: Request = None):

        if request is None:
            pass
        else:
            self.bot = get_bot_from_request(request)

    @staticmethod
    def to_safe_snowflake(id_: SupportsIntCast) -> str:
        return disnake.Object(id_).snowflake

    @classmethod
    def set_bot(cls, bot: Bot):
        instance = cls()
        instance.bot = bot
        return instance


class CRUDXService(AppService):

    async def add(self, *args, **kwargs):
        pass

    async def remove(self, *args, **kwargs):
        pass

    async def get(self, *args, **kwargs):
        pass

    async def get_all(self, *args, **kwargs):
        pass

    async def exists(self, *args, **kwargs):
        pass

# class APIService(AppService):
#     bot: Bot
#
#     def __init__(self, request: Request):
#         self.request = request
#         self.bot = get_bot_from_request(request)
#
#     def println(self, text: str):
#         print(self.bot.user.name + ":\t" + text)
#
#
# class CogService(AppService):
#     bot: Bot
