from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RolViewSet,
    UsuarioViewSet,
    PersonalViewSet,
    ResidenteViewSet,
    LoginView,
    RefreshView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# -----------------------------
# Router DRF
# -----------------------------
router = DefaultRouter()
router.register(r"roles", RolViewSet, basename="rol")
router.register(r"usuarios", UsuarioViewSet, basename="usuario")
router.register(r"personal", PersonalViewSet, basename="personal")
router.register(r"residentes", ResidenteViewSet, basename="residente")

# -----------------------------
# URLs principales
# -----------------------------
urlpatterns = [
    path("", include(router.urls)),

    # JWT
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Reset de contraseña
    path("password-reset/request/", PasswordResetRequestView.as_view(), name="pwd_request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="pwd_confirm"),
    
    path('admin/', admin.site.urls),
    path('api/', include('vehiculos.urls')),  # Cambiar 'vehiculos' por el nombre real de tu app
]

