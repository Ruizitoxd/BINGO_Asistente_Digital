from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.database.connection import Database
from app.security.tokens import verify_token

bearer = HTTPBearer(auto_error=False)

def get_database() -> Database:
    return Database()

async def require_device(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Database = Depends(get_database)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Falta el token Bearer")
    with db.connect() as conn:
        rows = conn.execute("SELECT device_id, token_hash, is_active FROM devices").fetchall()
    for row in rows:
        if row["is_active"] and verify_token(credentials.credentials, row["token_hash"]):
            return {"device_id": row["device_id"]}
    raise HTTPException(status_code=401, detail="Token inválido o dispositivo desactivado")
