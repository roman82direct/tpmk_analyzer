from abc import ABC, abstractmethod
from collections.abc import Iterable


class BaseExtractor[T](ABC):
    """Абстрактный generic-класс получения данных из разных источников."""

    @abstractmethod
    def extract(self) -> Iterable[T]: ...
