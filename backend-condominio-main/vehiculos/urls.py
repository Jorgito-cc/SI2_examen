from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoViewSet, AccesoQRViewSet, CrearVehiculoUsuarioView

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'accesos', AccesoQRViewSet, basename='accesoqr')

urlpatterns = [
    # CRUD de vehículos y QR
    path('', include(router.urls)),
    # extra: crear vehículo + usuario
    path('vehiculos/crear/', CrearVehiculoUsuarioView.as_view(), name='vehiculo-crear-usuario'),
]
