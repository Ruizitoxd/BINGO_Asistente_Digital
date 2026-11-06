# JARVIS — Fase 1

Esqueleto inicial del servidor central para Windows 11. Incluye configuración,
contratos Pydantic, interfaz y registro de módulos, API FastAPI y pruebas.

## Requisitos
Python 3.11 o superior.

## Instalar (PowerShell, desde `central_server`)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
```

## Ejecutar
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Abrir `http://127.0.0.1:8000/docs`. Endpoints: `/health` y `/api/v1/modules`.
El host local es intencional: no exponer a la red antes de implementar
autenticación y conectividad segura.

## Pruebas
```powershell
pytest
```

## Añadir un módulo
Crear un paquete en `app/modules/`, implementar `JarvisModule` y registrarlo
en `app/bootstrap.py`. Cada módulo implementa `name`, `initialize`,
`get_tools` y `shutdown`.

Esta fase no implementa todavía autenticación, base de datos, IA, WebSocket,
agentes Windows/Android ni ejecución de acciones del sistema.
