from datetime import datetime, timezone
from app.database.connection import Database
from app.security.tokens import hash_token

def now_iso(): return datetime.now(timezone.utc).isoformat()

class DeviceRepository:
    def __init__(self, db: Database): self.db = db
    def register(self, descriptor, token: str):
        with self.db.connect() as conn:
            conn.execute("INSERT INTO devices(device_id,device_type,display_name,protocol_version,token_hash,created_at) VALUES(?,?,?,?,?,?)",
                (descriptor.device_id, descriptor.device_type.value, descriptor.display_name, descriptor.protocol_version, hash_token(token), now_iso()))
    def authenticate(self, device_id: str):
        with self.db.connect() as conn:
            conn.execute("UPDATE devices SET last_seen_at=? WHERE device_id=?", (now_iso(), device_id))
    def list(self):
        with self.db.connect() as conn:
            return [dict(r) for r in conn.execute("SELECT device_id,device_type,display_name,protocol_version,created_at,last_seen_at,is_active FROM devices ORDER BY created_at").fetchall()]

class MemoryRepository:
    def __init__(self, db: Database): self.db = db
    def add(self, device_id: str, role: str, content: str):
        with self.db.connect() as conn:
            cur = conn.execute("INSERT INTO conversations(device_id,role,content,created_at) VALUES(?,?,?,?)", (device_id, role, content, now_iso()))
            return cur.lastrowid
    def recent(self, device_id: str, limit: int = 20):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT id,role,content,created_at FROM conversations WHERE device_id=? ORDER BY id DESC LIMIT ?", (device_id, limit)).fetchall()
            return [dict(r) for r in reversed(rows)]

class AuditRepository:
    def __init__(self, db: Database): self.db = db
    def record(self, device_id: str | None, action: str, detail: str):
        with self.db.connect() as conn:
            conn.execute("INSERT INTO audit_log(device_id,action,detail,created_at) VALUES(?,?,?,?)", (device_id, action, detail[:2000], now_iso()))
