from decimal import Decimal

from data.savings_goal_repository import SavingsGoalRepository
from domain.savings_goal import SavingsGoal


def test_save_and_get_savings_goal(tmp_path):
    database_path = tmp_path / "test.db"

    repository = SavingsGoalRepository(
        database_path
    )

    goal = SavingsGoal(
        goal_id="goal-1",
        name="Vacation",
        target_amount="2000",
    )

    repository.save(goal)

    saved_goal = repository.get_by_id(
        "goal-1"
    )

    assert saved_goal is not None
    assert saved_goal.name == "Vacation"
    assert saved_goal.target_amount == Decimal(2000)
    assert saved_goal.current_amount == Decimal(0)


def test_update_savings_goal(tmp_path):
    database_path = tmp_path / "test.db"

    repository = SavingsGoalRepository(
        database_path
    )

    goal = SavingsGoal(
        goal_id="goal-1",
        name="Vacation",
        target_amount="2000",
    )

    repository.save(goal)

    goal.add_contribution("500")
    repository.save(goal)

    saved_goal = repository.get_by_id(
        "goal-1"
    )

    assert saved_goal is not None
    assert saved_goal.current_amount == Decimal(500)


def test_get_all_savings_goals(tmp_path):
    database_path = tmp_path / "test.db"

    repository = SavingsGoalRepository(
        database_path
    )

    repository.save(
        SavingsGoal(
            goal_id="goal-1",
            name="Vacation",
            target_amount="2000",
        )
    )

    repository.save(
        SavingsGoal(
            goal_id="goal-2",
            name="Laptop",
            target_amount="1500",
        )
    )

    goals = repository.get_all()

    assert len(goals) == 2