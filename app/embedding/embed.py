import datetime

import disnake

from app import Settings
from app.types import DiscordUtilizer


class EmbedField:
    def __init__(self, name, value, inline=False):
        self.name = name
        self.value = value
        self.inline = inline

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "inline": self.inline
        }

    def __str__(self):
        return f"{self.name} - {self.value}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.value!r}, " \
               f"inline={self.inline!r})"


# Custom Embed
class Embed:
    BASE_COLOR = disnake.Color.from_rgb(*Settings.RGB_EMBED_COLOR)
    BASE_TIMEZONE = Settings.TIMEZONE
    MAX_EMBED_LENGTH = 3000
    BASE_AUTHOR_ICON_URL = Settings.ICON_URL

    def __init__(
            self,
            user: disnake.ClientUser | disnake.Member | disnake.User,
            thumbnail: bool = False,
            fields: list[EmbedField] | tuple[EmbedField] = (),
            *args,
            **kwargs
    ):
        self.user = user
        self.thumbnail = thumbnail
        self.fields = fields
        self.embed = disnake.Embed(*args, **kwargs)
        self._set_footer(user)

    def _set_footer(self, user: DiscordUtilizer) -> None:
        if user.avatar:
            self.embed.set_footer(text=user.name, icon_url=user.avatar.url)
        else:
            self.embed.set_footer(text=user.name)

    def _get_default(self) -> disnake.Embed:
        # copy of the self.embed
        c = self.embed.copy()
        c.timestamp = datetime.datetime.now(tz=self.BASE_TIMEZONE)

        if Settings.AUTHOR_DISPLAY_NAME:
            c.set_author(
                name=Settings.AUTHOR_DISPLAY_NAME,
            )

        if self.fields:
            for field in self.fields:
                c.add_field(**field.to_dict())

        if (
                c.description is not None and len(c.description) > 40
        ) or self.thumbnail:
            if self.BASE_AUTHOR_ICON_URL:
                c.set_thumbnail(url=self.BASE_AUTHOR_ICON_URL)

        if len(c) > self.MAX_EMBED_LENGTH:
            raise Exception(
                f"Embed length is more than {self.MAX_EMBED_LENGTH} characters"
            )

        return c

    def as_color(
            self, color: disnake.Color | tuple[int, int, int]
    ) -> disnake.Embed:

        if isinstance(color, tuple):
            color = disnake.Color.from_rgb(*color)

        # copy of the self.embed
        c = self._get_default()
        c._colour = color
        return c

    @property
    def default(self):
        return self._get_default()
