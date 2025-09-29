
from django.contrib import admin
from .models import FaceProfile, FaceEvent

@admin.register(FaceProfile)
class FaceProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "label", "vector_dim", "created_at")
    search_fields = ("usuario__username", "usuario__email", "label")

@admin.register(FaceEvent)
class FaceEventAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "confianza", "aceptado", "motivo", "fecha_hora")
    search_fields = ("usuario__username", "motivo")
    list_filter = ("aceptado",)
