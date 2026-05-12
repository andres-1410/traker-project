from django.db import models
from catalogos.models import Catalogo

class Dispositivo(models.Model):
    fingerprint_hash = models.CharField(max_length=255, unique=True, db_index=True)
    marca_modelo_aprox = models.CharField(max_length=150, blank=True, null=True)
    sistema_operativo = models.CharField(max_length=100, blank=True, null=True)
    es_iphone = models.BooleanField(default=False)
    fecha_primera_visita = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispositivo: {self.fingerprint_hash[:8]}..."

class Visita(models.Model):
    catalogo = models.ForeignKey(Catalogo, on_delete=models.CASCADE, related_name='visitas')
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='historial_visitas')
    timestamp_entrada = models.DateTimeField(auto_now_add=True, db_index=True)
    ip_publica = models.GenericIPAddressField(blank=True, null=True)
    proveedor_internet_isp = models.CharField(max_length=100, blank=True, null=True)
    ubicacion_aprox = models.CharField(max_length=150, blank=True, null=True)
    user_agent_raw = models.TextField(blank=True, null=True, help_text="Cadena completa del navegador")
    
    # Campo JSONB para guardar metadatos variables (batería, conexión, etc.)
    metadata_extra = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Visita a {self.catalogo.slug_url} el {self.timestamp_entrada.strftime('%Y-%m-%d %H:%M')}"