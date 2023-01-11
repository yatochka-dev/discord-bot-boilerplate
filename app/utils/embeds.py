import disnake

from app import Embed, EmbedField


def create_embeds_from_fields(
        embed: Embed, fields: list[EmbedField], max_size: int = 6, emb_style: str = "default"
) -> list[Embed] | None:
    assert max_size <= 25, "Max size must be less or equal to 25"

    embeds = []

    chunks = disnake.utils.as_chunks(fields, max_size)
    emb: disnake.Embed = getattr(embed, emb_style)
    emb.clear_fields()
    for chunk in chunks:
        emb_c = emb.copy()
        for field in chunk:
            emb_c.add_field(name=field.name, value=field.value, inline=field.inline)

        embeds.append(emb_c)

    return embeds if embeds else None
