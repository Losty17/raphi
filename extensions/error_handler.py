# # # # # # # # # # # # # # # # # # # # # # # # #
#                                               #
#   Error Handling is always good! Change it    #
#   for your own bot responses when a command   #
#   throws an error.                            #
#                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # 
import discord
from discord.ext import commands
from datetime import timedelta
from math import ceil

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return await ctx.send('É necessário estar em um servidor para utilizar meus comandos.')
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send('Este comando está desabilitado neste servidor.')
        elif isinstance(error, commands.errors.NSFWChannelRequired):
            return await ctx.send(f'Você so pode usar este comando em um canal NSFW.')
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send('Você não tem permissão para usar este comando.')
        elif isinstance(error, commands.NotOwner):
            return await ctx.send('Somente o dono do bot pode usar este comando.')
        elif isinstance(error, commands.CommandNotFound):
            return  
            #await ctx.send('Desculpe, não consegui encontrar o comando solicitado...')
        elif isinstance(error, commands.errors.CommandInvokeError):
            #await ctx.send(f'Ops, acabei encontrando um erro!\n<@!207947146371006464>```{error}```')
            return
        elif isinstance(error, commands.errors.CommandOnCooldown):
            seconds = timedelta(0, ceil(error.retry_after))
            return await ctx.send(f'Você poderá usar esse comando novamente em {seconds}!')

def setup(bot):
    bot.add_cog(Error(bot))