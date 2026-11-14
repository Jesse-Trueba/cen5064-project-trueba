from decimal import Decimal, InvalidOperation


class SavingsGoal:
    def __init__(
        self,
        goal_id: str,
        name: str,
        target_amount,
        current_amount=0,
    ):
        if not goal_id or not goal_id.strip():
            raise ValueError("Savings goal ID cannot be empty.")

        if not name or not name.strip():
            raise ValueError("Savings goal name cannot be empty.")

        if isinstance(target_amount, float):
            raise TypeError(
                "Target amount must not use float."
            )

        if isinstance(current_amount, float):
            raise TypeError(
                "Current amount must not use float."
            )

        try:
            target = Decimal(str(target_amount))
            current = Decimal(str(current_amount))
        except InvalidOperation as error:
            raise ValueError(
                "Savings amounts must be valid numbers."
            ) from error

        if target <= 0:
            raise ValueError(
                "Target amount must be greater than zero."
            )

        if current < 0:
            raise ValueError(
                "Current amount cannot be negative."
            )

        self.id = goal_id.strip()
        self.name = name.strip()
        self.target_amount = target
        self.current_amount = current

    def add_contribution(self, amount) -> None:
        if isinstance(amount, float):
            raise TypeError(
                "Contribution must not use float."
            )

        try:
            contribution = Decimal(str(amount))
        except InvalidOperation as error:
            raise ValueError(
                "Contribution must be a valid number."
            ) from error

        if contribution <= 0:
            raise ValueError(
                "Contribution must be greater than zero."
            )

        self.current_amount += contribution

    @property
    def remaining_amount(self) -> Decimal:
        remaining = (
            self.target_amount
            - self.current_amount
        )

        if remaining < 0:
            return Decimal(0)

        return remaining

    @property
    def progress_percentage(self) -> Decimal:
        percentage = (
            self.current_amount
            / self.target_amount
            * Decimal(100)
        )

        return min(
            percentage,
            Decimal(100),
        )

    @property
    def is_complete(self) -> bool:
        return (
            self.current_amount
            >= self.target_amount
        )