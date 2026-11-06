from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.database.connection import Database
from app.security.tokens import verify_token

router = APIRouter(tags=["realtime"])
@router.websocket("/ws")
async def device_socket(websocket: WebSocket):
    token = websocket.query_params.get("token", "")
    db = Database()
    with db.connect() as conn:
        rows = conn.execute("SELECT device_id,token_hash FROM devices WHERE is_active=1").fetchall()
    identity = next((r["device_id"] for r in rows if verify_token(token, r["token_hash"])), None)
    if not identity:
        await websocket.close(code=1008, reason="No autorizado")
        return
    await websocket.accept()
    try:
        await websocket.send_json({"type": "connection.ready", "device_id": identity})
        while True:
            message = await websocket.receive_json()
            await websocket.send_json({"type": "message.received", "echo": message})
    except WebSocketDisconnect:
        pass
