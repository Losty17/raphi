from os import getenv

from discord import Intents
from dotenv import load_dotenv

from .raphi import Raphi

load_dotenv()

intents = Intents.all()

bot = Raphi("$", intents=intents, application_id=getenv(
    "APP_ID"), owner_id=getenv("OWNER_ID"))
