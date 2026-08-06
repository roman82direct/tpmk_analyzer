from abc import ABC, abstractmethod


class BaseExtractor[T](ABC):
    """Абстрактный generic-класс получения данных из разных источников."""

    @abstractmethod
    def extract(self) -> T: ...
