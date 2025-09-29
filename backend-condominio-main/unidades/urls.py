from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UnidadHabitacionalViewSet, ResidenteUnidadViewSet,MascotaViewSet, IntegranteViewSet, VisitaViewSet

router = DefaultRouter()
router.register(r"unidades", UnidadHabitacionalViewSet, basename="unidad")
router.register(r"residentes-unidades", ResidenteUnidadViewSet, basename="residente-unidad")
router.register(r'mascotas', MascotaViewSet)
router.register(r'integrantes', IntegranteViewSet)
router.register(r'visitas', VisitaViewSet)


urlpatterns = [
    path("", include(router.urls)),
]


