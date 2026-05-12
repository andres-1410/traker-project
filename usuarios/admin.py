from django.contrib import admin
from .models import Vendedor, Pago, CodigoPromocional

@admin.register(CodigoPromocional)
class CodigoPromocionalAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'permite_registro', 'dias_gratis_otorgados', 'porcentaje_descuento', 'usos_actuales', 'usos_maximos', 'activo')
    list_filter = ('activo', 'permite_registro', 'fecha_vencimiento')
    search_fields = ('codigo', 'notas')
    readonly_fields = ('usos_actuales',) # El sistema debe sumar esto automáticamente, mejor no editarlo a mano
    
    # Agrupamos los campos para que sea más cómodo crear campañas
    fieldsets = (
        ('Información del Código', {
            'fields': ('codigo', 'notas', 'activo')
        }),
        ('Reglas y Recompensas', {
            'fields': ('permite_registro', 'dias_gratis_otorgados', 'porcentaje_descuento')
        }),
        ('Límites', {
            'fields': ('usos_maximos', 'usos_actuales', 'fecha_vencimiento')
        }),
    )

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    # Añadimos el teléfono y el estatus de publicidad a la vista
    list_display = ('nombre_comercial', 'usuario', 'telefono_whatsapp', 'publicidad_activada', 'activo', 'fecha_vencimiento_suscripcion')
    search_fields = ('nombre_comercial', 'usuario__username', 'telefono_whatsapp')
    list_filter = ('activo', 'publicidad_activada')
    
    # list_editable te permite apagar/prender estos interruptores directamente desde la tabla general
    list_editable = ('publicidad_activada', 'activo')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    # Añadimos la columna del código promocional usado (si aplica)
    list_display = ('numero_referencia', 'vendedor', 'monto', 'estado', 'codigo_usado', 'fecha_pago')
    list_filter = ('estado', 'fecha_pago')
    search_fields = ('numero_referencia', 'vendedor__nombre_comercial', 'codigo_usado__codigo')