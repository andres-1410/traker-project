from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
  # --- Autenticación y Registro ---
    path('api/validar-codigo/', views.validar_codigo_api, name='validar_codigo'),
    path('api/registro/', views.registrar_vendedor_api, name='registro_vendedor'),
    path('api/login/', views.login_api, name='login_api'),
    
    # --- Gestión del Cliente ---
    path('api/perfil/', views.perfil_api, name='perfil_api'),
    path('api/pagos/reportar/', views.reportar_pago_api, name='reportar_pago_api'),
    path('api/metricas/', views.metricas_dashboard_api, name='metricas_dashboard_api'),
]