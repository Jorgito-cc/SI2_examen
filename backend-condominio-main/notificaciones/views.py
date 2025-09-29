from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notificacion
from .serializers import NotificacionSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    """
    Reglas:
      - Admin (is_staff=True): puede ver TODAS, crear para cualquiera, editar/borrar cualquiera.
      - Usuario autenticado NO admin: solo ve/crea/edita/borrar SUS notificaciones.
        (al crear, se fuerza usuario=request.user)
    Filtros:
      - ?search=texto (titulo, descripcion, poligono)
      - ?leido=true|false
    Orden:
      - ?ordering=-creado_en (default)
    Acciones:
      - POST /notificaciones/{id}/marcar_leida/
      - POST /notificaciones/{id}/marcar_no_leida/
      - GET  /notificaciones/mias/   (alias del list ya filtrado por user, útil si quieres endpoint explícito)
    """
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descripcion', 'poligono', 'usuario__username', 'usuario__email']
    ordering_fields = ['creado_en', 'titulo', 'leido', 'id']
    ordering = ['-creado_en']

    def get_queryset(self):
        qs = Notificacion.objects.select_related('usuario').all()
        user = self.request.user

        # Admin ve todo; usuario normal solo lo suyo
        if not user.is_staff:
            qs = qs.filter(usuario=user)

        # filtro por leido=true/false opcional
        leido = self.request.query_params.get('leido')
        if leido in ('true', 'false'):
            qs = qs.filter(leido=(leido == 'true'))

        return qs

    def perform_create(self, serializer):
        user = self.request.user
        # Si no es admin, IGNORAR usuario_id del payload y asignar el propio
        if not user.is_staff:
            serializer.save(usuario=user)
        else:
            # Admin puede enviar usuario_id en el payload
            serializer.save()

    def perform_update(self, serializer):
        """
        Evita que un usuario normal reasigne la notificación a otro usuario al actualizar.
        """
        instance = self.get_object()
        user = self.request.user
        if not user.is_staff:
            serializer.save(usuario=instance.usuario)
        else:
            serializer.save()

    # ----- Acciones personalizadas -----

    @action(detail=False, methods=['get'], url_path='mias')
    def mias(self, request):
        """
        Alias explícito: devuelve solo las notificaciones del usuario actual (ya es el comportamiento por defecto para no-admin).
        """
        queryset = self.filter_queryset(self.get_queryset()).filter(usuario=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(queryset, many=True)
        return Response(ser.data)

    @action(detail=True, methods=['post'], url_path='marcar_leida')
    def marcar_leida(self, request, pk=None):
        n = self.get_object()
        # Si no es admin, solo puede marcar la suya
        if not request.user.is_staff and n.usuario_id != request.user.id:
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)
        if not n.leido:
            n.leido = True
            n.save(update_fields=['leido'])
        return Response(self.get_serializer(n).data)

    @action(detail=True, methods=['post'], url_path='marcar_no_leida')
    def marcar_no_leida(self, request, pk=None):
        n = self.get_object()
        if not request.user.is_staff and n.usuario_id != request.user.id:
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)
        if n.leido:
            n.leido = False
            n.save(update_fields=['leido'])
        return Response(self.get_serializer(n).data)
