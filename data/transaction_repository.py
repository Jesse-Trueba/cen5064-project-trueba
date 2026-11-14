from decimal import Decimal

from data.database import get_connection, initialize_database
from domain.transaction import Transaction


class TransactionRepository:
    def __init__(self, database_path=None):
        self.database_path = database_path
        initialize_database(self.database_path)

    def save(self, transaction: Transaction) -> None:
        # Store money as integer cents to avoid floating-point errors.
        amount_cents = int(transaction.amount * 100)

        with get_connection(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO transactions (
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
                SELECT
                    id,
                    date,
                    description,
                    category,
                    amount_cents,
                    type
                FROM transactions
                ORDER BY date DESC
                """
            ).fetchall()

        return [
            self._row_to_transaction(row)
            for row in rows
        ]

    def get_for_month(
        self,
        month: str,
    ) -> list[Transaction]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    date,
                    description,
                    category,
                    amount_cents,
                    type
                FROM transactions
                WHERE date LIKE ?
                ORDER BY date DESC
                """,
                (f"{month}-%",),
            ).fetchall()

        return [
            self._row_to_transaction(row)
            for row in rows
        ]

    def delete(
        self,
        transaction_id: str,
    ) -> None:
        with get_connection(self.database_path) as connection:
            # Verify the transaction exists before attempting deletion.
            existing = connection.execute(
                """
                SELECT id
                FROM transactions
                WHERE id = ?
                """,
                (transaction_id,),
            ).fetchone()

            if existing is None:
                raise ValueError(
                    f"Transaction not found: {transaction_id}"
                )

            connection.execute(
                """
                DELETE FROM transactions
                WHERE id = ?
                """,
                (transaction_id,),
            )
            connection.commit()

    def delete_many(
        self,
        transaction_ids: list[str],
    ) -> None:
        if not transaction_ids:
            return

        placeholders = ", ".join(
            "?" for _ in transaction_ids
        )

        with get_connection(self.database_path) as connection:
            # Check that every requested transaction exists first.
            rows = connection.execute(
                f"""
                SELECT id
                FROM transactions
                WHERE id IN ({placeholders})
                """,
                transaction_ids,
            ).fetchall()

            existing_ids = {
                row["id"]
                for row in rows
            }

            missing_ids = [
                transaction_id
                for transaction_id in transaction_ids
                if transaction_id not in existing_ids
            ]

            if missing_ids:
                raise ValueError(
                    "Transaction(s) not found: "
                    + ", ".join(missing_ids)
                )

            connection.execute(
                f"""
                DELETE FROM transactions
                WHERE id IN ({placeholders})
                """,
                transaction_ids,
            )
            connection.commit()

    @staticmethod
    def _row_to_transaction(row) -> Transaction:
        # Convert stored cents back into Decimal dollars.
        return Transaction(
            id=row["id"],
            date=row["date"],
            description=row["description"],
            category=row["category"],
            amount=(
                Decimal(row["amount_cents"])
                / Decimal(100)
            ),
            transaction_type=row["type"],
        )