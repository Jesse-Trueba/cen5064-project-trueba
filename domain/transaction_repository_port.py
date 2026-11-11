from typing import Protocol

from domain.transaction import Transaction


class TransactionRepositoryPort(Protocol):
    """Defines the storage operations required by TransactionService."""

    def save(
        self,
        transaction: Transaction,
    ) -> None: ...

    def get_all(
        self,
    ) -> list[Transaction]: ...

    def get_for_month(
        self,
        month: str,
    ) -> list[Transaction]: ...

    def delete(
        self,
        transaction_id: str,
    ) -> None: ...

    def delete_many(
        self,
        transaction_ids: list[str],
    ) -> None: ...