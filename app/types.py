from typing import SupportsInt, Union

import disnake
from disnake import ApplicationCommandInteraction

# CommandInteraction type is used for slash commands
#
# Example:
# async def <SLASH_CMD_NAME>(self, interaction: CommandInteraction) -> None:
CommandInteraction = ApplicationCommandInteraction

DiscordUtilizer = disnake.ClientUser | disnake.Member | disnake.User

SupportsIntCast = Union[SupportsInt, str, bytes, bytearray]
# ... you can add your custom types and enums here
