import logging

from backend.app.config.settings import backend_settings


def logging_setup() -> None:
    logging.basicConfig(
        format=backend_settings.log_format,
        level=getattr(logging,
                      backend_settings.log_level.upper(),
                      logging.INFO)
    )
