from typing import SupportsInt, Union

import disnake
from disnake import ApplicationCommandInteraction

# CommandInteraction type is used for slash commands
#
# Example:
# async def <SLASH_COMMAND_NAME>(self, interaction: CommandInteraction) -> None:
CommandInteraction = ApplicationCommandInteraction

# ... you can add your custom types and enums here


DiscordUtilizer = disnake.ClientUser | disnake.Member | disnake.User
SupportsIntCast = Union[SupportsInt, str, bytes, bytearray]