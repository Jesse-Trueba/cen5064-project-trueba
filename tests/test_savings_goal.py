from decimal import Decimal

import pytest

from domain.savings_goal import SavingsGoal


def test_create_savings_goal():
    goal = SavingsGoal(
        goal_id="goal-1",
        name="Vacation",
        target_amount="2000",
    )

    assert goal.id == "goal-1"
    assert goal.name == "Vacation"
    assert goal.target_amount == Decimal(2000)
    assert goal.current_amount == Decimal(0)


def test_add_contribution():
    goal = SavingsGoal(
        goal_id="goal-1",
        name="Vacation",
        target_amount="2000",
    )

    goal.add_contribution("500")

    assert goal.current_amount == Decimal(500)
    assert goal.remaining_amount == Decimal(1500)


def test_progress_percentage():
    goal = SavingsGoal(
        goal_id="goal-1",
        name="Vacation",
        target_amount="2000",
        current_amount="500",
    )

    assert goal.progress_percentage == Decimal(25)


def test_goal_is_complete():
    goal = SavingsGoal(
        goal_id="goal-1",
        name="Vacation",
        target_amount="2000",
        current_amount="2000",
    )

    assert goal.is_complete is True
    assert goal.remaining_amount == Decimal(0)


def test_progress_does_not_exceed_100_percent():
    goal = SavingsGoal(
        goal_id="goal-1",
        name="Vacation",
        target_amount="1000",
        current_amount="1200",
    )

    assert goal.progress_percentage == Decimal(100)
    assert goal.remaining_amount == Decimal(0)


def test_empty_name_is_invalid():
    with pytest.raises(
        ValueError,
        match="Savings goal name cannot be empty",
    ):
        SavingsGoal(
            goal_id="goal-1",
            name="",
            target_amount="1000",
        )


def test_zero_target_is_invalid():
    with pytest.raises(
        ValueError,
        match="Target amount must be greater than zero",
    ):
        SavingsGoal(
            goal_id="goal-1",
            name="Vacation",
            target_amount="0",
        )


def test_negative_contribution_is_invalid():
    goal = SavingsGoal(
        goal_id="goal-1",
        name="Vacation",
        target_amount="1000",
    )

    with pytest.raises(
        ValueError,
        match="Contribution must be greater than zero",
    ):
        goal.add_contribution("-50")


def test_float_target_is_invalid():
    with pytest.raises(
        TypeError,
        match="Target amount must not use float",
    ):
        SavingsGoal(
            goal_id="goal-1",
            name="Vacation",
            target_amount=1000.50,
        )