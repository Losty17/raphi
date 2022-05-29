from discord.app_commands import Group, guild_only

from ..checks import *
from . import KodyQuestions, KodyUsers


@guild_only()
class KodyStaff(Group):
    questions = KodyQuestions()
    users = KodyUsers()

    def __init__(self):
        super().__init__(name="staff",
                         description="Kody Administration commands")

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user.id in [207947146371006464, 333457501817405442]
