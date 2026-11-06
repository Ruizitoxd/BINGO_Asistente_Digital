# BINGO — Fase 2: servidor central

## Objetivo
Añadir identidad de dispositivos, persistencia SQLite, coordinación de solicitudes, auditoría y canal WebSocket al scaffold de la Fase 1.

## Componentes
- `security/tokens.py`: emisión de tokens aleatorios y almacenamiento mediante HMAC-SHA256 con pepper.
- `api/routes/devices.py`: registro protegido por secreto de enrolamiento y listado autenticado.
- `database/`: conexión SQLite y tablas `devices`, `conversations`, `audit_log`.
- `services/coordinator.py`: valida módulo/acción contra herramientas registradas; no ejecuta código arbitrario.
- `api/routes/memory.py`: guardar y recuperar mensajes del dispositivo autenticado.
- `api/routes/commands.py`: entrada autenticada al coordinador.
- `api/routes/websocket.py`: conexión persistente autenticada y eco de prueba.

## Instalación (PowerShell)
Desde `central_server`:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
```
Edita `.env` y cambia `BINGO_ENROLLMENT_SECRET` y `BINGO_TOKEN_PEPPER` por valores largos y aleatorios. No compartas ni subas `.env` al repositorio.

## Ejecución
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Abre `http://127.0.0.1:8000/docs`. La base se crea automáticamente en `data/bingo.db`.

## Registrar un dispositivo
Ejemplo PowerShell:
```powershell
$body = @{
  enrollment_secret = "TU_SECRETO_DE_REGISTRO"
  device = @{
    device_id = "windows-laptop"
    device_type = "windows"
    display_name = "Portatil Windows 11"
    protocol_version = "1.0"
  }
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/devices/register" -ContentType "application/json" -Body $body
```
La respuesta contiene `access_token`. Guárdalo de forma segura: solo se muestra una vez. Para el teléfono cambia `device_id` a `poco-f7` y `device_type` a `android`.

## Probar memoria
```powershell
$token = "TOKEN_DEL_DISPOSITIVO"
$headers = @{ Authorization = "Bearer $token" }
$entry = @{ role = "user"; content = "Hola BINGO" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/memory" -Headers $headers -ContentType "application/json" -Body $entry
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/api/v1/memory" -Headers $headers
```

## WebSocket
Conecta a `ws://127.0.0.1:8000/ws?token=TOKEN`. El servidor envía `connection.ready` y responde `message.received`. El token en URL es solo una simplificación de prototipo; puede quedar registrado en logs. Antes de uso real se cambiará a autenticación por mensaje inicial/cabecera y WSS.

## API
- `GET /health`: salud básica.
- `GET /api/v1/modules`: módulos registrados.
- `POST /api/v1/devices/register`: enrolamiento con secreto compartido.
- `GET /api/v1/devices`: listado autenticado.
- `POST /api/v1/memory` y `GET /api/v1/memory`: memoria conversacional básica por dispositivo.
- `POST /api/v1/commands`: validación de módulo/acción autenticada.
- `WS /ws?token=...`: canal persistente de prueba.

## Límites y seguridad
- Base de desarrollo local; no exponer a Internet.
- El secreto de enrolamiento es compartido temporalmente; luego se sustituirá por emparejamiento de un solo uso.
- Los tokens se almacenan como hash HMAC y deben guardarse de forma segura en cada cliente.
- No se ejecutan comandos de sistema, código generado por IA ni herramientas reales.
- La memoria aún no tiene cifrado, retención configurable ni búsqueda semántica.
- Mantén `127.0.0.1`; no cambies a `0.0.0.0` todavía.

## Pruebas
```powershell
pytest
```
