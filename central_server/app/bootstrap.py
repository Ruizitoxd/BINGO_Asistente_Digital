from app.core.registry import ModuleRegistry
from app.modules.system_info.module import SystemInfoModule


def create_module_registry() -> ModuleRegistry:
    registry = ModuleRegistry()
    registry.register(SystemInfoModule())
    return registry
