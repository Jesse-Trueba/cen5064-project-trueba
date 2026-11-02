from pathlib import Path


class AppConfig:
    """Application-wide configuration shared as a single instance."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.database_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "finance.db"
            )

        return cls._instance