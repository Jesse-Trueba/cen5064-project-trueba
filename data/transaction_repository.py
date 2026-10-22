from decimal import Decimal

from data.database import get_connection, initialize_database
from domain.transaction import Transaction


class TransactionRepository:
    def __init__(self, database_path=None):
        self.database_path = database_path
        initialize_database(self.database_path)

    def save(self, transaction: Transaction) -> None:
        amount_cents = int(transaction.amount * 100)

        with get_connection(self.database_path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO transactions (
                    id,
                    date,
                    description,
                    category,
                    amount_cents,
                    type
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction.id,
                    transaction.date,
                    transaction.description,
                    transaction.category,
                    amount_cents,
                    transaction.transaction_type,
                ),
            )

            connection.commit()

    def get_all(self) -> list[Transaction]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, date, description, category, amount_cents, type
                FROM transactions
                ORDER BY date DESC
                """
            ).fetchall()

        return [self._row_to_transaction(row) for row in rows]

    def get_for_month(self, month: str) -> list[Transaction]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, date, description, category, amount_cents, type
                FROM transactions
                WHERE date LIKE ?
                ORDER BY date DESC
                """,
                (f"{month}-%",),
            ).fetchall()

        return [self._row_to_transaction(row) for row in rows]

    @staticmethod
    def _row_to_transaction(row) -> Transaction:
        return Transaction(
            id=row["id"],
            date=row["date"],
            description=row["description"],
            category=row["category"],
            amount=Decimal(row["amount_cents"]) / Decimal(100),
            transaction_type=row["type"],
        )