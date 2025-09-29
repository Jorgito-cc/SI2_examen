from django.contrib import admin
from .models import UnidadHabitacional, ResidenteUnidad

@admin.register(UnidadHabitacional)
class UnidadHabitacionalAdmin(admin.ModelAdmin):
    list_display = ("bloque", "numero", "estado", "superficie")
    list_filter = ("estado", "bloque")
    search_fields = ("bloque", "numero")
    ordering = ("bloque", "numero")

@admin.register(ResidenteUnidad)
class ResidenteUnidadAdmin(admin.ModelAdmin):
    list_display = ("residente", "unidad", "es_propietario")
    list_filter = ("es_propietario",)
    search_fields = ("residente__usuario__username", "unidad__bloque", "unidad__numero")
