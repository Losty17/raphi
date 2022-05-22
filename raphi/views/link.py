from typing import Dict, Optional

import discord
import discord.ui as ui
import validators
from discord.ui import Button, View


class LinkButton(View):
    def __init__(self, label: str, url: str, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)

        if not validators.url(url):
            raise Exception(message="The provided URL is not valid.")

        self.add_item(Button(label=label, url=url))


class AuthorLinks(View):
    def __init__(self, info: Dict[str, str], *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)

        for l in info:
            if not validators.url(info[l]):
                self.add_item(Button(label=f'{l}: {info[l]}', disabled=True))
            else:
                self.add_item(Button(label=l, url=info[l]))


class Counter(View):
    @ui.button(label='0', style=discord.ButtonStyle.red)
    async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
        number = int(button.label) if button.label else 0

        if number + 1 >= 5:
            button.style = discord.ButtonStyle.green
            button.disabled = True

        button.label = str(number + 1)

        await interaction.response.edit_message(view=self)
