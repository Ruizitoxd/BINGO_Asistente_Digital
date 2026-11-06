from fastapi import APIRouter, Depends, Request
from app.database.connection import Database
from app.database.repositories import AuditRepository
from app.schemas.contracts import CommandRequest
from app.security.dependencies import get_database, require_device

router = APIRouter(prefix="/commands", tags=["commands"])
@router.post("")
async def submit_command(payload: CommandRequest, request: Request, identity=Depends(require_device), db: Database=Depends(get_database)):
    if payload.device_id != identity["device_id"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="No puedes enviar comandos en nombre de otro dispositivo")
    response = await request.app.state.coordinator.dispatch(payload)
    AuditRepository(db).record(identity["device_id"], "command.submit", f"{payload.module}.{payload.action}: {response.status.value}")
    return response
