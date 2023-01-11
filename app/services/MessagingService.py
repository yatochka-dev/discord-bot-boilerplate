import disnake

from app.dantic import EmbedDANT
from app.embedding import Embed, EmbedField
from .index import AppService


class MessagingService(AppService):
    async def _form_embed(self, embed: EmbedDANT):
        fields = [
            EmbedField(
                name=field.name,
                value=field.value,
                inline=field.inline,
            )
            for field in embed.fields
        ]

        raw_embed = Embed(
            title=embed.title,
            description=embed.description,
            fields=fields,
            user=self.bot.user,
        )

        embed = getattr(raw_embed, embed.pre_build_color)

        return embed

    async def send_message(self, embed: EmbedDANT, channel_id: int) -> disnake.Message | None:
        embed = await self._form_embed(embed)

        channel = self.bot.get_channel(channel_id)

        if channel is None:
            raise ValueError(f"Channel with id {channel_id} not found")

        try:
            message = await channel.send(embed=embed)
        except Exception as exc:
            self.bot.logger.error(f"Error while sending embed: {exc}", exc_info=exc)
            raise exc from exc

        return message
