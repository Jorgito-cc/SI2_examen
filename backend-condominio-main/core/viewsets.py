from rest_framework import viewsets, permissions, filters
from .permissions import IsOwnerOrAdmin


class BaseOwnedModelViewSet(viewsets.ModelViewSet):
    """
    Base para recursos que tienen un dueño.
    - Usa IsOwnerOrAdmin para proteger objetos.
    - Incluye filtros de búsqueda y ordenamiento.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
