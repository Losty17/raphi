from typing import Optional

from discord import Interaction, Member
from discord.app_commands import (Choice, Group, choices, command, describe,
                                  rename)

from ..checks import *
from ..database import db


class KodyUsers(Group):
    def __init__(self):
        super().__init__(name="users", description="Manage Users")

    @command(name="vip")
    @choices(vip=[
        Choice(name="No Boost", value=VipEnum.none.name),
        Choice(name="Single Boost", value=VipEnum.once.name),
        Choice(name="Mega Booster", value=VipEnum.mega.name),
        Choice(name="Giga Booster", value=VipEnum.giga.name),
        Choice(name="Tera Booster", value=VipEnum.tera.name),
    ])
    @describe(member="Usuário a ser alterado", vip="Tipo de VIP adquirido")
    @rename(member="usuário")
    async def _add_vip(self, interaction: Interaction, member: Member, vip: Choice[str]):
        """ Gerencia o cargo VIP de um usuário """

        user = db.get_user(member.id)
        if not user:
            return await interaction.response.send_message("Não consegui encontrar o cadastro do usuário")

        old_vip: VipEnum = user.vip
        user.vip = vip.value

        match vip.value:
            case VipEnum.none.name:
                name = "Single" if old_vip == VipEnum.once else None

                msg = f"Desculpe {member.mention}, parece que você perdeu " + \
                    f"seus benefícios de {name if name else old_vip.name.capitalize()} Booster..."

            case VipEnum.once.name:
                msg = f"Obrigado pela contribuição, " + \
                    f"{member.mention}! Aproveite seus benefícios!"

            case _:
                msg = f"Parabéns {member.mention}! " + \
                    f"Agora você é um {vip.name}! Aproveite seus benefícios!"

        await interaction.response.send_message(msg)

    @command(name="register")
    @choices(vip=[
        Choice(name="No Boost", value=VipEnum.none.name),
        Choice(name="Single Boost", value=VipEnum.once.name),
        Choice(name="Mega Booster", value=VipEnum.mega.name),
        Choice(name="Giga Booster", value=VipEnum.giga.name),
        Choice(name="Tera Booster", value=VipEnum.tera.name),
    ])
    @describe(member="Usuário a ser registrado", vip="VIP adquirido pelo usuário. Padrão: Nenhum")
    @rename(member="usuário")
    async def _register_user(self, interaction: Interaction, member: Member, vip: Optional[Choice[str]]):
        """ Registra um usuário no banco de dados """
        await interaction.response.defer()

        _vip = vip or VipEnum.none
        user = User(id=member.id, vip=_vip.name)
        db.create_user(user)

        msg = f"Obrigado por se juntar a nós, {member.mention}!"
        if _vip != VipEnum.none:
            msg += f" Aproveite o seu {_vip.name}!"

        await interaction.followup.send(msg)
