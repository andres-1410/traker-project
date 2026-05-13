import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Vendedor, CodigoPromocional

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