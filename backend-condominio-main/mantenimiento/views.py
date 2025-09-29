from rest_framework import viewsets
from .models import Mantenimiento, Servicio
from .serializers import (
    MantenimientoSerializer,
    ServiciosSerializer,
)
from rest_framework.permissions import IsAuthenticated


class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer


class ServiciosViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServiciosSerializer
    permission_classes = [IsAuthenticated]  # opcional
