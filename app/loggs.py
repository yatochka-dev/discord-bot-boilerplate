import logging
import sys

from colorama import Fore, Style, Back

FORMATS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.BLUE,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Back.RED + Fore.WHITE,
}

red_stick = Fore.LIGHTRED_EX + " | " + Style.RESET_ALL
red_column = Fore.LIGHTRED_EX + ":" + Style.RESET_ALL
red_dash = Fore.LIGHTRED_EX + " - " + Style.RESET_ALL

FORMAT = (
    Fore.GREEN
    + "%(asctime)s "
    + Style.RESET_ALL
    + red_stick
    + "{primary_color}\033[1m%(levelname)s\033[0m{spaces}"
    + red_stick
    + Fore.CYAN
    + "%(filename)s"
    + red_column
    + Fore.CYAN
    + "%(name)s"
    + red_column
    + Fore.CYAN
    + "%(lineno)d"
    + red_dash
    + "{secondary_color}%(message)s"
    + Style.RESET_ALL
)


def get_format_spaces(record: int):
    _levelToSpaces = {
        logging.CRITICAL: 2,
        logging.ERROR: 5,
        logging.WARNING: 3,
        logging.INFO: 6,
        logging.DEBUG: 5,
        logging.NOTSET: 4,
    }

    return _levelToSpaces[record]


def get_format(record: int):
    spaces = " " * get_format_spaces(record)
    color = FORMATS[record]
    return FORMAT.format(
        spaces=Style.RESET_ALL + spaces,
        primary_color=color,
        secondary_color=color,
    )


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def format(self, record):
        log_fmt = get_format(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)


disnake_logger = logging.getLogger("disnake")
disnake_logger.setLevel(logging.WARNING)
disnake_logger.addHandler(handler)


__all__ = ["logger", "disnake_logger"]
