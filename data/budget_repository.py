from decimal import Decimal

from data.database import get_connection, initialize_database
from domain.budget import Budget


class BudgetRepository:
    def __init__(self, database_path=None):
        self.database_path = database_path
        initialize_database(self.database_path)

    def save(self, budget: Budget) -> None:
        monthly_limit_cents = int(budget.monthly_limit * 100)

        with get_connection(self.database_path) as connection:
            connection.execute(
                """
                DELETE FROM budgets
                WHERE month = ? AND id != ?
                """,
                (budget.month, budget.id),
            )

            connection.execute(
                """
                INSERT OR REPLACE INTO budgets (
                    id,
                    month,
                    monthly_limit_cents
                )
                VALUES (?, ?, ?)
                """,
                (
                    budget.id,
                    budget.month,
                    monthly_limit_cents,
                ),
            )

            connection.commit()

    def get_by_id(self, budget_id: str) -> Budget | None:
        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT id, month, monthly_limit_cents
                FROM budgets
                WHERE id = ?
                """,
                (budget_id,),
            ).fetchone()

        if row is None:
            return None

        return Budget(
            row["id"],
            Decimal(row["monthly_limit_cents"]) / Decimal(100),
            row["month"],
        )

    def get_by_month(self, month: str) -> Budget | None:
        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT id, month, monthly_limit_cents
                FROM budgets
                WHERE month = ?
                ORDER BY rowid DESC
                LIMIT 1
                """,
                (month,),
            ).fetchone()

        if row is None:
            return None

        return Budget(
            row["id"],
            Decimal(row["monthly_limit_cents"]) / Decimal(100),
            row["month"],
        )

    def get_all(self) -> list[Budget]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, month, monthly_limit_cents
                FROM budgets
                ORDER BY month DESC
                """
            ).fetchall()

        return [
            Budget(
                row["id"],
                Decimal(row["monthly_limit_cents"]) / Decimal(100),
                row["month"],
            )
            for row in rows
        ]