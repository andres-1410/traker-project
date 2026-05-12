from django.db import models
from django.contrib.auth.models import User
import uuid

class Vendedor(models.Model):
    # Enlazamos al modelo User de Django para aprovechar su sistema de login
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_vendedor')
    id_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre_comercial = models.CharField(max_length=150)
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
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    numero_referencia = models.CharField(max_length=100)
    comprobante = models.ImageField(upload_to='comprobantes_pagos/')
    estado = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='PENDIENTE')
    notas_admin = models.TextField(blank=True, help_text="Notas privadas para el administrador")

    def __str__(self):
        return f"Pago {self.numero_referencia} - {self.vendedor.nombre_comercial}"