"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""#
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),

 # Auth JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # cada app expone sus rutas:
    path('api/', include('authx.urls')),       # login, logout, reset, usuarios, roles
    path('api/', include('unidades.urls')),    # unidades, residentes, residente-unidad
    path('api/', include('auditoria.urls')),   # bitácora
    path('api/', include('mantenimiento.urls')),
    path('api/', include('vehiculos.urls')),
    path('api/', include('notificaciones.urls')),  # 👈 se conecta el módulo
    path('api/', include('amenities.urls')),  # 👈 agrega tu nueva app
    path('api/', include('finanzas.urls')),
    #path('api/', include('vision.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#  path("api/vision/", include("vision.urls")),  # 👈
