from time import monotonic
from random import choice
from typing import Optional

import discord
from discord import Interaction, app_commands
from discord.ext import commands


class Text(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction) -> None:
        """ Check the bot's latency """
        await interaction.response.send_message("Ping?")
        before = monotonic()
        await interaction.edit_original_message(content="Pong!")
        ping = (monotonic() - before) * 1000
        await interaction.edit_original_message(
            content=f"Pong! Minha latência é de `{int(ping)}ms`, a latência da API é de `{int(self.bot.latency * 1000)}ms`"
        )

    @app_commands.command()
    async def coin(self, interaction: discord.Interaction) -> None:
        """ Toss a coin. Good Luck. """
        await interaction.response.send_message(f'`{choice(["Cara", "Coroa"])}!`')

    @app_commands.command()
    @app_commands.describe(message="The message you want Raphi to say")
    async def say(self, interaction: discord.Interaction, *, message: str) -> None:
        """ Don't worry... They will know that you said this. """
        await interaction.response.send_message(message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Text(bot))
