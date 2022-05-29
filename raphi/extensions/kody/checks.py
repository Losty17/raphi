from datetime import datetime, timedelta
from discord import Interaction, app_commands

from .db import KodyDatabase
from .db.models import User
from .db.models.enums import VipEnum


def check_permission():
    def predicate(interaction: Interaction) -> bool:
        role = interaction.user.get_role(980149959435374655)
        return interaction.guild.id == 501807001324617748 and role
    return app_commands.check(predicate)


def ensure_user_created(db: KodyDatabase):
    def predicate(interaction: Interaction) -> bool:
        user = db.get_user(interaction.user.id)
        if not user:
            db.create_user(User(id=interaction.user.id))

        return True
    return app_commands.check(predicate)


def check_cooldown(db: KodyDatabase):
    def predicate(interaction: Interaction) -> bool:
        user = db.get_user(interaction.user.id)
        if user is None or user.last_question is None:
            return True
        diff: timedelta = datetime.utcnow() - user.last_question
        match user.vip:
            case VipEnum.mega:
                cd = 60 * 60 * 10

            case VipEnum.giga:
                cd = 60 * 60 * 8

            case VipEnum.tera:
                cd = 60 * 60 * 6

            case VipEnum.none:
                cd = 60 * 60 * 12

        if diff.total_seconds() >= cd:
            return True
        else:
            retry_after = (timedelta(seconds=cd) - diff).total_seconds()
            raise app_commands.CommandOnCooldown(cd, retry_after)
    return app_commands.check(predicate)


def is_staff():
    def predicate(interaction: Interaction) -> bool:
        staff_ids = [207947146371006464, 333457501817405442]
        return interaction.user.id in staff_ids
    return app_commands.check(predicate)
