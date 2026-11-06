from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.modules import router as modules_router
from app.api.routes.devices import router as devices_router
from app.api.routes.memory import router as memory_router
from app.api.routes.commands import router as commands_router
from app.api.routes.websocket import router as websocket_router
from app.bootstrap import create_module_registry
from app.core.config import get_settings
from app.database.connection import Database
from app.services.coordinator import Coordinator

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database(); db.initialize()
    registry = create_module_registry(); app.state.module_registry = registry
    await registry.initialize_all()
    app.state.coordinator = Coordinator(registry)
    try: yield
    finally: await registry.shutdown_all()

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.2.0", lifespan=lifespan)
    app.include_router(health_router)
    app.include_router(modules_router, prefix=settings.api_v1_prefix)
    app.include_router(devices_router, prefix=settings.api_v1_prefix)
    app.include_router(memory_router, prefix=settings.api_v1_prefix)
    app.include_router(commands_router, prefix=settings.api_v1_prefix)
    app.include_router(websocket_router)
    return app
app = create_app()
