from bot_app.config import DB_PATH, get_token
from bot_app.core import DojoBot
from bot_app.storage import DojoCoinStore


def main() -> None:
    store = DojoCoinStore(DB_PATH)
    bot = DojoBot(store)
    bot.run(get_token())


if __name__ == "__main__":
    main()