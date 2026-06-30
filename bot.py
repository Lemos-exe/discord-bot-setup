import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ligado como {bot.user}")
# 
# @bot.event
# async def on_member_join(member):
    # channel = discord.utils.get(member.guild.text_channels, name="geral")
    # if channel:
        # await channel.send(f"Bem-vindo(a) ao servidor {member.mention}!")
# 
# @bot.event
# async def on_member_remove(member):
    # channel = discord.utils.get(member.guild.text_channels, name="geral")
    # if channel:
        # await channel.send(f"{member.mention} saiu do servidor.")

@bot.command()
async def server(ctx):
    """Mostra nome e contagem de membros do servidor."""
    guild = ctx.guild
    nome = guild.name
    membros = guild.member_count
    icon_url = guild.icon.url if guild.icon else ""
    await ctx.send(f"Servidor: **{nome}**\nMembros: **{membros}** {icon_url}")


@bot.command()
async def ajuda(ctx):
    """Lista os comandos disponíveis."""
    comandos = (
        "**!ajuda** - Lista os comandos disponíveis.\n"
        "**!server** - Mostra nome e contagem de membros do servidor.\n"
        "**!ola** - Saudação.\n"
        "**!ping** - Latência do bot.\n"
        "**!dado** - Lança um dado (1-6).\n"
        "**!moeda** - Joga uma moeda.\n"
        "**!avatar** - Mostra seu avatar.\n"
        "**!pergunta <pergunta>** - Responde aleatoriamente.\n"
    )
    await ctx.send(f"Comandos disponíveis:\n{comandos}")


@bot.command()
async def ola(ctx):
    await ctx.send(f"Olá {ctx.author.mention}!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong {round(bot.latency * 1000)} ms")

@bot.command()
async def dado(ctx):
    numero = random.randint(1, 6)
    await ctx.send(f"Saiu o número **{numero}**")

@bot.command()
async def moeda(ctx):
    resultado = random.choice(["Cara", "Coroa"])
    await ctx.send(f"Resultado: **{resultado}**")

@bot.command()
async def avatar(ctx):
    await ctx.send(ctx.author.display_avatar.url)

@bot.command()
async def pergunta(ctx, *, _):
    respostas = [
        "SIM!!!" ,
        "É claro que sim",
        "Não",
        "Nope",
        "Não faço ideia",
        "*Perchance*",
        "Pergunta mais tarde."
    ]
    await ctx.send(random.choice(respostas))

token=("teu_token_aqui")

if not token:
    raise RuntimeError("DISCORD_TOKEN nao definido no ambiente")

bot.run(token)