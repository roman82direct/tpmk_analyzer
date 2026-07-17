from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    """Класс общих настроек приложения."""

    app_name: str = 'GC_BI'
    app_description: str = 'tpmk_analyzer'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
