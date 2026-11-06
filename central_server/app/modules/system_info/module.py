from typing import Any
from app.core.module import JarvisModule


class SystemInfoModule(JarvisModule):
    @property
    def name(self) -> str:
        return "system_info"

    async def initialize(self) -> None:
        return None

    def get_tools(self) -> list[dict[str, Any]]:
        return [{
            "name": "get_server_status",
            "description": "Consulta el estado básico del servidor.",
            "permission": "system.read",
        }]

    async def shutdown(self) -> None:
        return None
