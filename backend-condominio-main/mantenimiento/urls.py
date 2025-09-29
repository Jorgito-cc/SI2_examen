from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MantenimientoViewSet, ServiciosViewSet

router = DefaultRouter()
router.register(r'mantenimientos', MantenimientoViewSet)
router.register(r'servicios', ServiciosViewSet)  # URL del paquete


urlpatterns = [
    path('', include(router.urls)),
]

 