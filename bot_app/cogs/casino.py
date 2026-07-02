from __future__ import annotations

import asyncio
import random

import discord
from discord.ext import commands

from bot_app.config import PRECO_CARGO, ROLE_NAME_PREMIO
from bot_app.storage import DojoCoinStore


class CasinoCog(commands.Cog):
    def __init__(self, bot: commands.Bot, store: DojoCoinStore) -> None:
        self.bot = bot
        self.store = store

    @commands.command(name="roleta", help="Aposta DojoCoins na roleta. Uso: $son$ roleta [DojoCoins] [red/black/green]")
    async def roleta(self, ctx: commands.Context, aposta: int, escolha: str) -> None:
        user_id = ctx.author.id
        saldo_atual = self.store.get_balance(user_id)
        escolha = escolha.lower()

        if aposta <= 0:
            await ctx.send("❌ A aposta deve ser maior que 0!")
            return

        if saldo_atual < aposta:
            await ctx.send(f"❌ Você não tem DojoCoins suficientes! Saldo: {saldo_atual} DojoCoins")
            return

        if escolha not in ["red", "black", "green"]:
            await ctx.send("❌ Escolha inválida! Use `red`, `black` ou `green`.")
            return

        opcoes = ["red"] * 18 + ["black"] * 18 + ["green"] * 2
        resultado = random.choice(opcoes)

        self.store.remove_balance(user_id, aposta)

        if resultado == escolha:
            multiplicador = 10 if resultado == "green" else 2
            ganho = aposta * multiplicador
            saldo_final = self.store.add_balance(user_id, ganho)
            await ctx.send(
                f"🎉 A roleta girou e caiu em **{resultado.upper()}**! {ctx.author.mention} ganhou **{ganho}** DojoCoins! Saldo atual: {saldo_final} DojoCoins"
            )
        else:
            saldo_final = self.store.get_balance(user_id)
            await ctx.send(
                f"😭 A roleta girou e caiu em **{resultado.upper()}**! {ctx.author.mention} perdeu **{aposta}** DojoCoins. Saldo atual: {saldo_final} DojoCoins"
            )

    @commands.command(name="comprarcargo", help="Compra o cargo exclusivo por 1 hora.")
    async def comprar_cargo(self, ctx: commands.Context) -> None:
        user_id = ctx.author.id
        saldo_atual = self.store.get_balance(user_id)

        if saldo_atual < PRECO_CARGO:
            await ctx.send(
                f"❌ Você precisa de {PRECO_CARGO} DojoCoins para comprar este cargo. Você tem: {saldo_atual} DojoCoins"
            )
            return

        cargo = discord.utils.get(ctx.guild.roles, name=ROLE_NAME_PREMIO) if ctx.guild else None
        if not cargo:
            await ctx.send(
                f"❌ Erro: não encontrei o cargo **{ROLE_NAME_PREMIO}** no servidor. Cria esse cargo ou ajusta `DOJOCOINS_ROLE_NAME`."
            )
            return

        self.store.remove_balance(user_id, PRECO_CARGO)

        try:
            await ctx.author.add_roles(cargo)
            await ctx.send(f"👑 {ctx.author.mention} comprou o cargo **{cargo.name}** por 1 hora! Parabéns!")

            await asyncio.sleep(3600)
            await ctx.author.remove_roles(cargo)
            await ctx.send(f"⏰ O tempo do cargo VIP de {ctx.author.mention} acabou!")
        except discord.Forbidden:
            await ctx.send(
                "❌ Eu não tenho permissão para gerenciar cargos. Verifique se o meu cargo está acima do cargo VIP na lista."
            )

    @commands.command(name="coinflip", help="Desafia alguém para cara ou coroa. Uso: $son$ coinflip @membro [DojoCoins]")
    async def coinflip(self, ctx: commands.Context, oponente: discord.Member, aposta: int) -> None:
        desafiante = ctx.author

        if oponente.id == desafiante.id:
            await ctx.send("❌ Não podes desafiar-te a ti próprio!")
            return

        if oponente.bot:
            await ctx.send("❌ Não podes desafiar um bot!")
            return

        if aposta <= 0:
            await ctx.send("❌ A aposta deve ser maior do que 0!")
            return

        saldo_desafiante = self.store.get_balance(desafiante.id)
        saldo_oponente = self.store.get_balance(oponente.id)

        if saldo_desafiante < aposta:
            await ctx.send(f"❌ {desafiante.mention}, não tens DojoCoins suficientes! Saldo: {saldo_desafiante} DojoCoins")
            return

        if saldo_oponente < aposta:
            await ctx.send(
                f"❌ {oponente.mention} não tem DojoCoins suficientes para aceitar esta aposta de {aposta} DojoCoins!"
            )
            return

        await ctx.send(
            f"🪙 {oponente.mention}, foste desafiado por {desafiante.mention} para um **Coin Flip**!\n"
            f"💰 **Valor da aposta:** {aposta} DojoCoins de cada um (Total em jogo: {aposta * 2} DojoCoins).\n"
            f"Escreve `sim` para aceitar ou `não` para recusar. Tens 30 segundos!"
        )

        def check(msg: discord.Message) -> bool:
            return msg.author.id == oponente.id and msg.channel.id == ctx.channel.id and msg.content.lower() in ["sim", "nao", "não"]

        try:
            resposta = await self.bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send(
                f"⏰ O tempo acabou! O desafio de {desafiante.mention} foi cancelado porque {oponente.mention} não respondeu."
            )
            return

        if resposta.content.lower() in ["nao", "não"]:
            await ctx.send(f" Peace out! {oponente.mention} recusou o desafio de {desafiante.mention}.")
            return

        if self.store.get_balance(desafiante.id) < aposta or self.store.get_balance(oponente.id) < aposta:
            await ctx.send("❌ O Coin Flip foi cancelado porque um de vocês já não tem DojoCoins suficientes.")
            return

        await ctx.send("🪙 A moeda está no ar... 🔄")
        await asyncio.sleep(2)

        resultado = random.choice([0, 1])
        if resultado == 0:
            vencedor = desafiante
            perdedor = oponente
        else:
            vencedor = oponente
            perdedor = desafiante

        self.store.add_balance(vencedor.id, aposta)
        self.store.remove_balance(perdedor.id, aposta)

        await ctx.send(
            f"🎉 A moeda caiu! **{vencedor.mention}** ganhou o Coin Flip e levou **{aposta * 2} DojoCoins** no total! \n"
            f"💀 {perdedor.mention} perdeu {aposta} DojoCoins. Boa sorte na próxima!"
        )