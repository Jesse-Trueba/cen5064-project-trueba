from decimal import Decimal

from domain.budget import Budget


class BudgetService:
    def __init__(self, budget_repository, transaction_repository=None):
        self.budget_repository = budget_repository
        self.transaction_repository = transaction_repository

    def create_budget(
        self,
        budget_id: str,
        monthly_limit,
        month: str,
    ) -> Budget:
        budget = Budget(
            budget_id,
            Decimal(str(monthly_limit)),
            month,
        )

        self.budget_repository.save(budget)

        return budget

    def create_or_update_monthly_budget(
        self,
        month: str,
        monthly_limit,
    ) -> Budget:
        budget_id = f"budget-{month}"

        return self.create_budget(
            budget_id=budget_id,
            monthly_limit=monthly_limit,
            month=month,
        )

    def get_budget_status(
        self,
        budget_id: str,
        total_spending=None,
    ) -> dict:
        budget = self.budget_repository.get_by_id(budget_id)

        if budget is None:
            raise ValueError("Budget not found.")

        if total_spending is None:
            spending = self._calculate_monthly_spending(budget.month)
        else:
            spending = Decimal(str(total_spending))

        return self._build_status(budget, spending)

    def get_budget_status_for_month(self, month: str) -> dict:
        budget = self.budget_repository.get_by_month(month)

        if budget is None:
            raise ValueError(f"No budget exists for {month}.")

        spending = self._calculate_monthly_spending(month)

        return self._build_status(budget, spending)

    def _calculate_monthly_spending(self, month: str) -> Decimal:
        if self.transaction_repository is None:
            return Decimal(0)

        transactions = self.transaction_repository.get_for_month(month)

        return sum(
            (
                transaction.amount
                for transaction in transactions
                if transaction.transaction_type == "expense"
            ),
            Decimal(0),
        )

    @staticmethod
    def _build_status(budget: Budget, spending: Decimal) -> dict:
        return {
            "id": budget.id,
            "month": budget.month,
            "monthly_limit": budget.monthly_limit,
            "total_spending": spending,
            "remaining": budget.calculate_remaining(spending),
            "exceeded": budget.is_exceeded(spending),
        }