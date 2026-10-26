from decimal import Decimal

from domain.transaction import Transaction
from service.transaction_service import TransactionService


class FakeTransactionRepository:
    def __init__(self):
        self.transactions: list[Transaction] = []

    def save(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def get_all(self) -> list[Transaction]:
        return self.transactions.copy()

    def get_for_month(self, month: str) -> list[Transaction]:
        return [
            transaction
            for transaction in self.transactions
            if transaction.date.startswith(f"{month}-")
        ]


def test_service_works_with_fake_repository():
    repository = FakeTransactionRepository()
    service = TransactionService(repository)

    transaction = service.add_transaction(
        transaction_date="2026-10-26",
        description="Publix",
        category="Groceries",
        amount="50.00",
        transaction_type="expense",
    )

    assert transaction in repository.transactions
    assert transaction.description == "Publix"
    assert transaction.amount == Decimal("50.00")


def test_monthly_expense_total_without_database():
    repository = FakeTransactionRepository()
    service = TransactionService(repository)

    service.add_transaction(
        transaction_date="2026-10-10",
        description="Publix",
        category="Groceries",
        amount="50.00",
        transaction_type="expense",
    )

    service.add_transaction(
        transaction_date="2026-10-15",
        description="Gas",
        category="Transportation",
        amount="25.00",
        transaction_type="expense",
    )

    service.add_transaction(
        transaction_date="2026-10-20",
        description="Paycheck",
        category="Salary",
        amount="1000.00",
        transaction_type="income",
    )

    assert service.get_monthly_expense_total("2026-10") == Decimal(
        "75.00"
    )


def test_monthly_income_total_without_database():
    repository = FakeTransactionRepository()
    service = TransactionService(repository)

    service.add_transaction(
        transaction_date="2026-10-20",
        description="Paycheck",
        category="Salary",
        amount="1000.00",
        transaction_type="income",
    )

    service.add_transaction(
        transaction_date="2026-10-21",
        description="Bonus",
        category="Bonus",
        amount="250.00",
        transaction_type="income",
    )

    assert service.get_monthly_income_total("2026-10") == Decimal(
        "1250.00"
    )