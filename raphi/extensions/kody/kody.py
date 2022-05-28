import json
import os
from datetime import datetime
from random import choice
from typing import Dict, List

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from raphi.raphi import Raphi

from .checks import *
from .db.models.enums import NodeEnum
from .question import Question
from .views import QuestionUi
from . import db as database

db = database.KodyDatabase()


class Kody(commands.Cog):
    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

        questions_path = os.path.join(
            self.bot.res_dir, 'kody', 'questions.json')

        with open(questions_path, 'rb') as file:
            self.questions: List[Dict] = json.loads(file.read())

        db.sync()

    @app_commands.command(name="question")
    @check_permission()
    @check_cooldown(db)
    @ensure_user_created(db)
    async def _question_command(self, interaction: Interaction):
        """ Responda uma perguntinha! """
        # Set the cooldown for the user
        user = db.get_user(interaction.user.id)
        user.last_question = datetime.utcnow()
        db.update_user_last_question(user)

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
    async def _on_question_command_error(self, interaction: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            cd = error.retry_after / 60 / 60
            msg = 'Uma pergunta já foi respondida recentemente. ' + \
                f'Você poderá responder outra pergunta em: {round(cd)}h'
            await interaction.response.send_message(msg, ephemeral=True)
            return

    @app_commands.command(name="testdb")
    @check_permission()
    async def _test_db(self, interaction: Interaction):
        """ Testa o banco de dados """
        db.create_user(interaction.user.id)

        user = db.get_user(interaction.user.id)

        for i in range(9):
            db.insert_question(
                "texto", NodeEnum.coding.name, "certo", "errado")

        quest = db.get_questions()

        await interaction.response.send_message(quest, ephemeral=True)
