from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CuotaViewSet,ReservaViewSet,FacturaViewSet

router = DefaultRouter()
router.register(r'cuotas', CuotaViewSet, basename='cuota')
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r"facturas", FacturaViewSet, basename="factura")

urlpatterns = [
    path('', include(router.urls)),
]


