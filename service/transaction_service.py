from decimal import Decimal
from uuid import uuid4

from data.transaction_repository import TransactionRepository
from domain.transaction import Transaction


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def add_transaction(
        self,
        transaction_date: str,
        description: str,
        category: str,
        amount: str | int | Decimal,
        transaction_type: str,
    ) -> Transaction:
        transaction = Transaction(
            id=str(uuid4()),
            date=transaction_date,
            description=description,
            category=category,
            amount=Decimal(str(amount)),
            transaction_type=transaction_type,
        )

        self.repository.save(transaction)

        return transaction

    def get_all_transactions(self) -> list[Transaction]:
        return self.repository.get_all()

    def get_transactions_for_month(self, month: str) -> list[Transaction]:
        return self.repository.get_for_month(month)

    def get_monthly_expense_total(self, month: str) -> Decimal:
        transactions = self.repository.get_for_month(month)

        return sum(
            (
                transaction.amount
                for transaction in transactions
                if transaction.transaction_type == "expense"
            ),
            Decimal(0),
        )

    def get_monthly_income_total(self, month: str) -> Decimal:
        transactions = self.repository.get_for_month(month)

        return sum(
            (
                transaction.amount
                for transaction in transactions
                if transaction.transaction_type == "income"
            ),
            Decimal(0),
        )