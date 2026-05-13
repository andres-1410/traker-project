from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('api/validar-codigo/', views.validar_codigo_api, name='validar_codigo'),
    path('api/registro/', views.registrar_vendedor_api, name='registro_vendedor'),
]