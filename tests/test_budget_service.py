from decimal import Decimal

import pytest

from data.budget_repository import BudgetRepository
from service.budget_service import BudgetService


def test_budget_working_slice(tmp_path):
    storage_file = tmp_path / "budgets.json"
    repository = BudgetRepository(str(storage_file))
    service = BudgetService(repository)

    service.create_budget(
        budget_id="budget-1",
        monthly_limit=Decimal("500.00"),
        month="2026-10",
    )

    status = service.get_budget_status(
        budget_id="budget-1",
        total_spending=Decimal("350.00"),
    )

    assert status["monthly_limit"] == Decimal("500.00")
    assert status["total_spending"] == Decimal("350.00")
    assert status["remaining"] == Decimal("150.00")
    assert status["exceeded"] is False


def test_budget_working_slice_when_exceeded(tmp_path):
    storage_file = tmp_path / "budgets.json"
    repository = BudgetRepository(str(storage_file))
    service = BudgetService(repository)

    service.create_budget(
        budget_id="budget-2",
        monthly_limit=Decimal("500.00"),
        month="2026-10",
    )

    status = service.get_budget_status(
        budget_id="budget-2",
        total_spending=Decimal("625.50"),
    )

    assert status["remaining"] == Decimal("-125.50")
    assert status["exceeded"] is True


def test_budget_not_found(tmp_path):
    storage_file = tmp_path / "budgets.json"
    repository = BudgetRepository(str(storage_file))
    service = BudgetService(repository)

    with pytest.raises(ValueError, match="Budget not found."):
        service.get_budget_status(
            budget_id="missing",
            total_spending=Decimal("100.00"),
        )