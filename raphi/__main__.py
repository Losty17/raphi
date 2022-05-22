from os import getenv

import discord
from discord import Intents
from dotenv import load_dotenv

from .raphi import Raphi

load_dotenv()

intents = Intents.default()

bot = Raphi("", intents=intents, application_id=getenv("APP_ID"))


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            name="cantigas de ninar",
            type=discord.ActivityType.listening
        )
    )
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(getenv("BOT_TOKEN"))
