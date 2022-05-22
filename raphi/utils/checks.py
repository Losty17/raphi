from discord import Interaction, app_commands
from os import getenv


def is_owner():
    def predicate(interaction: Interaction) -> bool:
        return interaction.user.id == int(getenv("OWNER_ID"))
    return app_commands.check(predicate)
