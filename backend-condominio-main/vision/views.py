# vision/views.py
from rest_framework import viewsets, filters, permissions
from django.utils.dateparse import parse_datetime
from .models import Zona, Camara, DeteccionIA
from .serializers import (
    ZonaSerializer,
    CamaraReadSerializer, CamaraWriteSerializer,
    DeteccionIAReadSerializer, DeteccionIAWriteSerializer
)

# ---------- ZONAS ----------
class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all().order_by("nombre")
    serializer_class = ZonaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "ubicacion"]
    ordering_fields = ["nombre", "estado", "id"]
    ordering = ["nombre"]


# ---------- DETECCIONES IA ----------
class DeteccionIAViewSet(viewsets.ModelViewSet):
    queryset = DeteccionIA.objects.select_related('camara', 'camara__zona', 'camara__areacomun').all().order_by('-fechaHora')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['evidencia', 'nivel_riesgo', 'incidencia', 'camara__zona__nombre', 'camara__areacomun__nombre']
    ordering_fields = ['fechaHora', 'confianza', 'id']
    ordering = ['-fechaHora']

    def get_serializer_class(self):
        return DeteccionIAReadSerializer if self.action in ['list', 'retrieve'] else DeteccionIAWriteSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # ?camara=ID
        camara_id = self.request.query_params.get('camara')
        if camara_id:
            qs = qs.filter(camara_id=camara_id)

        # ?nivel_riesgo=bajo|medio|alto|critico
        nivel = self.request.query_params.get('nivel_riesgo')
        if nivel:
            qs = qs.filter(nivel_riesgo=nivel)

        # ?incidencia=robo|vandalismo|incendio|otro
        incidencia = self.request.query_params.get('incidencia')
        if incidencia:
            qs = qs.filter(incidencia=incidencia)

        # ?evidencia=imagen|video|audio|otro
        evidencia = self.request.query_params.get('evidencia')
        if evidencia:
            qs = qs.filter(evidencia=evidencia)

        # ?min_confianza=0.8  | ?max_confianza=0.95
        min_conf = self.request.query_params.get('min_confianza')
        if min_conf is not None:
            try:
                qs = qs.filter(confianza__gte=float(min_conf))
            except ValueError:
                pass

        max_conf = self.request.query_params.get('max_confianza')
        if max_conf is not None:
            try:
                qs = qs.filter(confianza__lte=float(max_conf))
            except ValueError:
                pass

        # Rango de fecha/hora (ISO 8601): ?desde=2025-09-18T00:00:00Z&hasta=2025-09-19T23:59:59Z
        desde = self.request.query_params.get('desde')
        if desde:
            dt_from = parse_datetime(desde)
            if dt_from:
                qs = qs.filter(fechaHora__gte=dt_from)

        hasta = self.request.query_params.get('hasta')
        if hasta:
            dt_to = parse_datetime(hasta)
            if dt_to:
                qs = qs.filter(fechaHora__lte=dt_to)

        return qs


# ---------- CAMARAS ----------
class CamaraViewSet(viewsets.ModelViewSet):
    queryset = Camara.objects.select_related('zona', 'areacomun').all().order_by('id')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['zona__nombre', 'areacomun__nombre', 'estado']
    ordering_fields = ['id', 'estado', 'zona__nombre', 'areacomun__nombre']
    ordering = ['id']

    def get_serializer_class(self):
        return CamaraReadSerializer if self.action in ['list', 'retrieve'] else CamaraWriteSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # ?zona=ID
        zona = self.request.query_params.get('zona')
        if zona:
            qs = qs.filter(zona_id=zona)

        # ?areacomun=ID
        areacomun = self.request.query_params.get('areacomun')
        if areacomun:
            qs = qs.filter(areacomun_id=areacomun)

        # ?estado=disponible|ocupada|mantenimiento
        estado = self.request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)

        return qs
