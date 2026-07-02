import os

import discord


PREFIX = "$$$ "
DB_PATH = os.getenv("DOJOCOINS_DB_FILE", "banco_dojocoins.json")
ROLE_NAME_PREMIO = os.getenv("DOJOCOINS_ROLE_NAME", "VIP DojoCoins")
PRECO_CARGO = 500


def build_intents() -> discord.Intents:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    return intents


def get_token() -> str:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN nao definido corretamente")
    return token