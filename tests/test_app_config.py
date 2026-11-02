from config.app_config import AppConfig


def test_app_config_returns_same_instance():
    first = AppConfig()
    second = AppConfig()

    assert first is second


def test_app_config_has_database_path():
    config = AppConfig()

    assert config.database_path.name == "finance.db"