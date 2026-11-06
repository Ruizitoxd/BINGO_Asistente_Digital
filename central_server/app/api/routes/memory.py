from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.database.connection import Database
from app.database.repositories import MemoryRepository
from app.security.dependencies import get_database, require_device

router = APIRouter(prefix="/memory", tags=["memory"])
class MemoryEntry(BaseModel): role: str = Field(pattern="^(user|assistant|system)$"); content: str = Field(min_length=1, max_length=10000)
@router.post("")
async def save_entry(payload: MemoryEntry, identity=Depends(require_device), db: Database=Depends(get_database)):
    entry_id = MemoryRepository(db).add(identity["device_id"], payload.role, payload.content)
    return {"id": entry_id, "saved": True}
@router.get("")
async def get_entries(limit: int = 20, identity=Depends(require_device), db: Database=Depends(get_database)):
    limit = max(1, min(limit, 100))
    return {"entries": MemoryRepository(db).recent(identity["device_id"], limit)}
