from typing import List

from discord import ButtonStyle, Interaction
from discord.ui import Button, View


class QuestionButton(Button):
    def __init__(
        self,
        label: str,
        right_ans: str,
        buttons: List[Button],
        view: View,
        *, style: ButtonStyle = ButtonStyle.grey
    ):
        super().__init__(style=style, label=label)
        self.ans = label
        self.right_ans = right_ans
        self.buttons = buttons
        self._view = view

    async def callback(self, interaction: Interaction) -> None:
        if (self.ans == self.right_ans):
            self.style = ButtonStyle.green
            msg = "Você acertou!"
        else:
            self.style = ButtonStyle.red
            msg = "Você errou..."

        for btn in self.buttons:
            btn.disabled = True

        await interaction.response.edit_message(content=msg, view=self._view)
