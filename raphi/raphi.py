from os import getenv, listdir, path
from pathlib import Path
from traceback import print_exc
from typing import List

from discord import Intents, Object
from discord.ext import commands


class Raphi(commands.Bot):
    package = 'raphi'
    ext_dir = 'extensions'
    root_dir = Path(__file__).parent.resolve()

    def __init__(self, command_prefix: str, *, intents: Intents, application_id: int) -> None:
        super().__init__(
            command_prefix,
            intents=intents,
            application_id=application_id
        )

        self.ext = self.get_extensions(self.ext_dir)

        self.glds = [
            Object(id=getenv("UDYR")),
            Object(id=getenv("TAVERN")),
        ]

    async def setup_hook(self) -> None:
        await self.load_modules(self.ext)

        for g in self.glds:
            self.tree.copy_global_to(guild=g)
            await self.tree.sync(guild=g)
            # await self.tree.sync()

    async def load_modules(self, extensions: List[str]):
        """Loads the specified extensions

        Args:
            extensions (List[str]): the list of extensions
        """
        for e in extensions:
            try:
                print(f"Loading: {self.package}{e}...", end=' ')
                await self.load_extension(e, package=self.package)
                print('Ok!')
            except Exception as ex:
                print(f"Failed.")
                print_exc(ex)

    def get_extensions(self, directory: str) -> List[str]:
        """Get the bot's extensions from the specified directory

        Args:
            directory (str): extensions directory
        Returns:
            List[str]: a list containing all the extensions
        """
        file_list = listdir(
            path.join(
                self.root_dir,
                directory
            )
        )

        return [f'.{directory}.{e[:-3]}' for e in file_list if e.endswith('.py')]
