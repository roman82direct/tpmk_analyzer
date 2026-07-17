from pathlib import Path

from config.settings import BaseAppSettings

ROOT_DIR = Path(__file__).resolve().parents[3]


class BackendSettings(BaseAppSettings):
    """Класс настроек backend-приложения."""

    log_level: str = 'DEBUG'
    log_format: str = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    database_url: str = (
        'postgresql+asyncpg://postgres:root@localhost:5432/gc_bi_db'
    )
    storage_input_dir: Path = ROOT_DIR / 'storage' / 'input'


backend_settings = BackendSettings()
