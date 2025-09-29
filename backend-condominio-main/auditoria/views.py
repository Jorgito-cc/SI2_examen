from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Bitacora
from .serializers import BitacoraSerializer

class BitacoraViewSet(ReadOnlyModelViewSet):
    """
    /api/bitacora/         -> lista (solo admin)
    /api/bitacora/{id}/    -> detalle (solo admin)
    /api/bitacora/mias/    -> mis logs (usuario autenticado)
    Soporta filtros por ?q=texto&desde=YYYY-MM-DD&hasta=YYYY-MM-DD
    """
    queryset = Bitacora.objects.select_related("usuario").all()
    serializer_class = BitacoraSerializer
    permission_classes = [IsAdminUser]
    search_fields = ["accion", "detalle", "path", "usuario__username", "usuario__email"]
    ordering = ["-creado_en"]

    def get_queryset(self):
        qs = super().get_queryset()

        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(accion__icontains=q) | qs.filter(detalle__icontains=q) | qs.filter(path__icontains=q)

        desde = self.request.query_params.get("desde")
        hasta = self.request.query_params.get("hasta")
        def to_dt(s):
            try:
                return make_aware(datetime.strptime(s, "%Y-%m-%d"))
            except Exception:
                return None
        if desde:
            d = to_dt(desde)
            if d: qs = qs.filter(creado_en__date__gte=d.date())
        if hasta:
            h = to_dt(hasta)
            if h: qs = qs.filter(creado_en__date__lte=h.date())
        return qs

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def mias(self, request):
        qs = self.get_queryset().filter(usuario=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

