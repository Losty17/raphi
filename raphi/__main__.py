from os import getenv

from discord import Intents
from dotenv import load_dotenv

from .raphi import Raphi
from . import bot

load_dotenv()


bot.run(getenv("BOT_TOKEN"))
