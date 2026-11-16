from decimal import Decimal

from data.database import get_connection, initialize_database
from domain.savings_goal import SavingsGoal


class SavingsGoalRepository:
    def __init__(self, database_path=None):
        self.database_path = database_path
        initialize_database(self.database_path)

    def save(self, goal: SavingsGoal) -> None:
        # Store money as integer cents to avoid floating-point errors.
        target_cents = int(goal.target_amount * 100)
        current_cents = int(goal.current_amount * 100)

        with get_connection(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO savings_goals (
                    id,
                    name,
                    target_amount_cents,
                    current_amount_cents
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    target_amount_cents = excluded.target_amount_cents,
                    current_amount_cents = excluded.current_amount_cents
                """,
                (
                    goal.id,
                    goal.name,
                    target_cents,
                    current_cents,
                ),
            )
            connection.commit()

    def get_all(self) -> list[SavingsGoal]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    name,
                    target_amount_cents,
                    current_amount_cents
                FROM savings_goals
                ORDER BY name
                """
            ).fetchall()

        return [
            self._row_to_goal(row)
            for row in rows
        ]

    def get_by_id(
        self,
        goal_id: str,
    ) -> SavingsGoal | None:
        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    name,
                    target_amount_cents,
                    current_amount_cents
                FROM savings_goals
                WHERE id = ?
                """,
                (goal_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_goal(row)

    @staticmethod
    def _row_to_goal(row) -> SavingsGoal:
        # Convert stored cents back into Decimal dollar values.
        return SavingsGoal(
            goal_id=row["id"],
            name=row["name"],
            target_amount=(
                Decimal(row["target_amount_cents"])
                / Decimal(100)
            ),
            current_amount=(
                Decimal(row["current_amount_cents"])
                / Decimal(100)
            ),
        )