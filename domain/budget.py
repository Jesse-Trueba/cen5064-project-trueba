from decimal import Decimal
from typing import Any


class Budget:
    """Domain entity representing a monthly spending budget."""

    def __init__(
        self,
        id: Any,
        monthly_limit: Decimal | int | str,
        month: str,
    ) -> None:
        self._id = id
        self._monthly_limit = self._coerce_monetary_value(
            monthly_limit, "Monthly limit"
        )
        if self._monthly_limit < Decimal("0"):
            raise ValueError("Monthly limit cannot be negative.")
        self._month = month

    @property
    def id(self) -> Any:
        return self._id

    @property
    def monthly_limit(self) -> Decimal:
        return self._monthly_limit

    @property
    def month(self) -> str:
        return self._month

    def calculate_remaining(self, total_spending: Decimal | int | str) -> Decimal:
        spending = self._coerce_monetary_value(total_spending, "Total spending")
        self._validate_spending(spending)
        return self._monthly_limit - spending

    def is_exceeded(self, total_spending: Decimal | int | str) -> bool:
        spending = self._coerce_monetary_value(total_spending, "Total spending")
        self._validate_spending(spending)
        return spending > self._monthly_limit

    @staticmethod
    def _coerce_monetary_value(value: Any, field_name: str) -> Decimal:
        if isinstance(value, float):
            raise TypeError(
                f"{field_name} cannot be a float to prevent precision issues. Use Decimal, int, or str."
            )
        if not isinstance(value, (Decimal, int, str)):
            raise TypeError(
                f"{field_name} must be a Decimal, int, or str, got {type(value).__name__}."
            )
        return Decimal(value)

    @staticmethod
    def _validate_spending(spending: Decimal) -> None:
        if spending < Decimal("0"):
            raise ValueError("Total spending cannot be negative.")