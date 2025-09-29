from rest_framework.permissions import BasePermission


class HasAnyRole(BasePermission):
    """
    Permite acceso si el usuario tiene al menos uno de los roles indicados.
    Uso:
        permission_classes = [IsAuthenticated, HasAnyRole.as_perm('ADMINISTRADOR','GUARDIA')]
    """
    required = ()

    def __init__(self, *roles):
        self.required = roles or self.required

    @classmethod
    def as_perm(cls, *roles):
        class _W(cls):
            def __init__(self):
                super().__init__(*roles)
        return _W

    def has_permission(self, request, view):
        u = request.user
        return bool(
            u and u.is_authenticated and (
                getattr(u, 'is_staff', False) or u.has_role(*self.required)
            )
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Admin (is_staff/es_admin) o propietario del recurso.
    - Busca campos comunes: obj.usuario o obj.propietario
    - También soporta obj.unidad.propietario
    """
    def has_object_permission(self, request, view, obj):
        u = request.user
        if not (u and u.is_authenticated):
            return False

        if getattr(u, 'is_staff', False) or getattr(u, 'es_admin', False):
            return True

        for attr in ('usuario', 'propietario'):
            if hasattr(obj, attr) and getattr(obj, attr) == u:
                return True

        if hasattr(obj, 'unidad') and hasattr(obj.unidad, 'propietario'):
            return obj.unidad.propietario == u

        return False
