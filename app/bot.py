from pathlib import Path

from disnake.ext.commands import InteractionBot
from pydantic import BaseSettings

from .loggs import logger, disnake_logger
from .db import prisma

__all__ = ["Bot"]


class AppSettings(BaseSettings):
    TESTING: bool = True


class Bot(InteractionBot):
    def __init__(self, *args, **kwargs):
        self.APP_SETTINGS = AppSettings()
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.logger = logger
        self.prisma = prisma
        self.disnake_logger = disnake_logger
        super().__init__(*args, **kwargs)
