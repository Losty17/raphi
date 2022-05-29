import csv
import os
from io import StringIO
from pathlib import Path
from typing import Optional

import discord
from discord import Attachment, Interaction, Member
from discord.app_commands import (Choice, Group, choices, command, describe,
                                  rename)

from ..checks import *
from ..database import db
from ..db.models import Question
from ..views import SelectorView


class KodyQuestions(Group):
    def __init__(self):
        super().__init__(name="questions",
                         description="Question Administration Command")

    @command(name="add")
    async def _add(self, interaction: Interaction):
        """ Adiciona uma questão ao banco. """
        await interaction.response.send_message(
            "Adicionando uma questão...",
            view=SelectorView(),
            ephemeral=True
        )

    @command(name="import")
    @rename(file="arquivo")
    @describe(file='O arquivo ".csv" a ser usado. ' +
              'Deve conter uma linha de cabeçalho e valores separados por ";"')
    async def _import_csv(self, interaction: Interaction, file: Attachment):
        """ Importe seu arquivo .csv com as questões a serem gravadas no banco de dados. 
        Isso pode demorar. """

        # Mostrando para o usuário que uma ação está sendo realizada
        await interaction.response.defer()

        byte_content = await file.read()  # Lendo os bytes
        file = StringIO(byte_content.decode())  # Transformando em StringIO
        reader = csv.reader(file, delimiter=";")  # Lendo
        next(reader, None)  # Pulando o cabeçalho

        questions = []
        for row in reader:
            try:
                # Criando uma questão a partir do model
                quest = Question(
                    node=row[0],
                    text=row[1],
                    right_ans=row[2],
                    first_ans=row[3],
                    second_ans=row[4],
                    third_ans=row[5],
                )

                questions.append(quest)
            except:
                continue

        db.bulk_add_question(questions)  # Adicionando ao banco

        await interaction.followup.send(f"Foram adicionadas `{len(questions)}` questões!", ephemeral=True)

    @command(name="cooldown")
    @choices(option=[
        Choice(name="reset", value="reset")
    ])
    @rename(option="comando")
    @describe(option="A ação a ser realizada")
    async def _cooldown(self, interaction: Interaction, option: Choice[str], member: Optional[Member]):
        """ Gerenciador de intervalos para os usuários """
        match option.value:
            case "reset":
                user = db.get_user(interaction.user.id)
                user.last_question = None

                await interaction.response.send_message(
                    f'Cooldown reseted for user `{user.id}`. ' +
                    f'New cooldown: `{user.last_question}`', ephemeral=True
                )

                return

    @command(name="model")
    async def _send_csv_model(self, interaction: Interaction):
        """ Receba um modelo de .csv para ter como base """
        path = Path(__file__).parents[1].resolve()
        full_path = os.path.join(path, 'res', 'model.csv')
        with open(full_path, 'rb') as csv_file:
            byte_content = csv_file.read()
            csv_model = discord.File(
                StringIO(byte_content.decode()), filename="modelo.csv")
            await interaction.response.send_message("Aqui está um modelo de `.csv`", file=csv_model, ephemeral=True)
