# urls.py del app (por ejemplo areas/urls.py)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AreaComunViewSet

router = DefaultRouter()
router.register(r'areas-comunes', AreaComunViewSet, basename='area-comun')

urlpatterns = [
    path('', include(router.urls)),
]
