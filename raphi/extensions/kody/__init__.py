import json
import os
from random import choice
from typing import Dict, List

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from raphi.extensions.kody.db.models.enums import NodeEnum
from raphi.raphi import Raphi
from .question import Question
from .views import QuestionUi

from .db import KodyDatabase


def check_permission():
    def predicate(interaction: Interaction) -> bool:
        return interaction.guild.id == 501807001324617748 and interaction.channel.id == 979441373046521937
    return app_commands.check(predicate)


class Kody(commands.Cog):
    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

        questions_path = os.path.join(
            self.bot.res_dir, 'kody', 'questions.json')

        with open(questions_path, 'rb') as file:
            self.questions: List[Dict] = json.loads(file.read())

    @app_commands.command(name="question")
    @app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.guild_id, i.user.id))
    async def _question_command(self, interaction: discord.Interaction):
        """ Responda uma perguntinha! """
        question = choice(self.questions)
        content = question['text']
        right_answer = question['answers']['right']
        answers = []
        for i in question['answers']:
            answers.append(question['answers'][i])

        question = Question.get_question(answers, right_answer, content)

        if question:
            await interaction.response.send_message(content=content, view=QuestionUi(question))

    @_question_command.error
    async def _on_question_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f'Você já respondeu uma pergunta, tente novamente em {int(round(error.retry_after, 0))}s', ephemeral=True)
            return

    @app_commands.command(name="testdb")
    async def _test_db(self, interaction: discord.Interaction):
        """ Testa o banco de dados """
        database = KodyDatabase()

        database.sync()

        database.create_user(interaction.user.id)

        user = database.get_user(interaction.user.id)

        for i in range(9):
            database.insert_question(
                "texto", NodeEnum.coding.name, "certo", "errado")

        quest = database.get_questions()

        await interaction.response.send_message(quest, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Kody(bot))
