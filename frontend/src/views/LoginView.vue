<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg border border-gray-100">
      
      <div class="text-center mb-8">
        <h2 class="text-3xl font-extrabold text-gray-900">Iniciar Sesión</h2>
        <p class="mt-2 text-sm text-gray-600">Accede a tus catálogos y estadísticas</p>
      </div>

      <!-- Banner de Error Global -->
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

      <form class="space-y-6" @submit.prevent="iniciarSesion">
        <div class="space-y-4">
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

        <div class="pt-2">
          <button type="submit" :disabled="cargando"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-800 hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-800 disabled:opacity-70 transition-colors">
            
            <svg v-if="cargando" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            
            {{ cargando ? 'Verificando...' : 'Entrar' }}
          </button>
        </div>
      </form>

      <div class="text-center mt-4">
        <p class="text-sm text-gray-600">
          ¿No tienes cuenta? 
          <router-link to="/registro" class="font-medium text-blue-600 hover:text-blue-500">Regístrate aquí</router-link>
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL
const router = useRouter()

const cargando = ref(false)
const errorGlobal = ref('')
const formulario = ref({
  email: '',
  password: ''
})

const iniciarSesion = async () => {
  errorGlobal.value = ''
  cargando.value = true
  
  try {
    const respuesta = await axios.post(`${API_URL}/usuarios/api/login/`, formulario.value)
    
    // Guardamos la llave de acceso y el nombre en el navegador
    localStorage.setItem('vendedor_id', respuesta.data.vendedor_id)
    localStorage.setItem('nombre_comercial', respuesta.data.nombre_comercial)
    
    // Lo empujamos al Dashboard
    router.push('/dashboard')
    
  } catch (error) {
    errorGlobal.value = error.response?.data?.message || 'Error de conexión con el servidor.'
  } finally {
    cargando.value = false
  }
}
</script>