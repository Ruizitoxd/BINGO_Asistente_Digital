# Fase 1 — Fundamentos

- Servidor central alojado inicialmente en el portátil Windows 11.
- Monolito modular con FastAPI.
- Contratos Pydantic con versión de esquema.
- Módulos implementan `BingoModule` y se registran en `app/bootstrap.py`.
- API versionada bajo `/api/v1`.
- Desarrollo limitado a `127.0.0.1` hasta implementar autenticación y acceso remoto.

No se implementan todavía autenticación real, base de datos, IA, WebSocket,
agente Windows, cliente Android ni ejecución de herramientas del sistema.
