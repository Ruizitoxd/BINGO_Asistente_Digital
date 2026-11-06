from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.modules import router as modules_router
from app.bootstrap import create_module_registry
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    registry = create_module_registry()
    app.state.module_registry = registry
    await registry.initialize_all()
    try:
        yield
    finally:
        await registry.shutdown_all()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
    app.include_router(health_router)
    app.include_router(modules_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
