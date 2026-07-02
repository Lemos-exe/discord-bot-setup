from __future__ import annotations

import json
from pathlib import Path


class DojoCoinStore:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self._balances = self._load()

    def _load(self) -> dict[int, int]:
        if not self.file_path.exists():
            return {}

        try:
            with self.file_path.open("r", encoding="utf-8") as file_handle:
                stored_data = json.load(file_handle)
                return {int(user_id): int(balance) for user_id, balance in stored_data.items()}
        except Exception as error:
            print(f"Erro ao carregar dados: {error}")
            return {}

    def save(self) -> None:
        try:
            with self.file_path.open("w", encoding="utf-8") as file_handle:
                json.dump(self._balances, file_handle, indent=4, ensure_ascii=False)
        except Exception as error:
            print(f"Erro ao salvar banco de dados: {error}")

    @property
    def balances(self) -> dict[int, int]:
        return self._balances

    def get_balance(self, user_id: int) -> int:
        return self._balances.get(user_id, 0)

    def add_balance(self, user_id: int, amount: int) -> int:
        self._balances[user_id] = self.get_balance(user_id) + amount
        self.save()
        return self._balances[user_id]

    def remove_balance(self, user_id: int, amount: int) -> int:
        self._balances[user_id] = self.get_balance(user_id) - amount
        self.save()
        return self._balances[user_id]

    def transfer(self, from_user_id: int, to_user_id: int, amount: int) -> tuple[int, int]:
        self._balances[from_user_id] = self.get_balance(from_user_id) - amount
        self._balances[to_user_id] = self.get_balance(to_user_id) + amount
        self.save()
        return self.get_balance(from_user_id), self.get_balance(to_user_id)