import datetime
from pathlib import Path

from disnake.ext.commands import InteractionBot
from pydantic import BaseSettings

from .db import prisma
from .loggs import logger, disnake_logger

__all__ = ["Bot", "Settings"]


class AppSettings(BaseSettings):
    TESTING: bool = True
    TIMEZONE = datetime.timezone(
        offset=datetime.timedelta(hours=3), name="UTC"
    )

    # EMBED SETTINGS
    RGB_EMBED_COLOR: tuple = (255, 255, 255)
    # if none - won't be added
    AUTHOR_DISPLAY_NAME: str | None = None
    ICON_URL: str | None = None


Settings = AppSettings()


class Bot(InteractionBot):
    def __init__(self, *args, **kwargs):
        self.APP_SETTINGS = AppSettings()
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.logger = logger
        self.prisma = prisma
        self.disnake_logger = disnake_logger
        super().__init__(*args, **kwargs)
