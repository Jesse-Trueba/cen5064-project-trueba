from decimal import Decimal

import pytest

from data.savings_goal_repository import SavingsGoalRepository
from service.savings_goal_service import SavingsGoalService


def test_create_goal(tmp_path):
    database_path = tmp_path / "test.db"

    repository = SavingsGoalRepository(
        database_path
    )
    service = SavingsGoalService(
        repository
    )

    goal = service.create_goal(
        name="Vacation",
        target_amount="2000",
    )

    assert goal.name == "Vacation"
    assert goal.target_amount == Decimal(2000)
    assert goal.current_amount == Decimal(0)


def test_created_goal_is_saved(tmp_path):
    database_path = tmp_path / "test.db"

    repository = SavingsGoalRepository(
        database_path
    )
    service = SavingsGoalService(
        repository
    )

    goal = service.create_goal(
        name="Laptop",
        target_amount="1500",
    )

    saved_goal = repository.get_by_id(
        goal.id
    )

    assert saved_goal is not None
    assert saved_goal.name == "Laptop"


def test_add_contribution(tmp_path):
    database_path = tmp_path / "test.db"

    repository = SavingsGoalRepository(
        database_path
    )
    service = SavingsGoalService(
        repository
    )

    goal = service.create_goal(
        name="Vacation",
        target_amount="2000",
    )

    updated_goal = service.add_contribution(
        goal.id,
        "500",
    )

    assert (
        updated_goal.current_amount
        == Decimal(500)
    )
    assert (
        updated_goal.remaining_amount
        == Decimal(1500)
    )


def test_contribution_is_persisted(tmp_path):
    database_path = tmp_path / "test.db"

    repository = SavingsGoalRepository(
        database_path
    )
    service = SavingsGoalService(
        repository
    )

    goal = service.create_goal(
        name="Vacation",
        target_amount="2000",
    )

    service.add_contribution(
        goal.id,
        "500",
    )

    saved_goal = repository.get_by_id(
        goal.id
    )

    assert saved_goal is not None
    assert (
        saved_goal.current_amount
        == Decimal(500)
    )


def test_get_all_goals(tmp_path):
    database_path = tmp_path / "test.db"

    repository = SavingsGoalRepository(
        database_path
    )
    service = SavingsGoalService(
        repository
    )

    service.create_goal(
        name="Vacation",
        target_amount="2000",
    )

    service.create_goal(
        name="Laptop",
        target_amount="1500",
    )

    goals = service.get_all_goals()

    assert len(goals) == 2


def test_missing_goal_raises_error(tmp_path):
    database_path = tmp_path / "test.db"

    repository = SavingsGoalRepository(
        database_path
    )
    service = SavingsGoalService(
        repository
    )

    with pytest.raises(
        ValueError,
        match="Savings goal not found",
    ):
        service.add_contribution(
            "missing-goal",
            "100",
        )