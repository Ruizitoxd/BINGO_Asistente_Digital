from app.schemas.contracts import CommandRequest, CommandResponse, CommandStatus

class Coordinator:
    """Coordina solicitudes sin ejecutar código arbitrario ni acciones del sistema."""
    def __init__(self, registry): self.registry = registry
    async def dispatch(self, request: CommandRequest) -> CommandResponse:
        try:
            module = self.registry.get(request.module)
        except KeyError:
            return CommandResponse(request_id=request.request_id, status=CommandStatus.FAILED, message=f"Módulo no disponible: {request.module}")
        tools = {tool.name: tool for tool in module.get_tools()}
        tool = tools.get(request.action)
        if tool is None:
            return CommandResponse(request_id=request.request_id, status=CommandStatus.FAILED, message=f"Acción no permitida: {request.action}")
        # La fase 2 solo habilita descubrimiento/control; la ejecución real se incorpora con permisos en fases posteriores.
        return CommandResponse(request_id=request.request_id, status=CommandStatus.ACCEPTED, message="Solicitud validada; ejecución aún no habilitada en esta fase.", data={"module": request.module, "action": request.action})
