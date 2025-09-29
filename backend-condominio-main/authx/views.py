import random
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from core.permissions import HasAnyRole
from core.mixins import OwnerScopedQuerysetMixin
from core.viewsets import BaseOwnedModelViewSet

from .models import Rol, PasswordResetCode, Personal, Residente
from .serializers import (
    RolSerializer,
    UsuarioReadSerializer,
    UsuarioWriteSerializer,
    PersonalCreateSerializer,
    PersonalReadSerializer, # AÑADI ESTE NUEVO: Importación del serializador de lectura para Personal.
    ResidenteUpsertSerializer as ResidenteSerializer
)

Usuario = get_user_model()


# -----------------------------
# CRUD Roles (solo admin)
# -----------------------------
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all().order_by("nombre")
    serializer_class = RolSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre"]
    ordering_fields = ["nombre", "id"]


# -----------------------------
# CRUD Usuarios
#   - Admin: CRUD completo
#   - Endpoint /me: cualquier autenticado ve su propio perfil
# -----------------------------
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by("id")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["id", "username", "email"]

    # Admin usa Write/Read serializers; users normales solo acceden a /me
    def get_permissions(self):
        if self.action == "me":
            return [permissions.IsAuthenticated()]
        # resto admin only
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "me"]:
            return UsuarioReadSerializer
        return UsuarioWriteSerializer

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        ser = UsuarioReadSerializer(request.user, context={"request": request})
        return Response(ser.data)


# -----------------------------
# JWT Login / Refresh / Logout
# -----------------------------
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class RefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh = request.data.get("refresh")
            if not refresh:
                return Response({"detail": "Falta refresh token"}, status=400)
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"detail": "Logout ok"})
        except Exception:
            return Response({"detail": "Token inválido"}, status=400)


# -----------------------------
# Reset de contraseña
# -----------------------------
def _gen_code():
    return f"{random.randint(0, 999999):06d}"


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username_or_email = request.data.get("username") or request.data.get("email")
        if not username_or_email:
            return Response({"detail": "username o email requerido"}, status=400)
        try:
            user = (
                Usuario.objects.filter(email=username_or_email).first()
                or Usuario.objects.filter(username=username_or_email).first()
            )
            # No reveles si existe o no
            if not user:
                return Response({"detail": "Si el usuario existe, se envió un código"}, status=200)

            code = _gen_code()
            expires = timezone.now() + timedelta(minutes=15)
            PasswordResetCode.objects.create(usuario=user, code=code, expires_at=expires)

            send_mail(
                "Código de restablecimiento",
                f"Tu código es: {code} (expira en 15 min)",
                "no-reply@condominio.local",
                [user.email] if user.email else [],
                fail_silently=True,
            )
            return Response({"detail": "Si el usuario existe, se envió un código"}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        code = request.data.get("code")
        new_password = request.data.get("new_password")
        if not (username and code and new_password):
            return Response({"detail": "username, code y new_password requeridos"}, status=400)

        user = Usuario.objects.filter(username=username).first()
        if not user:
            return Response({"detail": "Datos inválidos"}, status=400)

        pr = (
            PasswordResetCode.objects.filter(usuario=user, code=code, used=False)
            .order_by("-created_at")
            .first()
        )
        if not pr or not pr.is_valid():
            return Response({"detail": "Código inválido o expirado"}, status=400)

        user.set_password(new_password)
        user.save()
        pr.used = True
        pr.save(update_fields=["used"])
        return Response({"detail": "Contraseña actualizada"})


# -----------------------------
# Personal
#   - ADMIN/GAURDIA/PERSONAL: acceso
#   - Admin ve todo; el resto “solo lo suyo” gracias al mixin
# -----------------------------
class PersonalViewSet(OwnerScopedQuerysetMixin, BaseOwnedModelViewSet):
    queryset = Personal.objects.select_related("usuario").all()
    # AÑADI ESTE NUEVO: Método para cambiar dinámicamente el serializador.
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PersonalReadSerializer  # Usar el serializador para la lectura
        return PersonalCreateSerializer  # Usar el serializador para la escritura

    permission_classes = [
        permissions.IsAuthenticated,
        HasAnyRole.as_perm("ADMINISTRADOR", "GUARDIA", "PERSONAL"),
    ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["usuario__username", "usuario__email", "ocupacion"]
    ordering_fields = ["id", "ocupacion", "usuario__username"]


# -----------------------------
# Residente
#   - ADMIN/PROPIETARIO/INQUILINO: acceso
#   - Admin ve todo; propietarios/inq. solo su propio registro
# -----------------------------
class ResidenteViewSet(OwnerScopedQuerysetMixin, BaseOwnedModelViewSet):
    queryset = Residente.objects.select_related("usuario").all()
    serializer_class = ResidenteSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasAnyRole.as_perm("ADMINISTRADOR", "PROPIETARIO", "INQUILINO"),
    ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["usuario__username", "usuario__email"]
    ordering_fields = ["id", "usuario__username", "usuario__email"]