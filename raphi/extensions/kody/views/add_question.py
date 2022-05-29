from typing import Optional

from discord import Interaction, SelectOption, TextStyle
from discord.ui import Select, View, Modal, TextInput

from ..database import db
from ..db.models import Question
from ..db.models.enums import NodeEnum


class NodeModal(Modal):
    quest = TextInput(
        label='Pergunta:',
        style=TextStyle.paragraph,
        placeholder='Digite a pergunta',
        required=True,
        max_length=200,
    )
    right_ans = TextInput(
        label='Resposta correta:',
        style=TextStyle.short,
        placeholder='Digite a respota correta',
        required=True,
        max_length=200,
    )
    ans1 = TextInput(
        label='Resposta:',
        style=TextStyle.short,
        placeholder='Digite uma resposta incorreta',
        required=True,
        max_length=200,
    )
    ans2 = TextInput(
        label='Resposta:',
        style=TextStyle.short,
        placeholder='Digite uma resposta incorreta',
        required=False,
        max_length=200,
    )
    ans3 = TextInput(
        label='Resposta:',
        style=TextStyle.short,
        placeholder='Digite uma resposta incorreta',
        required=False,
        max_length=200,
    )

    def __init__(self, node: str) -> None:
        self.node = node
        super().__init__(
            title=f"Adicionando questão sobre {node}", timeout=None)

    async def on_submit(self, interaction: Interaction):
        quest = db.add_question(Question(
            node=self.node,
            text=self.quest.value,
            right_ans=self.right_ans.value,
            first_ans=self.ans1.value,
            second_ans=self.ans2.value,
            third_ans=self.ans3.value
        ))

        await interaction.response.send_message(f'Added question: {quest}!', ephemeral=True)

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        # traceback.print_tb(error.__traceback__)


class NodeSelector(Select):
    def __init__(self) -> None:
        emojis = ['🧭', '📟', '🎨', '💻', '📠', '🤖', '🖱️', '📀']
        options = []
        for i, n in enumerate(NodeEnum):
            options.append(SelectOption(
                label=n.name.capitalize(), emoji=emojis[i], value=n.name))

        super().__init__(
            placeholder="Selecione um node...",
            min_values=1, max_values=1,
            options=options
        )

    async def callback(self, interaction: Interaction):
        self.disabled = True
        self.placeholder = self.values[0]

        # msg = await interaction.edit_original_message(view=self.view)

        await interaction.response.send_modal(NodeModal(self.values[0]))


class SelectorView(View):
    def __init__(self):
        super().__init__(timeout=30)
        self.add_item(NodeSelector())
