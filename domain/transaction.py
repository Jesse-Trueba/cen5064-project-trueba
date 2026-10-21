from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation


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

        if not self.category.strip():
            raise ValueError("Category cannot be empty.")

        if isinstance(self.amount, float):
            raise TypeError("Amount must not be a float.")

        try:
            amount = Decimal(str(self.amount))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Amount must be a valid number.") from exc

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        transaction_type = self.transaction_type.lower().strip()

        if transaction_type not in {"income", "expense"}:
            raise ValueError("Transaction type must be income or expense.")

        object.__setattr__(self, "amount", amount)
        object.__setattr__(self, "transaction_type", transaction_type)