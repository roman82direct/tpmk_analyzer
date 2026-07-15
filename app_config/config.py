from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    """Класс общих настроек приложения."""

    app_name: str = 'GC_BI'
    app_description: str = 'tpmk_analyzer'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class BackendSettings(BaseAppSettings):
    """Класс настроек backend-приложения."""

    database_url: str = (
        'postgresql+asyncpg://postgres:root@localhost:5432/gc_bi_db'
    )


class StreamlitSettings(BaseAppSettings):
    """Класс настроек frontend-приложения."""

    api_base_url: str = 'http://localhost:8000/api/v1/'


backend_settings = BackendSettings()
st_settings = StreamlitSettings()
