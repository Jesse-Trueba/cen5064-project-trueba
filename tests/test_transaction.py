from decimal import Decimal

import pytest

from domain.transaction import Transaction


def test_expense_accepts_valid_category():
    transaction = Transaction(
        id="1",
        date="2026-10-22",
        description="Publix",
        category="Groceries",
        amount=Decimal("50.00"),
        transaction_type="expense",
    )

    assert transaction.category == "Groceries"
    assert transaction.transaction_type == "expense"


def test_income_accepts_valid_category():
    transaction = Transaction(
        id="2",
        date="2026-10-22",
        description="Paycheck",
        category="Salary",
        amount=Decimal("1500.00"),
        transaction_type="income",
    )

    assert transaction.category == "Salary"
    assert transaction.transaction_type == "income"


def test_expense_rejects_income_category():
    with pytest.raises(
        ValueError,
        match="Invalid expense category",
    ):
        Transaction(
            id="3",
            date="2026-10-22",
            description="Incorrect expense",
            category="Salary",
            amount=Decimal("25.00"),
            transaction_type="expense",
        )


def test_income_rejects_expense_category():
    with pytest.raises(
        ValueError,
        match="Invalid income category",
    ):
        Transaction(
            id="4",
            date="2026-10-22",
            description="Incorrect income",
            category="Groceries",
            amount=Decimal("100.00"),
            transaction_type="income",
        )


def test_transaction_rejects_unknown_category():
    with pytest.raises(
        ValueError,
        match="Invalid expense category",
    ):
        Transaction(
            id="5",
            date="2026-10-22",
            description="Unknown category",
            category="Random Stuff",
            amount=Decimal("20.00"),
            transaction_type="expense",
        )

def test_transaction_rejects_empty_description():
    with pytest.raises(
        ValueError,
        match="Description cannot be empty",
    ):
        Transaction(
            id="6",
            date="2026-10-23",
            description="",
            category="Groceries",
            amount=Decimal("25.00"),
            transaction_type="expense",
        )


def test_transaction_rejects_empty_category():
    with pytest.raises(
        ValueError,
        match="Invalid expense category",
    ):
        Transaction(
            id="7",
            date="2026-10-23",
            description="Publix",
            category="",
            amount=Decimal("25.00"),
            transaction_type="expense",
        )