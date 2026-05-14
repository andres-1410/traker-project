import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from .models import Vendedor, CodigoPromocional, Pago
from django.db.models import Count
from catalogos.models import Catalogo
from tracking.models import Visita

@csrf_exempt
def validar_codigo_api(request):
    """Recibe un código y devuelve si es válido y qué recompensas tiene"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codigo_str = data.get('codigo', '').strip()
            
            try:
                promocion = CodigoPromocional.objects.get(codigo=codigo_str)
                if promocion.es_valido():
                    return JsonResponse({
                        'status': 'success',
                        'valido': True,
                        'permite_registro': promocion.permite_registro,
                        'dias_gratis': promocion.dias_gratis_otorgados,
                        'descuento': promocion.porcentaje_descuento
                    })
                else:
                    return JsonResponse({'status': 'error', 'message': 'El código ha expirado o alcanzó su límite de usos.'}, status=400)
            except CodigoPromocional.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Código no encontrado.'}, status=404)
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


@csrf_exempt
def registrar_vendedor_api(request):
    """Procesa el formulario de registro desde Vue.js"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            nombre_comercial = data.get('nombre_comercial')
            telefono_whatsapp = data.get('telefono_whatsapp')
            codigo_str = data.get('codigo', '').strip()
            huella_viral = data.get('fingerprint_id') # Viene de la URL de publicidad

            # 1. Validaciones básicas
            if not all([email, password, nombre_comercial, telefono_whatsapp]):
                return JsonResponse({'status': 'error', 'message': 'Faltan datos obligatorios.'}, status=400)

            if User.objects.filter(username=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Este correo ya está registrado.'}, status=400)

            # 2. Lógica del Código Promocional
            dias_gratis = 0
            promocion = None
            if codigo_str:
                try:
                    promocion = CodigoPromocional.objects.get(codigo=codigo_str)
                    if not promocion.es_valido() or not promocion.permite_registro:
                        return JsonResponse({'status': 'error', 'message': 'Código inválido para registro.'}, status=400)
                    dias_gratis = promocion.dias_gratis_otorgados
                except CodigoPromocional.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Código no encontrado.'}, status=404)

            # 3. Creación del Usuario (Django Auth)
            user = User.objects.create_user(
                username=email, # Usamos el email como username para que inicien sesión con él
                email=email,
                password=password
            )

            # 4. Cálculo de Vencimiento
            fecha_vencimiento = None
            if dias_gratis > 0:
                fecha_vencimiento = timezone.now() + timedelta(days=dias_gratis)

            # 5. Creación del Vendedor (Tu Cliente)
            vendedor = Vendedor.objects.create(
                usuario=user,
                nombre_comercial=nombre_comercial,
                telefono_whatsapp=telefono_whatsapp,
                fecha_vencimiento_suscripcion=fecha_vencimiento
            )
            
            # ¡EL TRUCO MÁGICO!
            if huella_viral:
                from tracking.models import Dispositivo
                try:
                    dispositivo_anonimo = Dispositivo.objects.get(fingerprint_hash=huella_viral)
                    dispositivo_anonimo.vendedor_asociado = vendedor
                    dispositivo_anonimo.save()
                except Dispositivo.DoesNotExist:
                    pass

            # 6. Descontar el uso del código
            if promocion:
                promocion.usos_actuales += 1
                promocion.save()

            return JsonResponse({
                'status': 'success', 
                'message': 'Cuenta creada exitosamente.',
                'vendedor_id': str(vendedor.id_unico),
                'vencimiento': fecha_vencimiento.strftime('%Y-%m-%d') if fecha_vencimiento else None
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)



@csrf_exempt
def login_api(request):
    """Procesa el inicio de sesión y devuelve la 'llave' de acceso"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Django verifica si el usuario y la contraseña coinciden
            user = authenticate(username=email, password=password)
            
            if user is not None:
                vendedor = user.perfil_vendedor
                
                # Verificamos si la cuenta está activa
                if not vendedor.activo:
                    return JsonResponse({'status': 'error', 'message': 'Esta cuenta ha sido suspendida.'}, status=403)

                return JsonResponse({
                    'status': 'success',
                    'vendedor_id': str(vendedor.id_unico),
                    'nombre_comercial': vendedor.nombre_comercial,
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Correo o contraseña incorrectos.'}, status=401)
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


@csrf_exempt
def perfil_api(request):
    """Obtiene o actualiza el perfil del cliente, incluyendo la subida de su logo"""
    # 1. Identificamos al cliente por su llave de acceso
    vendedor_id = request.headers.get('X-Vendedor-ID')
    if not vendedor_id:
        return JsonResponse({'status': 'error', 'message': 'No autorizado. Inicie sesión.'}, status=401)
        
    try:
        vendedor = Vendedor.objects.get(id_unico=vendedor_id)
    except Vendedor.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Cuenta no encontrada.'}, status=404)

    # 2. Si es GET, solo devolvemos sus datos para rellenar el formulario en Vue
    if request.method == 'GET':
        return JsonResponse({
            'status': 'success',
            'nombre_comercial': vendedor.nombre_comercial,
            'telefono_whatsapp': vendedor.telefono_whatsapp,
            'publicidad_activada': vendedor.publicidad_activada,
            'logo_url': vendedor.logo.url if vendedor.logo else None,
            'fecha_vencimiento': vendedor.fecha_vencimiento_suscripcion,
        })
        
    # 3. Si es POST, actualizamos los datos y guardamos el logo
    elif request.method == 'POST':
        try:
            # Usamos request.POST porque vendrá como FormData desde Vue
            vendedor.nombre_comercial = request.POST.get('nombre_comercial', vendedor.nombre_comercial)
            vendedor.telefono_whatsapp = request.POST.get('telefono_whatsapp', vendedor.telefono_whatsapp)
            
            # Los booleanos en FormData llegan como texto ('true' o 'false')
            pub_activada = request.POST.get('publicidad_activada')
            if pub_activada is not None:
                vendedor.publicidad_activada = (pub_activada.lower() == 'true')
                
            # Si enviaron un archivo llamado 'logo', lo guardamos
            if 'logo' in request.FILES:
                vendedor.logo = request.FILES['logo']
                
            vendedor.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Perfil actualizado exitosamente.',
                'logo_url': vendedor.logo.url if vendedor.logo else None
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


@csrf_exempt
def reportar_pago_api(request):
    """Recibe un reporte de pago con imagen y aplica códigos de descuento si los hay"""
    if request.method == 'POST':
        vendedor_id = request.headers.get('X-Vendedor-ID')
        if not vendedor_id:
            return JsonResponse({'status': 'error', 'message': 'No autorizado.'}, status=401)
            
        try:
            vendedor = Vendedor.objects.get(id_unico=vendedor_id)
        except Vendedor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cuenta no encontrada.'}, status=404)
            
        try:
            monto = request.POST.get('monto')
            referencia = request.POST.get('numero_referencia')
            comprobante = request.FILES.get('comprobante') # ¡El archivo de imagen!
            codigo_str = request.POST.get('codigo', '').strip()
            
            if not all([monto, referencia, comprobante]):
                return JsonResponse({'status': 'error', 'message': 'Faltan datos (Monto, Referencia o Foto del Comprobante).'}, status=400)
                
            # Validamos si introdujo un código de descuento para su mensualidad
            promocion = None
            if codigo_str:
                try:
                    promocion = CodigoPromocional.objects.get(codigo=codigo_str)
                    if not promocion.es_valido():
                        return JsonResponse({'status': 'error', 'message': 'El código ingresado no es válido o ya expiró.'}, status=400)
                except CodigoPromocional.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Código promocional no encontrado.'}, status=404)
            
            # Creamos el registro del pago para que tú lo revises en el Panel Admin
            Pago.objects.create(
                vendedor=vendedor,
                codigo_usado=promocion,
                monto=monto,
                numero_referencia=referencia,
                comprobante=comprobante,
                estado='PENDIENTE' # Nace pendiente hasta que tú lo apruebes
            )
            
            # Descontamos un uso a la promoción
            if promocion:
                promocion.usos_actuales += 1
                promocion.save()
                
            return JsonResponse({'status': 'success', 'message': 'Pago enviado con éxito. Esperando aprobación del administrador.'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def metricas_dashboard_api(request):
    """Calcula y devuelve las estadísticas de tráfico para el panel del cliente"""
    if request.method == 'GET':
        vendedor_id = request.headers.get('X-Vendedor-ID')
        if not vendedor_id:
            return JsonResponse({'status': 'error', 'message': 'No autorizado.'}, status=401)
            
        try:
            vendedor = Vendedor.objects.get(id_unico=vendedor_id)
        except Vendedor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cuenta no encontrada.'}, status=404)

        try:
            # 1. Buscamos los catálogos que te pertenecen
            catalogos = Catalogo.objects.filter(vendedor=vendedor)
            
            # 2. Buscamos todas las visitas que han recibido esos catálogos
            visitas = Visita.objects.filter(catalogo__in=catalogos)
            
            # 3. Métricas Generales
            total_clics = visitas.count()
            # Contamos cuántas huellas distintas hay
            dispositivos_unicos = visitas.values('dispositivo').distinct().count()
            
            # 4. Agrupaciones Estadísticas (Los "Top 3")
            top_sistemas = list(
                visitas.values('dispositivo__sistema_operativo')
                .annotate(total=Count('id'))
                .order_by('-total')[:3]
            )
            
            top_ciudades = list(
                visitas.values('ubicacion_aprox')
                .annotate(total=Count('id'))
                .order_by('-total')[:3]
            )

            # 5. Rendimiento individual por catálogo (Para la tabla "Mis Catálogos")
            lista_catalogos = []
            for cat in catalogos:
                lista_catalogos.append({
                    'nombre': cat.nombre_interno,
                    'enlace_tracking': f"/{cat.slug_url}", # Luego en el front le ponemos el dominio completo
                    'total_visitas': cat.visitas.count(),
                    'activo': cat.activo
                })

            return JsonResponse({
                'status': 'success',
                'metricas_generales': {
                    'total_clics': total_clics,
                    'dispositivos_unicos': dispositivos_unicos,
                    'top_sistemas': top_sistemas,
                    'top_ciudades': top_ciudades
                },
                'catalogos': lista_catalogos
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)