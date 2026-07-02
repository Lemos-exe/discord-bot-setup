from __future__ import annotations

from discord.ext import commands

from bot_app.cogs.casino import CasinoCog
from bot_app.cogs.core import CoreCog
from bot_app.cogs.economy import EconomyCog
from bot_app.config import PREFIX, build_intents
from bot_app.storage import DojoCoinStore


class DojoBot(commands.Bot):
    def __init__(self, store: DojoCoinStore) -> None:
        super().__init__(command_prefix=PREFIX, intents=build_intents())
        self.store = store

    async def setup_hook(self) -> None:
        await self.add_cog(CoreCog(self))
        await self.add_cog(EconomyCog(self, self.store))
        await self.add_cog(CasinoCog(self, self.store))