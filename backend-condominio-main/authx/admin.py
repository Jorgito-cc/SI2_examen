from django.contrib import admin
from .models import Rol, Usuario, RolUsuario, Personal, Residente, PasswordResetCode

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id","username","email","estado","is_staff","is_active")
    list_filter = ("estado","is_staff","is_active")
    search_fields = ("username","email","first_name","last_name","ci")

@admin.register(RolUsuario)
class RolUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario","rol")
    search_fields = ("usuario__username","rol__nombre")

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ("usuario","ocupacion","horario_entrada","horario_salida")

@admin.register(Residente)
class ResidenteAdmin(admin.ModelAdmin):
    list_display = ("usuario",)

@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ("usuario","code","used","created_at","expires_at")
    list_filter = ("used",)
    search_fields = ("usuario__username","code")
