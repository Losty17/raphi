import json
from random import choice, shuffle
from typing import Dict, List, Optional
import discord
import os
from discord import app_commands
from discord.ext import commands
from raphi.raphi import Raphi


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
            for btn in self.buttons:
                btn.disabled = True

            await interaction.response.edit_message(content="Correto!", view=self._view)


class QuestionUi(discord.ui.View):
    def __init__(self, question: Question, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Comp(bot))
