import discord
from discord.ext import commands
from utils.embed import neko_img_text
from random import choice

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pezinho', 'pé', 'pe', 'foot'])
    @commands.is_nsfw()
    async def feet(self, ctx):
        pepe = choice(('feet', 'erofeet'))
        return await ctx.send(embed=neko_img_text(pepe))

    @commands.command(aliases=['softporn', 'pornoleve', 'lewd'])
    @commands.is_nsfw()
    async def ero(self, ctx):
        pepe = choice(('erokemo', 'nsfw_avatar', 'eron', 'ero', 'erok', 'eroyuri'))
        return await ctx.send(embed=neko_img_text(pepe))

    @commands.command(aliases=['hentai', 'porno', 'nsfw'])
    @commands.is_nsfw()
    async def porn(self, ctx):
        pepe = choice(('yuri', 'trap', 'lewdkemo', 'lewd', 'blowjob', 'solo', 'cum', 'hentai', 'tits', 'pussy', 'lewd'))
        return await ctx.send(embed=neko_img_text(pepe))
    
    @commands.command(aliases=['hentaigif', 'hgif'])
    @commands.is_nsfw()
    async def lewdgif(self, ctx):
        pepe = choice(('classic', 'random_hentai_gif','boobs', 'spank', 'kuni', 'pwankg', 'anal', 'nsfw_neko_gif', 'les', 'solog', 'feetg'))
        return await ctx.send(embed=neko_img_text(pepe))

def setup(bot):
    bot.add_cog(Nsfw(bot))