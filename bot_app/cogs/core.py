from __future__ import annotations

from discord.ext import commands


class CoreCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"Bot ligado como {self.bot.user}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            minutos = int(error.retry_after // 60)
            segundos = int(error.retry_after % 60)

            if minutos > 0:
                tempo_restante = f"{minutos}m e {segundos}s"
            else:
                tempo_restante = f"{segundos} segundos"

            await ctx.send(
                f"❌ {ctx.author.mention}, acalma-te! Ainda precisas de esperar **{tempo_restante}** para usar este comando novamente."
            )
            return

        raise error