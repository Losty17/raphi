import discord, os, asyncio
from discord.ext import commands
# from pymongo import MongoClient
from pytube import YouTube
import requests
from riotwatcher import LolWatcher
from dotenv import load_dotenv

load_dotenv()
watcher = LolWatcher(os.getenv('LOL_TOKEN'))
lol_region = 'br1'


# avatar_collection = db.get_collection('avatar_collection')
# collection = db.get_collection('guild_collection')

class Tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def __ignore(self):
        return
        # @commands.command(name='profile',aliases=['perfil'])
        # async def user_profile(self, ctx, member : discord.Member = None):
        #     if member is None:
        #         try:
        #             avatar_collection.insert_one({
        #                 '_id'     : ctx.author.id,
        #                 'name'    : ctx.author.name,
        #                 'bio'     : 'Olá, eu sou uma bio! Use o comando `bio` para me alterar!',
        #                 'backdrop': 'https://images5.alphacoders.com/100/thumb-1920-1004852.jpg',
        #                 'color'   : [255,200,255],
        #                 'rep'     : 0
        #             })
        #         except:
        #             pass
        #         member = ctx.author
        #     get = avatar_collection.find_one({'_id': member.id})
        #     if get is None:
        #         return await ctx.send('Usuário não encontrado')
            
        #     name = get['name']
        #     rep = get['rep']
        #     color = get['color']
        #     image = get['backdrop']
        #     bio = get['bio']
        #     status = lambda s : 'online' if s == discord.Status.online else ('ausente' if s == discord.Status.idle else ('ocupado' if s == discord.Status.dnd else 'offline'))

        #     # Set embed for profile (temp)
        #     emb = discord.Embed(
        #         title=f'~ {member.display_name}  —  {rep} rep! <:love:592371673647415299>',
        #         description=bio,
        #         color=discord.Colour.from_rgb(color[0],color[1],color[2])
        #     )
        #     emb.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
        #     emb.set_image(url=image)
        #     emb.set_thumbnail(url=member.avatar_url)
        #     emb.set_footer(text=f'{member.name} está {status(member.status)} agora!')
        #     return await ctx.send(embed=emb)
        
        # @commands.command(name='bio',aliases=['biografia','sobremim','aboutme'])
        # async def bio(self, ctx, *, bio : str = None):
        #     if bio is None:
        #         return await ctx.send('Uso: `bio <bio>. Exemplo: bio Eu sou um cara bacana!`')
        #     try:
        #         avatar_collection.update_one({'_id':ctx.author.id}, {'$set': {'bio': bio}})
        #     except:
        #         pass
        #     return await ctx.send('Sua biografia foi atualizada!')

        # @commands.command(name='background',aliases=['bg','papeldeparede'])
        # async def bg(self, ctx, *, backdrop : str = None):
        #     if backdrop is None:
        #         return await ctx.send('Uso: `background <link>; Exemplo: background http://site.com/imagemlegal.`')
        #     try:
        #         avatar_collection.update_one({'_id':ctx.author.id}, {'$set': {'backdrop': backdrop}})
        #     except:
        #         pass
        #     return await ctx.send('A imagem do seu perfil foi atualizada!')

        # @commands.command(name='color', aliases=['cor'])
        # async def color(self, ctx, *, rgb : str = None):
            # if rgb == None:
            #     return await ctx.send('Uso: `cor <R G B>; Exemplo: cor 200 60 200.`')
            # rgb = rgb.split()
            # try:
            #     _r = int(rgb[0])
            #     _g = int(rgb[1])
            #     _b = int(rgb[2])
            # except:
            #     return

            # r = lambda r : _r if _r < 256 and _r > -1 else 255
            # g = lambda g : _g if _g < 256 and _g > -1 else 255
            # b = lambda b : _b if _b < 256 and _b > -1 else 255
            # avatar_collection.update_one({'_id': ctx.author.id}, {'$set': {'color': (r(_r), g(_g), b(_b))}})
            # return await ctx.send('A cor do seu perfil foi atualizada!')

    @commands.command()
    async def yt(self, ctx, link : str):
        vd = YouTube(link)
        title = vd.title
        vd.streams.first().download(os.path.join('.','tmp'), 'vid')
        try:
            await ctx.send(file=discord.File(os.path.join('.','tmp','vid.mp4'), f'{title}.mp4'))
        except:
            await ctx.send(f'O vídeo `{title}` é muito grande para ser enviado.')
        
        return os.remove(os.path.join('.','tmp','vid.mp4'))

    @commands.command(aliases=['lolstats', 'leaguestatus'])
    async def lol(self, ctx, user : str = None):
        if not user: return

        # Get summoner by name
        summoner = watcher.summoner.by_name(lol_region, user)
        
        # Get ranked status for summoner
        ranked_status = watcher.league.by_summoner(lol_region, summoner['id'])
        
        # Masteries for the summoner
        mastery = watcher.champion_mastery.by_summoner(lol_region, summoner['id'])[0]
        
        # Here we get the full champion list for the actual version from data dragon
        champ_list = watcher.data_dragon.champions(watcher.data_dragon.versions_for_region(lol_region)['n']['champion'])['data']
        
        # We run through the list to find the top mastery champion
        for champion in champ_list:
            if champ_list[champion]['key'] == str(mastery['championId']):
                main = champ_list[champion]

        ##########################################################
        emb = discord.Embed(
            title=f"{summoner['name']}   -   lvl. {summoner['summonerLevel']}",
            description=f"League stats for this summoner below:"
        )
        emb.add_field(name=main['name'], value=f'Mastery level: **{mastery["championLevel"]}**', inline=True)
        emb.set_image(url=f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{main["name"]}_0.jpg')
        emb.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/10.8.1/img/profileicon/{summoner['profileIconId']}.png")
        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Tests(bot))

if __name__ == "__main__":
    me = watcher.summoner.by_name(lol_region, 'Styles Stilinski')
    ranked_status = watcher.league.by_summoner(lol_region, me['id'])
    me_mastery = watcher.champion_mastery.by_summoner(lol_region, me['id'])[0]
    ###
    champ_list = watcher.data_dragon.champions(watcher.data_dragon.versions_for_region(lol_region)['n']['champion'])['data']
    for champion in champ_list:
        if champ_list[champion]['key'] == str(me_mastery['championId']):
            main = champ_list[champion]

    print(me_mastery)
