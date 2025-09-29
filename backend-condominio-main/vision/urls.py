# zonas/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ZonaViewSet, DeteccionIAViewSet, CamaraViewSet
#from .api import FaceEnrollAPI, FaceRecognizeAPI

router = DefaultRouter()
router.register(r'zonas', ZonaViewSet, basename='zona')
router.register(r'detecciones', DeteccionIAViewSet, basename='deteccionia')
router.register(r'camaras', CamaraViewSet, basename='camara')

urlpatterns = [
    path('', include(router.urls)),
     #path("face/enroll", FaceEnrollAPI.as_view(), name="face-enroll"),
    #path("face/recognize", FaceRecognizeAPI.as_view(), name="face-recognize"),
]

