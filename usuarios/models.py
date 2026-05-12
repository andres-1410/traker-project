from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# --- NUEVO: Motor de Códigos de Acceso y Promociones ---
class CodigoPromocional(models.Model):
    codigo = models.CharField(max_length=20, unique=True, db_index=True)
    
    # 1. PERMISOS DE ENTRADA
    permite_registro = models.BooleanField(
        default=True, 
        help_text="¿Se puede usar este código en la pantalla principal para crear una cuenta nueva?"
    )
    
    # 2. RECOMPENSAS (Se pueden sumar)
    dias_gratis_otorgados = models.PositiveIntegerField(
        default=0, 
        help_text="Días de prueba gratuita que suma al registrarse."
    )
    porcentaje_descuento = models.PositiveIntegerField(
        default=0, 
        help_text="Descuento (Ej: 20 para 20%) aplicable en el registro o al reportar un pago."
    )
    
    # 3. CONTROL DE LÍMITES
    usos_maximos = models.PositiveIntegerField(default=1, help_text="Pon 0 para usos ilimitados")
    usos_actuales = models.PositiveIntegerField(default=0)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    notas = models.TextField(blank=True, help_text="Ej: Código para campaña de Instagram Junio")

    def es_valido(self):
        """Verifica si el código aún se puede usar en tiempo real"""
        if not self.activo:
            return False
        if self.usos_maximos > 0 and self.usos_actuales >= self.usos_maximos:
            return False
        from django.utils import timezone
        if self.fecha_vencimiento and self.fecha_vencimiento < timezone.now():
            return False
        return True

    def __str__(self):
        return f"{self.codigo} (Desc: {self.porcentaje_descuento}% | Días: {self.dias_gratis_otorgados})"

# --- ACTUALIZADO: El Cliente Final (Dueño del catálogo) ---
class Vendedor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_vendedor')
    id_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre_comercial = models.CharField(max_length=150)
    
    # Datos de Contacto Directo
    telefono_whatsapp = models.CharField(max_length=20, help_text="Ej: +584141234567")
    
    # Motor de Publicidad (Growth Hacking)
    publicidad_activada = models.BooleanField(
        default=False, 
        help_text="Si está activo, muestra 'Powered by' en la pantalla puente a cambio de descuento."
    )
    
    logo = models.ImageField(upload_to='logos_vendedores/', blank=True, null=True)
    fecha_vencimiento_suscripcion = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_comercial

    class Meta:
        verbose_name_plural = "Vendedores"

class Pago(models.Model):
    ESTADOS_PAGO = [
        ('PENDIENTE', 'Pendiente de Revisión'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='pagos')
    # Relacionamos el pago con un código en caso de que lo hayan usado al facturar
    codigo_usado = models.ForeignKey(CodigoPromocional, on_delete=models.SET_NULL, blank=True, null=True)
    
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    numero_referencia = models.CharField(max_length=100)
    comprobante = models.ImageField(upload_to='comprobantes_pagos/')
    estado = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='PENDIENTE')
    notas_admin = models.TextField(blank=True, help_text="Notas privadas para el administrador")

    def __str__(self):
        return f"Pago {self.numero_referencia} - {self.vendedor.nombre_comercial}"