from os import getenv

from discord import Intents
from dotenv import load_dotenv

from .raphi import Raphi

load_dotenv()

intents = Intents.default()

bot = Raphi("", intents=intents, application_id=getenv("APP_ID"))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(getenv("BOT_TOKEN"))
