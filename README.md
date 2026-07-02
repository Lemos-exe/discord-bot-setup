# Bot Discord

Projeto base para bots com `discord.py`.

## Setup

1. Cria e ativa o ambiente virtual:

```bash
/usr/local/bin/python3 -m venv .venv
source .venv/bin/activate
```

2. Instala as dependências:

```bash
pip install -r requirements.txt
```

3. Define o token do bot:

```python
export DISCORD_TOKEN="o_teu_token_aqui"
```

4. Executa o bot:

```bash
python bot.py
```

## Estrutura

- `bot.py`: ponto de entrada.
- `bot_app/config.py`: configurações e constantes.
- `bot_app/storage.py`: persistência do saldo em JSON.
- `bot_app/cogs/`: comandos separados por domínio.
- `requirements.txt`: dependências do projeto.
- `.venv/`: ambiente virtual local.

## Variáveis de ambiente

- `DISCORD_TOKEN`: token do bot.
- `DOJOCOINS_DB_FILE`: ficheiro JSON para os saldos. Padrão: `banco_dojocoins.json`.
- `DOJOCOINS_ROLE_NAME`: nome do cargo de prémio do casino. Padrão: `VIP DojoCoins`.

## Observações

- Não partilhes o token do bot com ninguém!
