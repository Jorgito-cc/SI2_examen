from django.db import models

class Notificacion(models.Model):
    usuario = models.ForeignKey(
        'authx.Usuario',
        on_delete=models.CASCADE,
        related_name="notificaciones"
    )
    titulo = models.CharField(max_length=200)
    poligono = models.CharField(max_length=200)  # o cambiar a TextField si va a ser largo
    descripcion = models.TextField()             # mejor para textos largos
    leido = models.BooleanField(default=False)   # útil: marcar notificación como leída
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} → {self.usuario}"
