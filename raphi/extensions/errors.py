from traceback import format_exception, print_exception

import discord
from discord import Interaction, app_commands
from discord.app_commands import AppCommandError
from discord.ext import commands
from raphi.raphi import Raphi


class Errors(commands.Cog):
    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

        self.bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self, interaction: Interaction, error: AppCommandError):
        await self.handle_error(interaction, error)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        await self.handle_error(ctx, error)

    @commands.Cog.listener()
    async def on_error(self, ctx: commands.Context, error: Exception):
        await self.handle_error(ctx, error)

    async def handle_error(self, ctx: commands.Context | Interaction, error: Exception | AppCommandError):
        """Dynamic error handler for `app_commands` and `ext.commands`

        Args:
            ctx (`commands.Context` | `discord.Interaction`): error source
            error (`Exception` | `AppCommandError`): error object
        """
        origin = type(ctx)
        user = ctx.author if origin == commands.Context else ctx.user

        # Select the right display message, or skip displaying one
        match type(error):
            case commands.CommandNotFound:
                return

            case app_commands.errors.CommandNotFound | discord.errors.NotFound:
                emsg = "Não consegui interpretar sua solicitação"

            case app_commands.errors.CheckFailure:
                return await ctx.response.send_message("Você não possui permissão para usar esse comando!", ephemeral=True)

            case app_commands.errors.CommandInvokeError:
                emsg = f"`{error}`"

            case app_commands.errors.CommandOnCooldown:
                return

            case _:
                emsg = f"Erro não tratado: `{type(error)}`"

        # Print the traceback if the user is the owner
        traceback = None
        if error.__traceback__ and user.id == self.bot.owner_id:
            traceback = (
                f"\n\nTraceback:\n" +
                f"```\n" +
                f"{''.join(format_exception(error, value=error, tb=error.__traceback__))}"
                f"```"
            )

        msg = f"Ops, algo deu errado! {emsg} {traceback if traceback else ''}"

        # Send the message the right way
        async def send_message(handle_origin, msg: str):
            if (handle_origin == commands.Context):
                # Simulate an ephemeral message
                await ctx.send(msg, delete_after=15)
            else:
                await ctx.response.send_message(msg, ephemeral=True)

        try:
            await send_message(origin, msg)
        except discord.errors.HTTPException as e:
            await send_message(
                origin, f"Ops, algo deu errado! {emsg}\n\nVerifique o console: `{type(error)}`")
            print_exception(error, value=error, tb=error.__traceback__)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Errors(bot))
