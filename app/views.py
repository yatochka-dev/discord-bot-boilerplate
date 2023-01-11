import disnake
from disnake import MessageInteraction
from disnake.ui import Item, View

from app import Bot, Embed
from app.types import DiscordUtilizer


class ViewDispatchException(Exception):

    def __init__(self, code: int):
        self.code = code


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
        if interaction.user.bot:
            raise ViewDispatchException(1)
        if interaction.user.id != self.user.id:
            raise ViewDispatchException(1)

        return True

    async def on_error(self, error: Exception, item: Item, interaction: MessageInteraction) -> None:
        if isinstance(error, ViewDispatchException):
            match error.code:
                case 1:
                    embed = Embed(
                        title="Forbidden",
                        description="You are not allowed to use this element.",
                        user=self.user,
                    ).error

                case 2:
                    embed = Embed(
                        title="Not found",
                        description="The element you are trying to use was not found.",
                        user=self.user,
                    ).error

                case _:
                    embed = Embed(
                        title="Error",
                        description="An unknown error occured.",
                        user=self.user,
                    ).error
            await interaction.send(embed=embed, ephemeral=True)
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
