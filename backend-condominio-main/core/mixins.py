from django.db.models import Q


class OwnerScopedQuerysetMixin:
    """
    Filtra automáticamente para que un usuario NO admin vea solo sus datos.
    - Campo directo 'usuario'
    - O por unidad (propietario o residente vía 'vinculos.residente.usuario')
    """
    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user

        if not u.is_authenticated or getattr(u, 'is_staff', False) or getattr(u, 'es_admin', False):
            return qs

        model = qs.model
        field_names = {f.name for f in model._meta.fields}

        if 'usuario' in field_names:
            return qs.filter(usuario=u)

        if 'unidad' in field_names:
            return qs.filter(
                Q(unidad__propietario=u) |
                Q(unidad__vinculos__residente__usuario=u)
            ).distinct()

        return qs


class AssignOwnerOnCreateMixin:
    """
    Al crear: si el serializer tiene 'usuario' y no vino en el payload,
    y el usuario no es admin, asigna automáticamente request.user.
    """
    def perform_create(self, serializer):
        u = self.request.user
        if not (getattr(u, 'is_staff', False) or getattr(u, 'es_admin', False)):
            if 'usuario' in serializer.fields and 'usuario' not in serializer.validated_data:
                serializer.save(usuario=u)
                return
        serializer.save()
