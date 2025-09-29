from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone


# ---------- TABLA ROL ----------
class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "rol"
        verbose_name_plural = "roles"

    def __str__(self):
        return self.nombre


# ---------- CHOICES / ENUMS ----------
class EstadoUsuario(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    INACTIVO = "INACTIVO", "Inactivo"
    BLOQUEADO = "BLOQUEADO", "Bloqueado"


# ---------- TABLA USUARIO ----------
class Usuario(AbstractUser):
    # AbstractUser ya trae: username, password, first_name, last_name, email, is_staff, is_superuser...
    ci = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100, blank=True)            # extra a first_name/last_name si quieres
    telefono = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=20, choices=EstadoUsuario.choices, default=EstadoUsuario.ACTIVO)
    url_img = models.URLField(blank=True)
    # Mejor JSONField si guardarás embeddings/rasgos
    registro_facial = models.JSONField(blank=True, null=True)        # en vez de TextField
    carnet = models.CharField(max_length=50, blank=True)


    url_img = models.URLField(blank=True) # ✅ Este campo es el importante ✅


    # muchos-a-muchos con tabla intermedia explícita
    roles = models.ManyToManyField("authx.Rol", through="authx.RolUsuario", related_name="usuarios")

    class Meta:
        indexes = [
            models.Index(fields=["estado"]),
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
        ]
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.get_full_name() or self.username or self.email or f"Usuario {self.pk}"
#--------------------------------------------------------------------------------------------------------------
 # ----- Helpers de rol (opcionales, muy prácticos) -----
    def has_role(self, *names: str) -> bool:
        """
        Devuelve True si el usuario tiene alguno de los roles indicados por nombre.
        Ej: user.has_role('ADMINISTRADOR','GUARDIA')
        """
        my_roles = set(self.roles.values_list("nombre", flat=True))
        return self.is_staff or any(r in my_roles for r in names)

    @property
    def es_admin(self):       return self.is_staff or self.has_role("ADMINISTRADOR")
    @property
    def es_guardia(self):     return self.has_role("GUARDIA")
    @property
    def es_personal(self):    return self.has_role("PERSONAL")
    @property
    def es_propietario(self): return self.has_role("PROPIETARIO")
    @property
    def es_inquilino(self):   return self.has_role("INQUILINO")

    @property
    def perfil(self):
        """
        Retorna el perfil relacionado según rol (Personal/Residente) si existe.
        """
        if self.es_guardia or self.es_personal:
            return getattr(self, "personal", None)
        if self.es_propietario or self.es_inquilino:
            return getattr(self, "residente", None)
        return None





# ---------- TABLA INTERMEDIA USUARIO-ROL ----------
class RolUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario_roles")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name="rol_usuarios")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["usuario", "rol"], name="uniq_usuario_rol")
        ]
        verbose_name = "rol de usuario"
        verbose_name_plural = "roles de usuario"

    def __str__(self):
        return f"{self.usuario} → {self.rol}"


# ---------- RESET DE CONTRASEÑA ----------
class PasswordResetCode(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pwd_resets")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["usuario", "used"]),
            models.Index(fields=["created_at"]),
        ]
        # En PostgreSQL puedes asegurar un solo código activo por usuario:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario"],
                condition=models.Q(used=False),
                name="uniq_active_reset_per_user",
            )
        ]
        verbose_name = "código de reset"
        verbose_name_plural = "códigos de reset"

    def is_valid(self):
        return (not self.used) and timezone.now() <= self.expires_at

    def __str__(self):
        estado = "USED" if self.used else "OK"
        return f"{self.usuario} - {self.code} - {estado}"


# ---------- PERSONAL ----------
class Personal(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="personal")
    ocupacion = models.CharField(max_length=100)
    horario_entrada = models.TimeField()
    horario_salida = models.TimeField()

    class Meta:
        verbose_name = "personal"
        verbose_name_plural = "personal"

    def __str__(self):
        return f"{self.ocupacion} - {self.usuario}"


# ---------- RESIDENTE ----------
class Residente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="residente")
    # agrega aquí campos extra si el residente necesita info distinta al usuario

    class Meta:
        verbose_name = "residente"
        verbose_name_plural = "residentes"

    def __str__(self):
        return f"Residente: {self.usuario}"   # 
