from raphi.raphi import Raphi
from . import kody


async def setup(bot: Raphi) -> None:
    await bot.add_cog(kody.Kody(bot))
