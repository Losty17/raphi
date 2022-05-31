from typing import List

from discord import ButtonStyle, Interaction, User
from discord.ui import Button, View

from ..embed import QuestionEmbed

from ..database import db
from ..db.models.enums import NodeEnum


class QuestionButton(Button):
    def __init__(
        self,
        label: str,
        node: str,
        right_ans: str,
        buttons: List[Button],
        *, author: User, style: ButtonStyle = ButtonStyle.grey
    ):
        super().__init__(style=style, label=label)
        self.ans = label
        self.right_ans = right_ans
        self.buttons = buttons
        self.node = node
        self.author = author

    async def callback(self, interaction: Interaction) -> None:
        if self.ans == self.right_ans:
            self.style = ButtonStyle.green
            msg = "Você acertou!"
            db.get_user(interaction.user.id).update_node(self.node)
        else:
            self.style = ButtonStyle.red
            msg = "Você errou..."

        for btn in self.buttons:
            btn.disabled = True

        await interaction.response.edit_message(content=msg, view=self.view)
