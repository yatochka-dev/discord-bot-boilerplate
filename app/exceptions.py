from disnake.ext.commands import CommandInvokeError as cmd_invoke_error

from .loggs import logger


class BotException(cmd_invoke_error):
    code: int
    message: str

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

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
