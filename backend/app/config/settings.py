from config.settings import BaseAppSettings


class BackendSettings(BaseAppSettings):
    """Класс настроек backend-приложения."""

    database_url: str = (
        'postgresql+asyncpg://postgres:root@localhost:5432/gc_bi_db'
    )
    log_level: str = 'DEBUG'
    log_format: str = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'


backend_settings = BackendSettings()
