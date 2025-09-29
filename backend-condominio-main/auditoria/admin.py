from django.contrib import admin
from .models import Bitacora

@admin.register(Bitacora)
class BitacoraAdmin(admin.ModelAdmin):
    list_display = ("creado_en", "usuario", "accion", "ip", "path")
    list_filter = ("usuario", "creado_en")
    search_fields = ("accion", "detalle", "path", "usuario__username", "usuario__email")
    readonly_fields = ("creado_en",)
