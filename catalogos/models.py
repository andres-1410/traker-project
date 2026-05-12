from django.db import models
from usuarios.models import Vendedor

class Catalogo(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='catalogos')
    nombre_interno = models.CharField(max_length=150, help_text="Ej: Lista Toyota Mayo")
    slug_url = models.SlugField(max_length=150, unique=True, help_text="Ej: precios-toyota (Se usa para la URL)")
    url_drive_destino = models.URLField(max_length=500, help_text="El enlace real de Google Drive")
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_interno} ({self.vendedor.nombre_comercial})"