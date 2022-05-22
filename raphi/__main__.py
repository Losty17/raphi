from os import getenv

import discord
from discord import Intents
from dotenv import load_dotenv

from .raphi import Raphi

load_dotenv()

intents = Intents.default()

bot = Raphi("", intents=intents, application_id=getenv("APP_ID"))

bot.run(getenv("BOT_TOKEN"))
