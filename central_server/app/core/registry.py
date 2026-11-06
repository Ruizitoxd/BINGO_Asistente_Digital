from app.core.module import JarvisModule


class ModuleRegistry:
    """Registro de módulos y administración de su ciclo de vida."""

    def __init__(self) -> None:
        self._modules: dict[str, JarvisModule] = {}
        self._initialized: list[str] = []

    def register(self, module: JarvisModule) -> None:
        name = module.name.strip()
        if not name:
            raise ValueError("El nombre del módulo no puede estar vacío.")
        if name in self._modules:
            raise ValueError(f"El módulo '{name}' ya está registrado.")
        self._modules[name] = module

    def get(self, name: str) -> JarvisModule:
        if name not in self._modules:
            raise KeyError(f"No existe el módulo '{name}'.")
        return self._modules[name]

    def list_modules(self) -> list[str]:
        return sorted(self._modules)

    async def initialize_all(self) -> None:
        try:
            for name, module in self._modules.items():
                await module.initialize()
                self._initialized.append(name)
        except Exception:
            await self.shutdown_all()
            raise

    async def shutdown_all(self) -> None:
        errors = []
        while self._initialized:
            name = self._initialized.pop()
            try:
                await self._modules[name].shutdown()
            except Exception as exc:
                errors.append(exc)
        if errors:
            raise RuntimeError(
                f"{len(errors)} módulo(s) no pudieron apagarse correctamente."
            ) from errors[0]
