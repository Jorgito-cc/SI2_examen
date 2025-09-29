# notificaciones/urls.py
from rest_framework.routers import DefaultRouter
from .views import NotificacionViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'notificaciones', NotificacionViewSet, basename='notificacion')

urlpatterns = [
    path('', include(router.urls)),
]