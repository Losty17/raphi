import discord, time, random, os, asyncio
from nekos import textcat, cat
from discord.ext import commands
from utils.embed import neko_img_text
from utils.imageman1 import image1test
from imgurpython import ImgurClient
from dotenv import load_dotenv
load_dotenv()
COR = 0xF26DDC

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Imgur connection
        self.imgurclient = ImgurClient(os.getenv('IMGUR_TOKEN'), os.getenv('IMGUR_SECRET'))

        self.COR = 0xF26DDC

    def is_empty(self, anything):
        if anything:
            return False
        else:
            return True

    @commands.command(pass_context=True, aliases=['icon'])
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            if ctx.channel.is_nsfw():
                embed = neko_img_text('nsfw_avatar')
            else:
                embed = neko_img_text('avatar')
        else:
            embed = discord.Embed(colour=0xF26DDC)
            embed.set_image(url=member.avatar_url)
        return await ctx.reply(embed=embed)

    @commands.command(aliases=['gato'])
    async def cat(self, ctx):
        embed = discord.Embed(colour = COR)
        embed.set_image(url=cat())
        await ctx.reply(embed=embed)
    
    @commands.command()
    async def neko(self, ctx):
        title = random.choice(('An enemy「猫」appears', 'A wild neko appears!', 'A wild 猫 appears', 'This must be work of an enemy 「猫」'))
        return await ctx.reply(embed=neko_img_text('ngif', title, textcat()))

    @commands.command(aliases=['ganso'])
    async def goose(self, ctx):
        return await ctx.reply(embed=neko_img_text('goose', textcat()))

    @commands.command(aliases=['dog', 'cão', 'cachorro'])
    async def woof(self, ctx):
        return await ctx.reply(embed=neko_img_text('woof', textcat()))

    @commands.command(aliases=['lagarto', 'largato', 'lagartixa'])
    async def lizard(self, ctx):
        return await ctx.reply(embed=neko_img_text('lizard', textcat()))

    @commands.command(aliases=['tapa'])
    async def slap(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} bateu em {member.name}'
        return await ctx.reply(embed=neko_img_text('slap', title, textcat()))
    
    @commands.command(aliases=['abraçar'])
    async def hug(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} abraçou {member.name}'
        return await ctx.reply(embed=neko_img_text('hug', title, textcat()))

    @commands.command(aliases=['carinho'])
    async def cuddle(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} faz carinho em {member.name}'
        return await ctx.reply(embed=neko_img_text('cuddle', title, textcat()))
    
    @commands.command(aliases=['acariciar'])
    async def pat(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} acariciou {member.name}'
        return await ctx.reply(embed=neko_img_text('pat', title, textcat()))

    @commands.command(aliases=['cutucar'])
    async def poke(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} cutucou {member.name}'
        return await ctx.reply(embed=neko_img_text('poke', title, textcat()))

    @commands.command(aliases=['idiota'])
    async def baka(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'B-baka {member.name}!'
        return await ctx.reply(embed=neko_img_text('baka', title, textcat()))

    @commands.command(aliases=['beijar'])
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        elif member == self.bot.user:
            embed = discord.Embed(colour=self.COR, title="o///o")
            embed.set_image(url='https://i.pinimg.com/originals/50/03/9d/50039d415a087ca8c213eb1337c82ca5.jpg')
            return await ctx.reply(embed=embed)
        title=f'{ctx.author.name} beijou {member.name}'
        return await ctx.reply(embed=neko_img_text('kiss', title, textcat()))

    @commands.command(aliases=['alimentar'])
    async def feed(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} alimentou {member.name}'
        return await ctx.reply(embed=neko_img_text('feed', title, textcat()))

    @commands.command(aliases=['cocegas'])
    async def tickle(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} fez cócegas em {member.name}'
        return await ctx.reply(embed=neko_img_text('tickle', title, textcat()))
    
    @commands.command()
    async def smug(self, ctx):
        return await ctx.reply(embed=neko_img_text('smug'))

    @commands.command(aliases=['pic', 'foto', 'random'])
    async def randompic(self, ctx):
        return await ctx.reply(embed=neko_img_text(random.choice(('fox_girl', 'gasm', 'kemonomimi'))))

    @commands.command()
    async def imagemcagada(self, ctx, image, *, text : str = 'Sua mãe aquela puta'):
        img = image1test(f'{image}', f'{text}')
        file = discord.File('./media/img.png', filename='yeaforsure.png')
        await ctx.reply(file=file)
        await ctx.message.delete()
        await asyncio.sleep(5)
        return os.remove('./media/img.png')

    @commands.command()
    async def meme(self, ctx):
        items = self.imgurclient.get_album_images('Kz30J')
        img = random.choice(items).link
        await ctx.reply(img)

    @commands.command(aliases=['jjba'])
    async def jojo(self, ctx):
        rand = random.randint(0, 113)
        album = self.imgurclient.get_album_images('FAmyQ')
        img = album[rand].link
        await ctx.reply(img)

    @commands.command(aliases=['jojoshitpost','jjbameme'])
    async def jojomeme(self, ctx):
        rand = random.randint(0, 59)  # 60 results generated per page
        items = self.imgurclient.subreddit_gallery(subreddit='ShitPostCrusaders', sort='time', window='week', page=0)
        img = items[rand].link
        await ctx.reply(img)

    @commands.command()
    async def imgur(self, ctx, *args):
        rand = random.randint(0, 59)  # 60 results generated per page
        if is_empty(args):
            items = self.imgurclient.gallery(section='hot', sort='viral', page=0, window='day', show_viral=True)
        else:
            query = ' '.join(args)
            items = self.imgurclient.gallery_search(q=query, advanced=None, sort='viral', window='all', page=0)
        img = items[rand].link
        await ctx.reply(img)

def setup(bot):
    bot.add_cog(Images(bot))