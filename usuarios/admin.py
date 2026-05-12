from django.contrib import admin
from .models import Vendedor, Pago

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercial', 'usuario', 'activo', 'fecha_vencimiento_suscripcion')
    search_fields = ('nombre_comercial', 'usuario__username')
    list_filter = ('activo',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('numero_referencia', 'vendedor', 'monto', 'estado', 'fecha_pago')
    list_filter = ('estado', 'fecha_pago')
    search_fields = ('numero_referencia', 'vendedor__nombre_comercial')