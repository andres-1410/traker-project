from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    # Esta es la URL visible que copiarás en WhatsApp (Ej: [midominio.com/v/precios-toyota/](https://midominio.com/v/precios-toyota/))
    path('v/<slug:slug>/', views.pantalla_puente, name='puente'),
    
    # Esta es la URL "oculta" a la que el JavaScript enviará los datos sin que el usuario lo note
    path('api/registrar-visita/', views.registrar_visita_ajax, name='registrar_visita'),
]