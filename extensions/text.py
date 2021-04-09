import discord, time, os, asyncio
from discord.ext import commands
from random import choice, randint

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words_file = open(os.path.join('media', 'words.txt'), "r")
        self.words = self.words_file.readlines()
        self.words_file.close()

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        mesgedit = await ctx.reply('Ping?')
        before = time.monotonic()
        await mesgedit.edit(content=f"Pong!")
        ping = (time.monotonic() - before) * 1000
        await mesgedit.edit(content=f"Pong! Minha latência é de `{int(ping)}ms`, a latência da API é de `{int(self.bot.latency * 1000)}ms`")

    @commands.command(aliases=['flip', 'coin', 'flipcoin'])
    async def moeda(self, ctx):
        coin = ['Cara!', 'Coroa!']
        pau = choice(coin)
        await ctx.reply(f'`{pau}`')

    @commands.command(pass_context = True, aliases=['say'])
    async def diga(self, ctx, *, args : str = None):
        if args == None: return
        if args.lower() == 'pindamonhangaba':
            await ctx.reply('Achou que eu ia falar? bobinho')
        else:
            await ctx.message.delete()
            return await ctx.send(args)

    @commands.command(aliases=['invert'])
    async def inverter(self, ctx, *, text: str = None):
        if text is not None:
            to_reverse = text
            await ctx.reply(str(to_reverse)[::-1])
        else:
            return

    @commands.command(aliases=['choice', 'chose', 'pick', 'choose'])
    async def escolha(self, ctx, *args):
        if args:
            return await ctx.reply(choice(args))

    @commands.command(aliases=['roll','dice','rolldice'])
    async def role(self, ctx, *args):
        if not args:
            return await ctx.send('Qual deveria ser o número para rolar?')
        roll = ''.join(args)
        
        async with ctx.typing():
            if 'd' in roll:
                try:
                    dice, faces = roll.split('d')
                    nums_str = []
                    nums_int = []
                    for i in range(int(dice)):
                        result = randint(1, int(faces))
                        nums_int.append(result)
                        nums_str.append(str(result))
                    final_result = sum(nums_int)
                    partial = ' + '.join(nums_str)
                    msg = await ctx.reply('Rolando...')
                    await asyncio.sleep(1)
                    return await msg.edit(content=f'{ctx.author.mention}, `{partial}` = `{str(final_result)}` 🎲')
                except:
                    return await msg.edit(content='Não consegui efetuar a operação, tente novamente')
            else:
                try:
                    msg = await ctx.reply('Rolando...')
                    time.sleep(2)
                    dice = randint(1, int(roll))
                    return await msg.edit(content=f'{ctx.author.mention}, `{dice}` 🎲')
                except:
                    return await msg.edit(content='Não consegui efetuar a operação, tente novamente')
    
    @commands.command(aliases=['autor'])
    async def author(self, ctx):
        await ctx.reply('Siga meu criador nas redes sociais!\n- https://twitter.com/yts0l\n- https://discord.gg/AWB9d2hjC6\n- https://anilist.co/user/Loooosty/')

    @commands.command(aliases=['lel', 'lil', 'lul'])
    async def lal(self, ctx):
        await ctx.reply('LAL')

    @commands.command(pass_context=True,aliases=['8ball'])
    async def filo(self, ctx, question : str = None):
        if not question: return
        else: 
            ans = [
                'Sim',
                'Não',
                'Talvez',
                'Não sei',
                'Concordo',
                'Com certeza',
                'Obviamente não',
                'Não posso negar',
                'Não posso afirmar',
                '(Censurado pelo governo)',
                'Com toda certeza que sim',
                'Para de encher o saco e vai capinar um lote, não tô aqui pra te responder'
            ]
            msg = choice(ans)
        
        # Finding the webhook
        filo = discord.utils.get(await ctx.channel.webhooks(), name='Filo-chan')
        if not filo:
            with open(os.path.join("media", "filo.png"), 'rb') as avatar:
                filo = await ctx.channel.create_webhook(name='Filo-chan',avatar=avatar.read())
        
        # Sending the message
        return await filo.send(content=msg)

    @commands.command()
    async def proibir(self, ctx, *, proibicao : str = None):
        # Setting the prohibition
        if proibicao: msg = f'Hoje o governo proibiu {proibicao}'
        else: msg = f'Hoje o governo proibiu {choice(self.words).lower()}'
        
        # Finding the webhook
        proibiubot = discord.utils.get(await ctx.channel.webhooks(), name='ProibiuBOT')
        if not proibiubot:
            with open(os.path.join("media", "proibiu.jpg"), 'rb') as avatar:
                proibiubot = await ctx.channel.create_webhook(name='ProibiuBOT',avatar=avatar.read())
        
        # Sending the message
        return await proibiubot.send(content=msg)

    @commands.command(name='effort', aliases=['eff', 'e'])
    async def effort_calculator(self, ctx, quality : str = None, effort : int = None):
        """
        É mole?
        """
        if quality is None or effort is None:
            return await ctx.reply('`r!effort <qualidade atual> <effort atual>`')
        if quality in 'damaged 0 d':
            final_effort = effort*(1.9**4)
        if quality in 'poor 1 p':
            final_effort = effort*(1.9**3)
        if quality in 'good 2 g':
            final_effort = effort*(1.9**2)
        if quality in 'excellent 3 e':
            final_effort = effort*1.9
        if quality in 'mint 4 m':
            return await ctx.reply('Esse já é o effort máximo para essa carta.')

        return await ctx.reply(f'O effort dessa carta em mint será aproximadamente `{int(final_effort)}`')

    @commands.command(name='style', aliases=['sty', 's'])
    async def style_calculator(self, ctx, base_value : int = None, effort : int = None):
        """
        É mole?
        """
        if base_value == None:
            return await ctx.reply('r!style <base value> (effort atual)')
        
        frame_or_mystic = int((base_value*0.75)+(base_value*0.75*0.25))
        common_dye = int((base_value*0.2)+(base_value*0.2*0.25))
        frame_and_mystic = int((base_value*1.5)+(base_value*1.5*0.25))

        if effort is not None:
            return await ctx.reply(f'''Effort adicionado com `frame` ou `mystic dye`: `{frame_or_mystic}`, para um total de `{frame_or_mystic+effort}`.
            Effort adicionado com `dye comum`: `{common_dye}`, para um total de `{common_dye+effort}`.
            Effort adicionado com `frame` e `mystic dye`: `{frame_and_mystic}`, para um total de `{frame_and_mystic+effort}`.''')
        else:
            return await ctx.reply(f'''Effort adicionado com `frame` ou `mystic dye`: `{frame_or_mystic}`.
            Effort adicionado com `dye comum`: `{common_dye}.`
            Effort adicionado com `frame` e `mystic dye`: `{frame_and_mystic}`.''')

    @commands.command(name='deinjurer', aliases=['d', 'di'])
    async def card_deinjurer(self, ctx, effort : int = None):
        if effort == None:
            return await ctx.reply('r!deinjurer <effort atual>')

        return await ctx.reply(f'O effort normal dessa carta é aproximadamente `{effort*5}`')

def setup(bot):
    bot.add_cog(Text(bot))

if __name__ == "__main__":
    pass