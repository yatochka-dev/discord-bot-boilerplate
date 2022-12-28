### Extensions
This folder contains all the extensions for the bot. Each extension is a separate file.
In extension files, you can add commands, events, tasks and cogs to your bot.

**!!!NEVER WORK WITH DATABASE FROM YOUR COG, USE SERVICES(app.services folder)!!!**

### Creating a cog
To create a cog, you need to create a file in the cogs' directory. The
file name should be the name of the cog you want to create. For example, if
you want to create an extension called `Events`, you should create a file
called `events.py` in the cogs' directory.

Terminology
Extension - File in cogs directory, extension can be added to your bot 
through the `load_extension` method. Can contain commands, events and tasks, 
(and more than one cog).

[Disnake docs for extensions](https://docs.disnake.dev/en/latest/ext/commands/extensions.html)
<br /><br />
Cog - class that inherits from disnake.ext.commands.Cog
<br /><br />
[Disnake docs for cogs](https://docs.disnake.dev/en/latest/ext/commands/cogs.html)
<br /><br /><br /><br />
`cogs` folder called "cogs" and not "extensions" because it's more common
terminology for python bots.

```python
# app\cogs\<EXTENSION_NAME>.py

from app import Bot
from disnake.ext.commands import Cog, slash_command

# Create a class that inherits from the Cog class
class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Create a method that will be called when the bot is ready
    @Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")

    # Create a method that will be called when a message is sent
    @Cog.listener()
    async def on_message(self, message):
        print(f"{message.author}: {message.content}")
    
    # Create a slash command
    @slash_command()
    async def ping(self, inter):
        await inter.response.send_message("Pong!")

# Add the cog to the bot
def setup(bot: Bot):
    bot.add_cog(Events(bot))
```

Loading cogs
------------
You don't need to load cogs by yourself, this template does it for you.
(You can edit main.py:load_cogs function to change this behavior)






