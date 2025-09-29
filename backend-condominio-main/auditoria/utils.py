from .models import Bitacora

def _get_ip(request):
    return (request.META.get("HTTP_X_FORWARDED_FOR") or
            request.META.get("REMOTE_ADDR") or "").split(",")[0].strip()

def log_action(user, accion, request=None, extra=""):
    """
    Uso: log_action(request.user, "Creó unidad", request, extra="B=A|N=12")
    """
    try:
        ip = path = ua = ""
        if request:
            ip = _get_ip(request)
            path = request.path
            ua = request.META.get("HTTP_USER_AGENT", "")[:255]
        Bitacora.objects.create(
            usuario=user if user and user.is_authenticated else None,
            accion=str(accion)[:255],
            detalle=extra or "",
            ip=ip or None,
            path=path or "",
            user_agent=ua or "",
        )
    except Exception:
        # Nunca romper la request por el log
        pass


