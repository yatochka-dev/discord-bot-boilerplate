from pydantic import BaseModel

from .main import EmbedDANT


class MessageDANT(BaseModel):
    channel_id: int
    embed: EmbedDANT
