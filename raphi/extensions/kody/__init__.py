from raphi.raphi import Raphi
from .kody import Kody


async def setup(bot: Raphi) -> None:
    await bot.add_cog(Kody(bot))
