from disnake.ext.commands import CommandInvokeError as cmd_invoke_error

from .embedding import Embed
from .loggs import logger
from .types import DiscordUtilizer


class BotException(cmd_invoke_error):
    code: int
    title: str = "Something went wrong, try again later"
    message: str

    def __init__(self, code: int, message: str, title=None):
        self.code = code
        self.message = message

        if title:
            self.title = title

    def to_embed(
            self,
            user: DiscordUtilizer
    ):
        return Embed(
            title=self.title,
            description=self.message,
            user=user
        ).error

    @classmethod
    def assert_value(cls, sequence: bool, error_code: int, message: str, *, warn: bool = False):
        if not sequence:
            if warn:
                logger.warn(message)
            raise cls(error_code, message)


class CommandInvokeError(BotException):
    code = 400
    message = "Command invoke error"


class InvalidArgument(BotException):
    code = 401
    message = "Invalid argument"


class MissingRequiredArgument(BotException):
    code = 402
    message = "Missing required argument"


class MissingPermissions(BotException):
    code = 403
    message = "Missing permissions"


class CantUseThatHere(BotException):
    code = 404
    message = "You can't use that here"
