from typing import Protocol

from domain.transaction import Transaction


class TransactionRepositoryPort(Protocol):
    """Defines the storage operations required by TransactionService."""

    def save(self, transaction: Transaction) -> None:
        """Save a transaction."""
        ...

    def get_all(self) -> list[Transaction]:
        """Return all stored transactions."""
        ...

    def get_for_month(self, month: str) -> list[Transaction]:
        """Return transactions belonging to a specific month."""
        ...