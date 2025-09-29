from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated  # si quieres proteger las rutas
from .models import UnidadHabitacional, ResidenteUnidad, Mascota, Integrante, Visita
from .serializers import UnidadHabitacionalSerializer, ResidenteUnidadSerializer, MascotaSerializer, IntegranteSerializer, VisitaSerializer


class UnidadHabitacionalViewSet(viewsets.ModelViewSet):
    queryset = UnidadHabitacional.objects.all().order_by("bloque", "numero")
    serializer_class = UnidadHabitacionalSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResidenteUnidadViewSet(viewsets.ModelViewSet):
    queryset = ResidenteUnidad.objects.select_related("residente__usuario", "unidad").all()
    serializer_class = ResidenteUnidadSerializer
    permission_classes = [permissions.IsAuthenticated]


# ----------------- MASCOTA -----------------
class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer
    permission_classes = [IsAuthenticated]  # opcional, si quieres autenticación

# ----------------- INTEGRANTE -----------------
class IntegranteViewSet(viewsets.ModelViewSet):
    queryset = Integrante.objects.all()
    serializer_class = IntegranteSerializer
    permission_classes = [IsAuthenticated]

# ----------------- VISITA -----------------
class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [IsAuthenticated]

