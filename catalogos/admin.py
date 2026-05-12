from django.contrib import admin
from django.utils.html import format_html
from .models import Catalogo

@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    # Agregamos 'enlace_whatsapp' a las columnas visibles
    list_display = ('nombre_interno', 'vendedor', 'enlace_whatsapp', 'activo')
    search_fields = ('nombre_interno', 'slug_url', 'vendedor__nombre_comercial')
    list_filter = ('activo',)
    prepopulated_fields = {'slug_url': ('nombre_interno',)} 

    # Función que genera el link visual
    def enlace_whatsapp(self, obj):
        # Cuando lo subas a internet, cambiarás 'http://127.0.0.1:8000' por tu dominio real
        url_completa = f"http://127.0.0.1:8000/v/{obj.slug_url}/"
        return format_html(f'<a href="{url_completa}" target="_blank">{url_completa}</a>')
    
    enlace_whatsapp.short_description = 'Link para WhatsApp'