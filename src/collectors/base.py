from abc import ABC, abstractmethod

from src.models.market import MarketQuote


class BaseCollector(ABC):
    """Contrato común para todos los proveedores de cotizaciones."""

    @abstractmethod
    def connect(self) -> None:
        """Inicia la conexión con la fuente de datos."""

    @abstractmethod
    def disconnect(self) -> None:
        """Cierra la conexión con la fuente de datos."""

    @abstractmethod
    def get_quotes(self) -> list[MarketQuote]:
        """Obtiene las cotizaciones disponibles."""
