from decimal import Decimal

from data.budget_repository import BudgetRepository
from domain.budget import Budget


class BudgetService:
    """Coordinates budget-related application use cases."""

    def __init__(self, repository: BudgetRepository) -> None:
        self._repository = repository

    def create_budget(
        self,
        budget_id: str,
        monthly_limit: Decimal | int | str,
        month: str,
    ) -> Budget:
        budget = Budget(
            id=budget_id,
            monthly_limit=monthly_limit,
            month=month,
        )

        self._repository.save(budget)
        return budget

    def get_budget_status(
        self,
        budget_id: str,
        total_spending: Decimal | int | str,
    ) -> dict:
        budget = self._repository.get_by_id(budget_id)

        if budget is None:
            raise ValueError("Budget not found.")

        return {
            "id": budget.id,
            "month": budget.month,
            "monthly_limit": budget.monthly_limit,
            "total_spending": Decimal(total_spending),
            "remaining": budget.calculate_remaining(total_spending),
            "exceeded": budget.is_exceeded(total_spending),
        }