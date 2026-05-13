<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg border border-gray-100">
      
      <!-- PANTALLA DE ÉXITO (Se muestra solo cuando el registro termina bien) -->
      <div v-if="registroExitoso" class="text-center py-8">
        <!-- Icono de Check Verde (SVG) -->
        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-100 mb-6">
          <svg class="h-10 w-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 class="text-3xl font-extrabold text-gray-900 mb-2">¡Cuenta Creada!</h2>
        <p class="text-gray-600 mb-6">Tu espacio de trabajo ha sido configurado con éxito. Ya puedes empezar a crear y medir tus catálogos.</p>
        
        <button @click="irAlLogin" 
          class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
          Entrar a mi Dashboard
        </button>
      </div>

      <!-- PANTALLA DEL FORMULARIO (Se oculta al tener éxito) -->
      <div v-else>
        <!-- Cabecera -->
        <div class="text-center mb-8">
          <h2 class="text-3xl font-extrabold text-gray-900">Crea tu Catálogo</h2>
          <p class="mt-2 text-sm text-gray-600">Empieza a medir tus ventas por WhatsApp</p>
        </div>

        <!-- Banner de Error Global (Reemplaza al alert de error) -->
        <div v-if="errorGlobal" class="mb-6 p-4 rounded-md bg-red-50 border border-red-200">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">{{ errorGlobal }}</h3>
            </div>
          </div>
        </div>

        <form class="space-y-6" @submit.prevent="registrarUsuario">
          <div class="space-y-4">
            
            <!-- Código Promocional -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Código de Invitación / Promo</label>
              <input type="text" v-model="formulario.codigo" @blur="validarCodigo" placeholder="Ej: VIP15DIAS"
                class="block w-full px-4 py-2 rounded-md border border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm uppercase transition-colors" />
              
              <!-- Mensaje de Validación del Código -->
              <p v-if="mensajeCodigo" :class="codigoValido ? 'text-green-600' : 'text-red-500'" class="mt-2 text-xs font-semibold flex items-center">
                <span class="mr-1" v-if="codigoValido">✓</span>
                {{ mensajeCodigo }}
              </p>
            </div>

            <!-- Datos del Negocio -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre Comercial</label>
              <input type="text" v-model="formulario.nombre_comercial" required placeholder="Repuestos El Chamo"
                class="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">WhatsApp de Ventas</label>
              <input type="tel" v-model="formulario.telefono_whatsapp" required placeholder="+584141234567"
                class="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors" />
            </div>

            <!-- Credenciales -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Correo Electrónico</label>
              <input type="email" v-model="formulario.email" required placeholder="tu@correo.com"
                class="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
              <input type="password" v-model="formulario.password" required placeholder="••••••••"
                class="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors" />
            </div>
          </div>

          <!-- Botón Submit -->
          <div class="pt-2">
            <button type="submit" :disabled="cargando"
              class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-800 hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-800 disabled:opacity-70 transition-colors">
              
              <!-- Spinner de Carga (SVG) -->
              <svg v-if="cargando" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              
              {{ cargando ? 'Procesando...' : 'Crear mi cuenta gratis' }}
            </button>
          </div>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

// Estados Reactivos UI
const cargando = ref(false)
const registroExitoso = ref(false)
const errorGlobal = ref('')
const codigoValido = ref(false)
const mensajeCodigo = ref('')

const formulario = ref({
  codigo: '',
  nombre_comercial: '',
  telefono_whatsapp: '',
  email: '',
  password: '',
  fingerprint_id: ''
})

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  if (urlParams.has('promo')) {
    formulario.value.codigo = urlParams.get('promo')
    validarCodigo()
  }
  if (urlParams.has('dispositivo_id')) {
    formulario.value.fingerprint_id = urlParams.get('dispositivo_id')
  }
})

const validarCodigo = async () => {
  if (!formulario.value.codigo) {
    mensajeCodigo.value = ''
    codigoValido.value = false
    return
  }

  try {
    const respuesta = await axios.post(`${API_URL}/usuarios/api/validar-codigo/`, {
      codigo: formulario.value.codigo.toUpperCase()
    })
    
    if (respuesta.data.valido && respuesta.data.permite_registro) {
      codigoValido.value = true
      let beneficios = 'Código válido'
      if (respuesta.data.dias_gratis > 0) beneficios += ` (${respuesta.data.dias_gratis} días gratis)`
      if (respuesta.data.descuento > 0) beneficios += ` - ${respuesta.data.descuento}% descuento`
      mensajeCodigo.value = beneficios
    } else {
      codigoValido.value = false
      mensajeCodigo.value = 'Código inválido para registro.'
    }
  } catch (error) {
    codigoValido.value = false
    mensajeCodigo.value = error.response?.data?.message || 'Código expirado o no existe'
  }
}

const registrarUsuario = async () => {
  errorGlobal.value = '' // Limpiamos errores anteriores
  cargando.value = true
  
  try {
    const respuesta = await axios.post(`${API_URL}/usuarios/api/registro/`, formulario.value)
    
    // Si llegamos aquí, fue un 200 OK. Mostramos la pantalla de éxito.
    registroExitoso.value = true
    
  } catch (error) {
    // Si falla (Ej: correo ya existe), pintamos el banner rojo
    errorGlobal.value = error.response?.data?.message || 'Ocurrió un problema de conexión con el servidor.'
  } finally {
    cargando.value = false
  }
}

const irAlLogin = () => {
  // Por ahora recarga la página, luego lo conectaremos al Router real de Login
  window.location.reload()
}
</script>