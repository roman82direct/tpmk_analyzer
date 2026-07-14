from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс настроек приложения."""

    app_name: str = 'GC_BI'
    app_description: str = 'tpmk_analyzer'
    database_url: str = (
        'postgresql+asyncpg://postgres:root@localhost:5433/gc_bi_db'
    )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
