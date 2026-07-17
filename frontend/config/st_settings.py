from config.settings import BaseAppSettings


class StreamlitSettings(BaseAppSettings):
    """Класс настроек frontend-приложения."""

    api_base_url: str = 'http://localhost:8000/api/v1/'


st_settings = StreamlitSettings()
