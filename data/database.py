import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "finance.db"


def get_connection(database_path=None) -> sqlite3.Connection:
    path = database_path or DATABASE_PATH

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database(database_path=None) -> None:
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS budgets (
                id TEXT PRIMARY KEY,
                month TEXT NOT NULL,
                monthly_limit_cents INTEGER NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount_cents INTEGER NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense'))
            )
            """
        )

        connection.commit()