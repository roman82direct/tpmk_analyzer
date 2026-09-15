from pathlib import Path
from urllib.parse import quote

from pydantic import SecretStr

from config.settings import BaseAppSettings

ROOT_DIR = Path(__file__).resolve().parents[3]


class BackendSettings(BaseAppSettings):
    """Класс настроек backend-приложения."""

    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_db: str
    postgres_user: str = 'postgres'
    postgres_pass: SecretStr = SecretStr('root')

    clickhouse_host: str = 'localhost'
    clickhouse_port: int = 8123
    clickhouse_db: str
    clickhouse_user: str
    clickhouse_pass: SecretStr = SecretStr('guest')

    log_level: str = 'DEBUG'
    log_format: str = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

    storage_input_dir: Path = ROOT_DIR / 'storage' / 'input'

    @property
    def postgres_url(self) -> str:
        """Строка подключения к Postgres."""
        user = quote(self.postgres_user, safe='')
        password = quote(self.postgres_pass.get_secret_value(), safe='')
        host = quote(self.postgres_host, safe='')
        return (
            f'postgresql+asyncpg://{user}:{password}@'
            f'{host}:{self.postgres_port}/{self.postgres_db}'
        )

    @property
    def clickhouse_url(self) -> str:
        """Строка подключения ClickHouse."""
        user = quote(self.clickhouse_user, safe='')
        password = quote(self.clickhouse_pass.get_secret_value(), safe='')
        host = quote(self.clickhouse_host, safe='')
        return (
            f'http://{user}:{password}@{host}:{self.clickhouse_port}/'
            f'?database={self.clickhouse_db}'
        )


backend_settings = BackendSettings()
