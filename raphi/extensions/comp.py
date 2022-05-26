import json
import os
from random import choice, shuffle
from typing import Dict, List, Optional

# import db
import discord
<<<<<<< HEAD
import os
from discord import Object, app_commands, Interaction
=======
from discord import app_commands
>>>>>>> 044b980774382fecd61d1aa0f16a51945dc2eb5a
from discord.ext import commands
from raphi.raphi import Raphi
from raphi import db


def check_permission():
    def predicate(interaction: Interaction) -> bool:
        return interaction.guild.id == 501807001324617748 and interaction.channel.id == 979441373046521937
    return app_commands.check(predicate)


class Question:
    def __init__(self, answers: List[str], right_answer: str, content: str) -> None:
        self.answers = answers
        self.right_answer = right_answer
        self.content = content

    @classmethod
    def get_question(self, answers: List[str], right_answer: str, content: str):
        return Question(answers, right_answer, content) if right_answer in answers else None


class QuestionButton(discord.ui.Button):
    def __init__(self, label: str, right_ans: str, buttons: List[discord.ui.Button], view: discord.ui.View, *, style: discord.ButtonStyle = discord.ButtonStyle.grey):
        super().__init__(style=style, label=label)
        self.ans = label
        self.right_ans = right_ans
        self.buttons = buttons
        self._view = view

    async def callback(self, interaction: discord.Interaction) -> None:
        if (self.ans == self.right_ans):
            self.style = discord.ButtonStyle.green
            msg = "Você acertou!"
        else:
            self.style = discord.ButtonStyle.red
            msg = "Você errou..."

        for btn in self.buttons:
            btn.disabled = True

        await interaction.response.edit_message(content=msg, view=self._view)


class QuestionUi(discord.ui.View):
    def __init__(self, question: Question):
        super().__init__(timeout=60)
        self.question = question
        shuffle(self.question.answers)
        right_ans = self.question.right_answer

        btns = []

        for i in question.answers:
            btns.append(QuestionButton(i, right_ans, btns, self))

        for btn in btns:
            self.add_item(btn)


class Comp(commands.Cog):
    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

        questions_path = os.path.join(
            self.bot.res_dir, 'comp', 'questions.json')

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
            await interaction.response.send_message(content=content, view=QuestionUi(question), ephemeral=True)

    @_question_command.error
    async def _on_question_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f'Você já respondeu uma pergunta, tente novamente em {int(round(error.retry_after, 0))}s', ephemeral=True)
            return

    @app_commands.command(name="testdb")
    async def _test_db(self, interaction: discord.Interaction):
        """ Testa o banco de dados """
        database = db.Database()

        database.sync()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Comp(bot))
