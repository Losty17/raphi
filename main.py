import discord, logging
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from sys import exit
from datetime import datetime
try:
    from extensions import *
except ImportError as error:
    exit(f'ERROR: Missing dependency: {error}')

# Get bot token
load_dotenv()
TOKEN = getenv('BOT_TOKEN')

# List of extensions to load
extensions = [
    'extensions.core',
    'extensions.adm',
    'extensions.text',
    'extensions.dev',
    'extensions.error_handler',
    'extensions.images',
    'extensions.nsfw',
    'extensions.tests'
]

# Bot creation
bot = commands.Bot(command_prefix=['r','r!'],help_command=None,case_insensitive=True,owner_id=int(getenv('BOT_OWNER')))      

# Function for loading all modules
def load_modules():
    for e in extensions:
        try:
            print(f"Carregando módulo: {e}...")
            bot.load_extension(e)
        except Exception:
            print(f"Não foi possível carregar o módulo {e}")

# Letta run the boat
if __name__ == "__main__":
    load_modules()
    try:
        bot.run(TOKEN)
    except KeyError:
        print('Váriavel de ambiente não encontrada.')