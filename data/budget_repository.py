import json
from decimal import Decimal
from pathlib import Path

from domain.budget import Budget


class BudgetRepository:
    """Stores and retrieves budgets using a JSON file."""

    def __init__(self, file_path: str = "data/budgets.json") -> None:
        self._file_path = Path(file_path)

    def save(self, budget: Budget) -> None:
        budgets = self._load_all()

        budgets[str(budget.id)] = {
            "id": budget.id,
            "monthly_limit": str(budget.monthly_limit),
            "month": budget.month,
        }

        self._file_path.parent.mkdir(parents=True, exist_ok=True)

        with self._file_path.open("w", encoding="utf-8") as file:
            json.dump(budgets, file, indent=2)

    def get_by_id(self, budget_id: str) -> Budget | None:
        budgets = self._load_all()
        stored_budget = budgets.get(str(budget_id))

        if stored_budget is None:
            return None

        return Budget(
            id=stored_budget["id"],
            monthly_limit=Decimal(stored_budget["monthly_limit"]),
            month=stored_budget["month"],
        )

    def _load_all(self) -> dict:
        if not self._file_path.exists():
            return {}

        with self._file_path.open("r", encoding="utf-8") as file:
            return json.load(file)