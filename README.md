# Bot Discord

Projeto base para bots com `discord.py`.

## Setup

1. Cria e ativa o ambiente virtual:
   
Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Windows
```
python -m venv -venv
.venv\Scripts\activate.bat
```

2. Instala as dependências:

```bash
pip install -r requirements.txt
```

3. Define o token do bot:

```python
bot.run("o_teu_token_aqui")
```

4. Executa o bot:

```bash
python bot.py
```

## Estrutura

- `bot.py`: código principal do bot.
- `requirements.txt`: dependências do projeto.
- `.venv/`: ambiente virtual local.

## Observações

- Não partilhes o token do bot com ninguém!
