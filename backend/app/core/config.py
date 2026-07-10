from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс настройки приложения."""

    app_name: str = 'GC_BI'
    app_description: str = 'tpmk_analyzer'
    database_url: str = (
        'postgresql+asyncpg://user:password@localhost:5432/gc_bi_db'
    )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
