from pydantic import BaseModel


class EmbedFieldDANT(BaseModel):
    name: str
    value: str
    inline: bool = False


class EmbedDANT(BaseModel):
    title: str
    description: str
    pre_build_color: str = "default"
    fields: list[EmbedFieldDANT]
