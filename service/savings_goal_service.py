from uuid import uuid4

from data.savings_goal_repository import SavingsGoalRepository
from domain.savings_goal import SavingsGoal


class SavingsGoalService:
    def __init__(
        self,
        repository: SavingsGoalRepository,
    ):
        self.repository = repository

    def create_goal(
        self,
        name: str,
        target_amount,
    ) -> SavingsGoal:
        goal = SavingsGoal(
            goal_id=str(uuid4()),
            name=name,
            target_amount=target_amount,
        )

        self.repository.save(goal)

        return goal

    def add_contribution(
        self,
        goal_id: str,
        amount,
    ) -> SavingsGoal:
        goal = self.repository.get_by_id(goal_id)

        if goal is None:
            raise ValueError(
                f"Savings goal not found: {goal_id}"
            )

        goal.add_contribution(amount)

        self.repository.save(goal)

        return goal

    def get_all_goals(self) -> list[SavingsGoal]:
        return self.repository.get_all()

    def get_goal(
        self,
        goal_id: str,
    ) -> SavingsGoal:
        goal = self.repository.get_by_id(goal_id)

        if goal is None:
            raise ValueError(
                f"Savings goal not found: {goal_id}"
            )

        return goal