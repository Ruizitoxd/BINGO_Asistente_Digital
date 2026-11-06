from fastapi import APIRouter, Request

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("")
async def list_modules(request: Request) -> dict[str, list[str]]:
    return {"modules": request.app.state.module_registry.list_modules()}
