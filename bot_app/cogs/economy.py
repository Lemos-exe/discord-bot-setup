from __future__ import annotations

import discord
from discord.ext import commands

from bot_app.storage import DojoCoinStore


class EconomyCog(commands.Cog):
    def __init__(self, bot: commands.Bot, store: DojoCoinStore) -> None:
        self.bot = bot
        self.store = store

    @commands.command(name="daily", help="Resgata suas 200 DojoCoins diárias. Pode ser usado a cada 1 hora.")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def daily(self, ctx: commands.Context) -> None:
        saldo_atual = self.store.add_balance(ctx.author.id, 200)
        await ctx.send(f"💰 {ctx.author.mention} resgatou **200 DojoCoins**! Saldo atual: {saldo_atual} DojoCoins.")

    @commands.command(name="saldo", help="Mostra quantas DojoCoins você tem.")
    async def saldo(self, ctx: commands.Context) -> None:
        saldo_atual = self.store.get_balance(ctx.author.id)
        await ctx.send(f"💳 {ctx.author.mention}, você tem **{saldo_atual}** DojoCoins.")

    @commands.command(name="leaderboard", aliases=["lb"], help="Mostra o Top 10 de utilizadores com mais DojoCoins.")
    async def leaderboard(self, ctx: commands.Context) -> None:
        if not self.store.balances:
            await ctx.send("📉 O banco de dados está vazio. Ninguém tem DojoCoins ainda!")
            return

        ranking_ordenado = sorted(self.store.balances.items(), key=lambda item: item[1], reverse=True)
        top_10 = ranking_ordenado[:10]

        texto_leaderboard = "🏆 **LEADERBOARD - TOP 10 MAIS RICOS** 🏆\n"
        texto_leaderboard += "—" * 35 + "\n\n"

        async with ctx.typing():
            for posicao, (user_id, saldo_atual) in enumerate(top_10, start=1):
                if posicao == 1:
                    emoji = "🥇"
                elif posicao == 2:
                    emoji = "🥈"
                elif posicao == 3:
                    emoji = "🥉"
                else:
                    emoji = f"**#{posicao}**"

                user = self.bot.get_user(user_id)
                if not user:
                    try:
                        user = await self.bot.fetch_user(user_id)
                    except Exception:
                        user = None

                nome_usuario = user.name if user else f"Utilizador Desconhecido ({user_id})"
                texto_leaderboard += f"{emoji} **{nome_usuario}** — `{saldo_atual}` DojoCoins\n"

        texto_leaderboard += "\n" + "—" * 35
        await ctx.send(texto_leaderboard)

    @commands.command(name="pagar", help="Envia DojoCoins para outro membro. Uso: $son$ pagar @membro [DojoCoins]")
    async def pagar(self, ctx: commands.Context, membro: discord.Member, quantia: int) -> None:
        autor_id = ctx.author.id
        membro_id = membro.id

        if autor_id == membro_id:
            await ctx.send("❌ Tu não podes enviar DojoCoins para ti mesmo!")
            return

        if quantia <= 0:
            await ctx.send("❌ A quantia a enviar deve ser maior que 0!")
            return

        saldo_autor = self.store.get_balance(autor_id)
        if saldo_autor < quantia:
            await ctx.send(f"❌ Não tens DojoCoins suficientes! O teu saldo atual é de **{saldo_autor}** DojoCoins.")
            return

        saldo_autor_novo, _ = self.store.transfer(autor_id, membro_id, quantia)
        await ctx.send(
            f"💸 {ctx.author.mention} enviou **{quantia}** DojoCoins para {membro.mention}! \n"
            f" Novo saldo de {ctx.author.mention}: **{saldo_autor_novo}** DojoCoins."
        )

    @commands.command(name="bonus", help="Resgata um bónus extra de DojoCoins a cada hora.")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def bonus(self, ctx: commands.Context) -> None:
        saldo_atual = self.store.add_balance(ctx.author.id, 1000)
        await ctx.send(
            f"✨ **1000 DojoCoins** de bónus foram adicionados à tua conta, {ctx.author.mention}! Saldo atual: {saldo_atual} DojoCoins."
        )