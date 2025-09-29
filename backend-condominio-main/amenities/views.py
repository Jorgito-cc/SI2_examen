# views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import AreaComun
from .serializers import AreaComunSerializer

class AreaComunViewSet(viewsets.ModelViewSet):
    queryset = AreaComun.objects.all().order_by('id')
    serializer_class = AreaComunSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # búsquedas y orden
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'ubicacion', 'estado', 'descripcion']
    ordering_fields = ['nombre', 'capacidad', 'estado', 'id']
    ordering = ['id']

    # filtro por ?estado=disponible|ocupada|mantenimiento
    def get_queryset(self):
        qs = super().get_queryset()
        estado = self.request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        return qs
