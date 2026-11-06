from abc import ABC, abstractmethod
from typing import Any


class JarvisModule(ABC):
    """Contrato base de los módulos extensibles del servidor."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Identificador único y estable del módulo."""

    @abstractmethod
    async def initialize(self) -> None:
        """Inicializa recursos del módulo."""

    @abstractmethod
    def get_tools(self) -> list[dict[str, Any]]:
        """Devuelve las herramientas que expone el módulo."""

    @abstractmethod
    async def shutdown(self) -> None:
        """Libera recursos del módulo."""
