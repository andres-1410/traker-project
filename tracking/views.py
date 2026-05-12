import json
import requests  # <-- OBLIGATORIO para la Geolocalización
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from catalogos.models import Catalogo
from tracking.models import Dispositivo, Visita

def obtener_ip_cliente(request):
    """Extrae la IP real, superando proxies como Cloudflare"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip if ip else None

def pantalla_puente(request, slug):
    """Renderiza el HTML que captura la huella"""
    catalogo = get_object_or_404(Catalogo, slug_url=slug, activo=True)
    return render(request, 'tracking/puente.html', {'catalogo': catalogo, 'vendedor': catalogo.vendedor})

@csrf_exempt
def registrar_visita_ajax(request):
    """Recibe los datos del JS y extrae el resto desde los headers HTTP de Django"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            slug_catalogo = data.get('slug')
            huella_hash = data.get('fingerprint')
            metadata_js = data.get('metadata', {}) # Datos que vienen del Frontend (Resolución, OS, etc.)

            catalogo = get_object_or_404(Catalogo, slug_url=slug_catalogo)
            ip_real = obtener_ip_cliente(request)
            
            # --- CAPTURA AVANZADA DE HEADERS (BACKEND) ---
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            referer = request.META.get('HTTP_REFERER', 'Directo / App Nativa')
            idioma_http = request.META.get('HTTP_ACCEPT_LANGUAGE', 'Desconocido')
            
            # Inyectamos estos datos del servidor directo al JSON que guardaremos
            metadata_js['origen_trafico_referer'] = referer
            metadata_js['idioma_http'] = idioma_http

            # Recibimos el SO y Modelo extraídos por nuestro JS
            sistema_operativo = metadata_js.get('os', 'Desconocido')
            marca_modelo = metadata_js.get('device', 'Desconocido')
            es_iphone = 'iPhone' in marca_modelo or 'iPad' in marca_modelo

            # --- GEOLOCALIZACIÓN E ISP ---
            ubicacion_detectada = "Local/Desconocida"
            isp_detectado = "Local/Desconocido"
            
            # En producción, esto traducirá la IP. En localhost (127.0.0.1) se saltará.
            if ip_real and ip_real != '127.0.0.1':
                try:
                    res_geo = requests.get(f'http://ip-api.com/json/{ip_real}', timeout=1.5)
                    if res_geo.status_code == 200:
                        data_geo = res_geo.json()
                        if data_geo.get('status') == 'success':
                            ubicacion_detectada = f"{data_geo.get('city')}, {data_geo.get('regionName')}"
                            isp_detectado = data_geo.get('isp')
                except Exception as e:
                    print(f"[GEO ERROR] Error contactando API de IPs: {e}")

            # 1. Guardamos/Actualizamos el Dispositivo
            dispositivo, creado = Dispositivo.objects.get_or_create(
                fingerprint_hash=huella_hash,
                defaults={
                    'es_iphone': es_iphone,
                    'sistema_operativo': sistema_operativo,
                    'marca_modelo_aprox': marca_modelo
                }
            )

            # Actualizamos datos si antes era "Desconocido" y ahora sí sabemos qué teléfono es
            if not creado and dispositivo.marca_modelo_aprox == 'Desconocido':
                dispositivo.sistema_operativo = sistema_operativo
                dispositivo.marca_modelo_aprox = marca_modelo
                dispositivo.es_iphone = es_iphone
                dispositivo.save()

            # 2. Guardamos la Visita con toda la carga útil
            Visita.objects.create(
                catalogo=catalogo,
                dispositivo=dispositivo,
                ip_publica=ip_real,
                proveedor_internet_isp=isp_detectado,
                ubicacion_aprox=ubicacion_detectada,
                user_agent_raw=user_agent,
                metadata_extra=metadata_js # Aquí va el mix de datos JS + Backend
            )

            return JsonResponse({'status': 'success', 'url_destino': catalogo.url_drive_destino})

        except Exception as e:
            print(f"\n[ERROR CRÍTICO EN TRACKING]: {e}\n")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'Metodo no permitido'}, status=405)