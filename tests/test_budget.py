from decimal import Decimal
import pytest
from domain.budget import Budget


def test_budget_attributes():
    budget = Budget(id=1, monthly_limit=Decimal("500.00"), month="2026-05")
    assert budget.id == 1
    assert budget.monthly_limit == Decimal("500.00")
    assert budget.month == "2026-05"


def test_under_budget():
    budget = Budget(id=1, monthly_limit=Decimal("500.00"), month="2026-05")
    spending = Decimal("350.00")

    assert budget.calculate_remaining(spending) == Decimal("150.00")
    assert budget.is_exceeded(spending) is False


def test_exactly_at_budget():
    budget = Budget(id=1, monthly_limit=Decimal("500.00"), month="2026-05")
    spending = Decimal("500.00")

    assert budget.calculate_remaining(spending) == Decimal("0.00")
    assert budget.is_exceeded(spending) is False


def test_over_budget():
    budget = Budget(id=1, monthly_limit=Decimal("500.00"), month="2026-05")
    spending = Decimal("625.50")

    assert budget.calculate_remaining(spending) == Decimal("-125.50")
    assert budget.is_exceeded(spending) is True


def test_zero_budget():
    budget = Budget(id=1, monthly_limit=Decimal("0.00"), month="2026-05")
    assert budget.monthly_limit == Decimal("0.00")

    assert budget.calculate_remaining(Decimal("0.00")) == Decimal("0.00")
    assert budget.is_exceeded(Decimal("0.00")) is False

    assert budget.calculate_remaining(Decimal("10.00")) == Decimal("-10.00")
    assert budget.is_exceeded(Decimal("10.00")) is True


def test_zero_spending():
    budget = Budget(id=1, monthly_limit=Decimal("300.00"), month="2026-05")
    spending = Decimal("0.00")

    assert budget.calculate_remaining(spending) == Decimal("300.00")
    assert budget.is_exceeded(spending) is False


def test_negative_budget_validation():
    with pytest.raises(ValueError, match="Monthly limit cannot be negative."):
        Budget(id=1, monthly_limit=Decimal("-0.01"), month="2026-05")


def test_negative_spending_validation():
    budget = Budget(id=1, monthly_limit=Decimal("500.00"), month="2026-05")
    negative_spending = Decimal("-50.00")

    with pytest.raises(ValueError, match="Total spending cannot be negative."):
        budget.calculate_remaining(negative_spending)

    with pytest.raises(ValueError, match="Total spending cannot be negative."):
        budget.is_exceeded(negative_spending)


def test_rejects_float_monetary_input():
    # Float in constructor
    with pytest.raises(TypeError, match="cannot be a float"):
        Budget(id=1, monthly_limit=150.50, month="2026-05")

    budget = Budget(id=1, monthly_limit=Decimal("500.00"), month="2026-05")

    # Float in calculate_remaining
    with pytest.raises(TypeError, match="cannot be a float"):
        budget.calculate_remaining(50.25)

    # Float in is_exceeded
    with pytest.raises(TypeError, match="cannot be a float"):
        budget.is_exceeded(50.25)