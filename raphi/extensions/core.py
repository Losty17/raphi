from os import getenv
import discord
from discord import Interaction, app_commands
from discord.ext import commands
from raphi.raphi import Raphi
from ..utils.checks import is_owner


class Core(commands.Cog):
    dev = app_commands.Group(
        name="dev",
        description="Developer commands",
        guild_ids=[
            int(getenv("TAVERN")),
            int(getenv("UDYR")),
            int(getenv("KODY")),
        ]
    )

    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                name="cantigas de ninar",
                type=discord.ActivityType.listening
            )
        )
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')

    @dev.command()
    @app_commands.describe(extension="Extension to be loaded")
    @is_owner()
    async def load(self, interaction: Interaction, *, extension: str):
        """ Load an extension """
        module = extension if extension.startswith(
            '.extensions') else f'.extensions.{extension}'

        fqn = f'{self.bot.package}{module}'

        try:
            print(f"Loading extension {fqn}...", end=" ")
            await self.bot.load_extension(module, package=self.bot.package)
            print("Ok!")
            await self.bot.sync()
        except commands.ExtensionError:
            await interaction.response.send_message(
                f"Não foi possível carregar o módulo `{fqn}`",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(f'`{fqn}` foi carregado com sucesso', ephemeral=True)

    @dev.command()
    @is_owner()
    async def unload(self, interaction: Interaction, *, extension: str):
        """ Unload an extension """
        module = extension if extension.startswith(
            '.extensions') else f'.extensions.{extension}'

        fqn = f'{self.bot.package}{module}'

        try:
            print(f"Unloading extension {fqn}...", end=" ")
            await self.bot.unload_extension(module, package=self.bot.package)
            print("Ok!")
            await self.bot.sync()
        except commands.ExtensionError:
            await interaction.response.send_message(
                f"Não foi possível descarregar o módulo `{fqn}`",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(f'`{fqn}` foi descarregado com sucesso', ephemeral=True)

    @dev.command()
    @is_owner()
    async def reload(self, interaction: Interaction, *, extension: str):
        """ Reload an extension """
        module = extension if extension.startswith(
            '.extensions') else f'.extensions.{extension}'

        fqn = f'{self.bot.package}{module}'
        try:
            print(f"Reloading extension {fqn}...", end=" ")
            await self.bot.reload_extension(module, package=self.bot.package)
            print("Ok!")
            await self.bot.sync()
        except commands.ExtensionError:
            await interaction.response.send_message(
                f"Não foi possível recarregar o módulo `{fqn}`",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(f'`{fqn}` foi recarregado com sucesso', ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Core(bot))
