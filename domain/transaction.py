from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation

EXPENSE_CATEGORIES = {
    "Groceries",
    "Dining",
    "Transportation",
    "Housing",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Other",
}

INCOME_CATEGORIES = {
    "Salary",
    "Bonus",
    "Investment",
    "Other",
}


@dataclass(frozen=True)
class Transaction:
    id: str
    date: str
    description: str
    category: str
    amount: Decimal
    transaction_type: str

    def __post_init__(self):
        if not self.id.strip():
            raise ValueError("Transaction ID cannot be empty.")

        try:
            date.fromisoformat(self.date)
        except ValueError as exc:
            raise ValueError("Date must use YYYY-MM-DD format.") from exc

        if not self.description.strip():
            raise ValueError("Description cannot be empty.")

        if isinstance(self.amount, float):
            raise TypeError("Amount must not be a float.")

        try:
            amount = Decimal(str(self.amount))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Amount must be a valid number.") from exc

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        transaction_type = self.transaction_type.lower().strip()
        category = self.category.strip()

        if transaction_type not in {"income", "expense"}:
            raise ValueError("Transaction type must be income or expense.")

        if (
            transaction_type == "expense"
            and category not in EXPENSE_CATEGORIES
        ):
            raise ValueError(
                f"Invalid expense category: {category}."
            )

        if (
            transaction_type == "income"
            and category not in INCOME_CATEGORIES
        ):
            raise ValueError(
                f"Invalid income category: {category}."
            )

        object.__setattr__(self, "amount", amount)
        object.__setattr__(self, "transaction_type", transaction_type)
        object.__setattr__(self, "category", category)