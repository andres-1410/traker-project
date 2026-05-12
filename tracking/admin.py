from django.contrib import admin
from .models import Dispositivo, Visita

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('fingerprint_hash', 'marca_modelo_aprox', 'sistema_operativo', 'es_iphone', 'fecha_primera_visita')
    search_fields = ('fingerprint_hash', 'marca_modelo_aprox')
    list_filter = ('es_iphone', 'sistema_operativo')

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('catalogo', 'dispositivo', 'ip_publica', 'timestamp_entrada')
    list_filter = ('catalogo', 'timestamp_entrada')
    search_fields = ('ip_publica', 'dispositivo__fingerprint_hash')
    readonly_fields = ('timestamp_entrada',) # Para no editar por error la fecha de visita