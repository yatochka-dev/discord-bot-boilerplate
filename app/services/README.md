### Services
Services are classes that are used mostly to manipulate database
records. They are used to create, update, delete, and retrieve
records from the database. They are also used to perform other 
tasks such as sending emails(for example), or performing 
calculations(Great example).

Services are used to keep your controllers clean and to keep your
models clean. They are also used to keep your code DRY(Don't repeat yourself).

### Creating a service
To create a service, you need to create a file in the services' directory. The 
file name should be the name of the service you want to create. For example, if
you want to create a service called `UserService`, you should create a file
called `UserService.py` in the services' directory.

(You already have an example service called `GuildService` in the services')

```python
# app\services\GuildService.py

import disnake
from prisma import models

# Import the CogService class
# This class provides you access to the self.bot variable
# which is the bot instance that has the .prisma attribute
# which is the prisma client instance

from .index import AppService 


# Create a class that inherits from the CogService class
class GuildService(AppService):
    
    # Create a method that returns True if the guild is in the database
    # and False if it isn't
    async def is_guild_exists(self, guild_id: int) -> bool:
        self.bot.logger.debug(f"Checking if guild exists: {guild_id}")
        return (
            await self.bot.prisma.guild.find_first(where={"id": str(guild_id)})
            is not None
        )
    
    
    # Create a method that adds a guild to the database
    # This method returns the guild object
    async def add_guild(self, guild: disnake.Guild) -> models.Guild:
        self.bot.logger.debug(f"Adding guild: {guild.name} (ID: {guild.id})")
        return await self.bot.prisma.guild.create(data={"id": str(guild.id)})
    
    
    # Create a method that removes the guild from the database
    async def remove_guild(self, guild: disnake.Guild):
        self.bot.logger.debug(f"Removing guild: {guild.name} (ID: {guild.id})")
        return await self.bot.prisma.guild.delete(where={"id": str(guild.id)})

```

Using a service inside of a cog 
---------------

```python
# app\cogs\events.py
import os

from disnake.ext.commands import Cog

from app import Bot

# Import the GuildService class
from app.services.GuildService import GuildService


# Create a class that inherits from the Cog class
# and the GuildService class (Now you have access to the methods from the GuildService class)
class Events(Cog, GuildService):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener(
        "on_ready",
    )
    async def bot_is_ready(self):
        self.bot.logger.info(
            f"Logged in as {self.bot.user} (ID: {self.bot.user.id})"
        )
        self.bot.logger.info(
            f"Started bot in {os.getenv('STATE_NAME').title()} mode."
        )
        self.bot.logger.info("------")

        # Use the is_guild_exists method from the GuildService class
        for guild in self.bot.guilds:
            if not await self.exists_guild(guild.id):
                # Use the add_guild method from the GuildService class
                await self.add_guild(guild)
                self.bot.logger.info(
                    f"Added guild: {guild.name} (ID: {guild.id})"
                )
            else:
                self.bot.logger.info(
                    f"Guild already exists: {guild.name} (ID: {guild.id})"
                )

    @Cog.listener(
        "on_guild_join",
    )
    async def bot_joined_guild(self, guild):
        # Use the add_guild method from the GuildService class to add new 
        # guild when the bot joins a new guild 
        await self.add_guild(guild)
        self.bot.logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")

    @Cog.listener(
        "on_guild_remove",
    )
    async def bot_quit_guild(self, guild):
        # Use the remove_guild method from the GuildService class to remove
        # guild when the bot leaves a guild
        await self.remove_guild(guild)
        self.bot.logger.info(f"Left guild: {guild.name} (ID: {guild.id})")


def setup(bot: Bot):
    bot.add_cog(Events(bot))


```

Using service in the API 
---------------

```python

# app/apis/guilds.py

from fastapi import APIRouter, Depends

from app.services.GuildService import GuildService

router = APIRouter()


@router.get("/guilds/")
async def getGuilds(service: GuildService = Depends(GuildService)):
    return await service.get_all_guilds()


@router.get("/guilds/{guild_id}")
async def is_guild_exists(
        guild_id: int, service: GuildService = Depends(GuildService)
):
    return await service.exists_guild(guild_id)


```