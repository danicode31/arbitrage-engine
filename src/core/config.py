from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Configuración general del sistema.
    """

    project_name: str = "Arbitrage Engine Argentina"

    environment: str = "development"

    database_path: str = "data/arbitrage.db"

    log_level: str = "INFO"

    market_api_url: str | None = None

    market_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
