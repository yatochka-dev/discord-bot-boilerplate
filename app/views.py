import disnake
from disnake import MessageInteraction
from disnake.ui import Item, View

from app import Bot, Embed
from app.exceptions import BotException
from app.types import DiscordUtilizer


class BaseView(View):

    def __init__(self, bot: Bot, user: DiscordUtilizer, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.bot = bot

    async def interaction_check(self, interaction: MessageInteraction):
        """

            Exception codes:
                1 - Forbidden
                2 - Not found
        """
        BotException.assert_value(
            not interaction.user.bot, error_code=403, message="This interaction can be used by bots"
        )

        BotException.assert_value(
            interaction.user.id == self.user.id, error_code=403, message="You can't use this interaction"
        )
        return True

    async def on_error(self, error: Exception, item: Item, interaction: MessageInteraction) -> None:
        if isinstance(error, BotException):

            await interaction.send(embed=error.to_embed(user=interaction.user), ephemeral=True)
        else:
            await interaction.response.send_message("An unknown error occured.", ephemeral=True)
            raise error


class PaginationView(BaseView):

    def __init__(
            self,
            bot: Bot,
            user: DiscordUtilizer,
            pages: list[Embed],
            **kwargs,
    ):
        super().__init__(bot, user, **kwargs)
        self.pages = pages
        self.current_page = 0

        self._update_state()

    def _update_state(self) -> None:
        if len(self.pages) == 1:
            self.clear_items()
            self.stop()

        self.first_page.disabled = self.prev_page.disabled = self.current_page == 0
        self.last_page.disabled = self.next_page.disabled = self.current_page == len(self.pages) - 1

    @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.blurple)
    async def first_page(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.current_page = 0
        self._update_state()

        await inter.response.edit_message(embed=self.pages[self.current_page], view=self)

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.secondary)
    async def prev_page(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.current_page -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.pages[self.current_page], view=self)

    @disnake.ui.button(emoji="🗑️", style=disnake.ButtonStyle.red, custom_id="delete")
    async def remove(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.secondary)
    async def next_page(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.current_page += 1
        self._update_state()

        await inter.response.edit_message(embed=self.pages[self.current_page], view=self)

    @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.blurple)
    async def last_page(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.current_page = len(self.pages) - 1
        self._update_state()

        await inter.response.edit_message(embed=self.pages[self.current_page], view=self)
