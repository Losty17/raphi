import discord
from discord import app_commands
from discord.ext import commands
from raphi.raphi import Raphi


class Core(commands.Cog):
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Core(bot))
