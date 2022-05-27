import discord
from discord import app_commands
from discord.ext import commands
from raphi.raphi import Raphi
from discord.ext.commands import Cog


class Events(Cog):
    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        owner = await guild.owner.create_dm()
        await owner.send(embed=None)


async def setup(bot: Raphi) -> None:
    await bot.add_cog(Events(bot))
