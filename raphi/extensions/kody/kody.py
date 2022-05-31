import os
from datetime import datetime
from typing import Optional

from discord import Interaction, Member, app_commands
from discord.ext import commands
from raphi.raphi import Raphi

from .groups import KodyStaff
from .checks import *
from .database import db
from .db.models import Question
from .views import QuestionUi
from .embed import QuestionEmbed


class Kody(commands.Cog):
    kody = KodyStaff()

    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

        # --- Debug ---
        if os.getenv("ENVIRONMENT").lower() != "production":
            db.sync()

    @app_commands.command(name="question")
    @check_permission()
    @check_cooldown(db)
    @ensure_user_created(db)
    async def _question_command(self, interaction: Interaction):
        """ Responda uma perguntinha! """
        # Set the cooldown for the user
        await interaction.response.defer(ephemeral=True, thinking=True)

        user = db.get_user(interaction.user.id)
        user.last_question = datetime.utcnow()

        question = db.get_random_question()

        if question:
            question_embed = QuestionEmbed(question)

            await interaction.followup.send(embed=question_embed, view=QuestionUi(question, author=interaction.user))
        else:
            await interaction.followup.send("Ocorreu um erro ao procurar uma questão.", ephemeral=True)

    @_question_command.error
    async def _on_question_error(self, interaction: Interaction, error):
        if isinstance(error, app_commands.CommandOnCooldown):
            cd = error.retry_after / 60 / 60

            msg = 'Uma pergunta já foi respondida recentemente. ' + \
                f'Você poderá responder outra pergunta em: {round(cd)}h'

            return await interaction.response.send_message(msg, ephemeral=True)

    @app_commands.command(name="profile")
    async def _user_data(self, interaction: Interaction, member: Optional[Member] = None):
        target = member or interaction.user

        user = db.get_user(target.id)

        data = f'''
        id: {user.id}
        vip: {user.vip}
        last_vote: {user.last_vote}
        last_question: {user.last_question}
        ----
        web: {user.web_bits}
        data: {user.data_bits}
        design: {user.design_bits}
        coding: {user.coding_bits}
        network: {user.network_bits}
        robotics: {user.robotics_bits}
        hardware: {user.hardware_bits}
        software: {user.software_bits}
        '''

        await interaction.response.send_message(data)

    async def _select_question(self) -> Question:
        return db.get_random_question()
