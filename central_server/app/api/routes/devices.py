import secrets
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from app.core.config import get_settings
from app.database.connection import Database
from app.database.repositories import DeviceRepository, AuditRepository
from app.schemas.contracts import DeviceDescriptor
from app.security.dependencies import get_database, require_device
from app.security.tokens import issue_token

router = APIRouter(prefix="/devices", tags=["devices"])
class EnrollmentRequest(BaseModel):
    enrollment_secret: str
    device: DeviceDescriptor

@router.post("/register")
async def register_device(payload: EnrollmentRequest, db: Database = Depends(get_database)):
    settings = get_settings()
    if not secrets.compare_digest(payload.enrollment_secret, settings.enrollment_secret):
        raise HTTPException(status_code=403, detail="Secreto de registro incorrecto")
    token = issue_token()
    try:
        DeviceRepository(db).register(payload.device, token)
    except Exception as exc:
        if "UNIQUE constraint failed" in str(exc):
            raise HTTPException(status_code=409, detail="El dispositivo ya está registrado")
        raise
    AuditRepository(db).record(payload.device.device_id, "device.register", "Dispositivo registrado")
    return {"device_id": payload.device.device_id, "access_token": token, "token_type": "bearer", "warning": "Guarda este token; no se vuelve a mostrar."}

@router.get("")
async def list_devices(_device=Depends(require_device), db: Database = Depends(get_database)):
    return {"devices": DeviceRepository(db).list()}
