import sqlite3
from pathlib import Path
from contextlib import contextmanager
from app.core.config import get_settings

SCHEMA = '''
CREATE TABLE IF NOT EXISTS devices (
 device_id TEXT PRIMARY KEY, device_type TEXT NOT NULL, display_name TEXT NOT NULL,
 protocol_version TEXT NOT NULL, token_hash TEXT NOT NULL, created_at TEXT NOT NULL,
 last_seen_at TEXT, is_active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS conversations (
 id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT NOT NULL, role TEXT NOT NULL,
 content TEXT NOT NULL, created_at TEXT NOT NULL,
 FOREIGN KEY(device_id) REFERENCES devices(device_id)
);
CREATE TABLE IF NOT EXISTS audit_log (
 id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT, action TEXT NOT NULL,
 detail TEXT NOT NULL, created_at TEXT NOT NULL
);
'''

class Database:
    def __init__(self, path: str | None = None):
        self.path = path or get_settings().database_path
    @contextmanager
    def connect(self):
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    def initialize(self):
        with self.connect() as conn:
            conn.executescript(SCHEMA)
