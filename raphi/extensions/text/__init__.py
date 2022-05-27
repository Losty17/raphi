import os
from random import choice
from time import monotonic

from discord import Interaction, app_commands
from discord.ext import commands
from raphi.raphi import Raphi
from raphi.views.link import AuthorLinks, Counter, LinkButton


class Text(commands.Cog):
    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

    @app_commands.command()
    async def ping(self, interaction: Interaction):
        """ Check the bot's latency """
        await interaction.response.send_message("Ping?")
        before = monotonic()
        await interaction.edit_original_message(content="Pong!")
        ping = (monotonic() - before) * 1000
        await interaction.edit_original_message(
            content=f"Pong! Minha latência é de `{int(ping)}ms`, a latência da API é de `{int(self.bot.latency * 1000)}ms`"
        )

    @app_commands.command()
    async def coin(self, interaction: Interaction):
        """ Toss a coin. Good Luck. """
        await interaction.response.send_message(f'`{choice(["Cara", "Coroa"])}!`')

    @app_commands.command()
    @app_commands.describe(message="The message you want Raphi to say")
    async def say(self, interaction: Interaction, *, message: str):
        """ Don't worry... They will know that you said this. """
        await interaction.response.send_message(message)

    @app_commands.command()
    @app_commands.describe(text="The text you wish to invert")
    async def invert(self, interaction: Interaction, *, text: str):
        """ Inverting is always good... isn't it? """
        await interaction.response.send_message(text[::-1])

    @app_commands.command()
    @app_commands.describe(items="The list of things you wish Raphi to choose from, separated by comma.")
    async def choose(self, interaction: Interaction, *, items: str):
        """ Raphi is very good at making choices. But you do need to be more specific. """
        await interaction.response.send_message(f'{choice(items.split(",")).strip()}')

    @app_commands.command()
    @app_commands.describe(question="The question Raphi will ask to Filo")
    async def filo(self, interaction: Interaction, *, question: str):
        """ Filo is the oracle of all knowledge, but only answers to Raphi """
        await interaction.response.send_message(f'Filo, {question}{"?" if not question.endswith("?") else ""}')

        with open(os.path.join(self.bot.root_dir, 'res', 'filo.png'), 'rb') as avatar:
            webhook = await interaction.channel.create_webhook(name="Filo", avatar=avatar.read())

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
        await webhook.send(choice(ans))
        await webhook.delete()

    @app_commands.command()
    async def author(self, interaction: Interaction):
        """ Raphi's creator social media """
        author_info = {
            "Github": "https://kappke.tech/github",
            "Twitter": "https://twitter.com/yts0l",
            # "Instagram": "https://instagram.com/vini.kkkappke",
            "Linkedin": "https://www.linkedin.com/in/viniciuskappke/",
            "Discord": "Losty#1572",
        }

        await interaction.response.send_message(view=AuthorLinks(author_info))

    @app_commands.command()
    async def github(self, interaction: Interaction):
        """ Raphi's Github Repository """
        await interaction.response.send_message(view=LinkButton("Github Repository", "https://github.com/losty17/raphi"))

    @app_commands.command()
    async def counter(self, interaction: Interaction):
        await interaction.response.send_message("teste", view=Counter())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Text(bot))
