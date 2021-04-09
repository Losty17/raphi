import discord, os, logging
from discord.ext import commands
from utils.embed import *
from random import choice

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Modules for bot config
        self.modules = [
            'text',
            'adm',
            'images',
            'music',
            'nsfw'
        ]
        self.m_string = ', '.join(self.modules)

    # Core Commands for Raphtalia
    @commands.command(aliases=['help'])
    async def ajuda(self, ctx):
        ajuda = embedajuda(ctx.author.mention)
        await ctx.reply(embed = ajuda)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('<@!824011589086347267>'):
            respostas = [
            'Fico pensando por que você está marcando um bot...',
            'Gostou do meu nome, é?',
            'Eu sou um robô, não adianta dar em cima de mim :p'
            ]
            await message.channel.send(choice(respostas))
        
        if 'lindo' in message.content.lower() or 'bonito' in message.content.lower():
            if not message.guild.id == 501807001324617748: return
            bezin = discord.utils.get(await message.channel.webhooks(), name='Bezin')
            if not bezin:
                with open(os.path.join("media", "bezin.png"), 'rb') as avatar:
                    bezin = await message.channel.create_webhook(name='Bezin',avatar=avatar.read())
            return await bezin.send(content='Eu sou Iindo!')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 592178925040435213:
            return
        prefix = 'r!'
        welcomeembed = embedwelcome(member, bot, prefix)
        await bot.get_channel(592179994193559573).send(member.mention, embed=welcomeembed)
        for r in member.guild.roles:
            if r.name == 'Newbie':
                return await member.add_roles(r)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Olá mundo! Eu sou {self.bot.user}')
        try:
            await self.bot.change_presence(activity=discord.Game('Precisa de ajuda? Diga r!ajuda'), status=discord.Status.idle)
        except:
            print('Não foi possível carregar as tarefas de segundo plano')

def setup(bot):
    bot.add_cog(Core(bot))