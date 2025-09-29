from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters,status
from .models import Cuota ,Reserva , Factura
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
# reservas/views.py
from django.utils.dateparse import parse_date, parse_datetime
from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError
from .serializers import (
    CuotaSerializer,
    ReservaReadSerializer,
    ReservaWriteSerializer,
    FacturaSerializer
)
from django_filters.rest_framework import DjangoFilterBackend








#--------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
class CuotaViewSet(viewsets.ModelViewSet):
    """
    CRUD de Cuotas/Multas (una sola tabla con tipo_cuota = CUOTA | MULTA)
    Filtros por query params:
      - ?unidad=ID
      - ?periodo=YYYY-MM
      - ?estado=EMITIDA|VENCIDA|PAGADA|PARCIAL|ANULADA
      - ?tipo_cuota=CUOTA|MULTA
      - ?desde=YYYY-MM-DD  &  ?hasta=YYYY-MM-DD (rango sobre fecha_a_pagar)
    Búsqueda y orden:
      - ?search=<texto en descripcion>
      - ?ordering=periodo  | -periodo | fecha_a_pagar | -fecha_a_pagar | cantidad_pago ...
    """
    queryset = Cuota.objects.select_related('unidad').all().order_by('-fecha_a_pagar', '-id')
    serializer_class = CuotaSerializer
    permission_classes = [permissions.IsAuthenticated]  # o IsAuthenticatedOrReadOnly si quieres lectura pública
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['descripcion', 'unidad__numero', 'unidad__bloque']
    ordering_fields = ['id', 'cantidad_pago', 'periodo', 'fecha_a_pagar', 'fecha_vencimiento', 'estado']

    def get_queryset(self):
        qs = super().get_queryset()
        qp = self.request.query_params

        unidad = qp.get('unidad')
        if unidad:
            qs = qs.filter(unidad_id=unidad)

        periodo = qp.get('periodo')
        if periodo:
            qs = qs.filter(periodo=periodo)

        estado = qp.get('estado')
        if estado:
            qs = qs.filter(estado=estado)

        tipo = qp.get('tipo_cuota')
        if tipo:
            qs = qs.filter(tipo_cuota=tipo)

        # Rango por fecha_a_pagar
        desde = qp.get('desde')
        if desde:
            d = parse_date(desde)
            if d:
                qs = qs.filter(fecha_a_pagar__gte=d)

        hasta = qp.get('hasta')
        if hasta:
            d = parse_date(hasta)
            if d:
                qs = qs.filter(fecha_a_pagar__lte=d)

        return qs



# ============================================================================================================
# Reserva (áreas comunes)=====================================================================================
# ==============================================================================================================
class ReservaViewSet(viewsets.ModelViewSet):
    """
    Reservas con exclusión de solapes a nivel BD (ExclusionConstraint).
    Filtros por query params:
      - estado, estado__in (coma-separado), areacomun, usuario
      - fecha_inicio__gte / __lte (ISO 8601)
      - fecha_fin__gte / __lte (ISO 8601)
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["nombre", "horario"]
    ordering_fields = ["fecha_inicio", "fecha_fin", "id", "estado"]
    ordering = ["-fecha_inicio", "-id"]

    def get_queryset(self):
        qs = (
            Reserva.objects
            .select_related("areacomun", "usuario", "aprobado_por")
            .all()
            .order_by(*self.ordering)
        )

        p = self.request.query_params

        # Filtros simples
        if (v := p.get("estado")):
            qs = qs.filter(estado=v)
        if (v := p.get("estado__in")):
            estados = [s.strip().upper() for s in v.split(",") if s.strip()]
            if estados:
                qs = qs.filter(estado__in=estados)

        if (v := p.get("areacomun")):
            qs = qs.filter(areacomun_id=v)
        if (v := p.get("usuario")):
            qs = qs.filter(usuario_id=v)

        # Rango de fechas (ISO 8601 en UTC o con tz)
        if (v := p.get("fecha_inicio__gte")):
            dt = parse_datetime(v)
            if dt is None:
                raise ValidationError({"fecha_inicio__gte": "Formato inválido. Usa ISO 8601 p.ej. 2025-09-25T18:00:00Z"})
            qs = qs.filter(fecha_inicio__gte=dt)

        if (v := p.get("fecha_inicio__lte")):
            dt = parse_datetime(v)
            if dt is None:
                raise ValidationError({"fecha_inicio__lte": "Formato inválido. Usa ISO 8601 p.ej. 2025-09-25T20:00:00Z"})
            qs = qs.filter(fecha_inicio__lte=dt)

        if (v := p.get("fecha_fin__gte")):
            dt = parse_datetime(v)
            if dt is None:
                raise ValidationError({"fecha_fin__gte": "Formato inválido. Usa ISO 8601."})
            qs = qs.filter(fecha_fin__gte=dt)

        if (v := p.get("fecha_fin__lte")):
            dt = parse_datetime(v)
            if dt is None:
                raise ValidationError({"fecha_fin__lte": "Formato inválido. Usa ISO 8601."})
            qs = qs.filter(fecha_fin__lte=dt)

        return qs

    def get_serializer_class(self):
        return ReservaReadSerializer if self.action in ["list", "retrieve"] else ReservaWriteSerializer

    # ---- Persistencia con manejo de solapes (constraint) ----
    def perform_create(self, serializer):
        # Si no quieres que el cliente mande 'usuario' en el payload:
        if "usuario" not in serializer.validated_data and self.request.user.is_authenticated:
            serializer.validated_data["usuario"] = self.request.user

        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            # Violación del ExclusionConstraint (solape en areacomun horario/rango)
            raise ValidationError("Conflicto: existe una reserva activa que se solapa en esa área y rango.")

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise ValidationError("Conflicto: el nuevo rango se solapa con otra reserva activa del área.")
        
        
        
        
#--------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
# facturacion/views.py

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Lectura para autenticados; escritura solo staff (ajústalo a tu gusto).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = (
        Factura.objects
        .select_related("usuario", "unidad", "reserva", "cuota")
        .all()
        .order_by("-created_at")
    )
    serializer_class = FacturaSerializer
    permission_classes = [IsStaffOrReadOnly]

    # Búsqueda / filtros / orden
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "estado": ["exact", "in"],
        "tipo_pago": ["exact", "in"],
        "fecha": ["exact", "gte", "lte"],
        "usuario": ["exact"],
        "unidad": ["exact"],
        "reserva": ["exact"],
        "cuota": ["exact"],
    }
    search_fields = ["numero", "serie", "nit", "razon_social", "observaciones"]
    ordering_fields = ["fecha", "created_at", "total"]

    # Acciones útiles (opcionales)
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def anular(self, request, pk=None):
        """
        Marca la factura como ANULADA (si no está pagada).
        """
        factura = self.get_object()
        if factura.estado == Factura.Estado.PAGADA:
            return Response(
                {"detail": "No puedes anular una factura pagada."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        factura.estado = Factura.Estado.ANULADA
        factura.save()
        return Response(self.get_serializer(factura).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def marcar_pagada(self, request, pk=None):
        """
        Marca la factura como PAGADA manualmente (útil si no tienes aún el flujo de Pago).
        """
        factura = self.get_object()
        if factura.estado == Factura.Estado.ANULADA:
            return Response(
                {"detail": "No puedes pagar una factura anulada."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        factura.estado = Factura.Estado.PAGADA
        factura.save()
        return Response(self.get_serializer(factura).data)


