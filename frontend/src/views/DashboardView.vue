<template>
  <div class="flex h-screen bg-gray-50 font-sans">
    
    <!-- BARRA LATERAL -->
    <aside class="w-64 bg-slate-900 text-white flex flex-col shadow-xl">
      <div class="h-16 flex items-center justify-center border-b border-slate-800">
        <h1 class="text-xl font-bold tracking-wider">Tu<span class="text-blue-500">Tracker</span></h1>
      </div>
      
      <nav class="flex-1 px-4 py-6 space-y-2">
        <a href="#" class="flex items-center px-4 py-3 bg-blue-600 text-white rounded-lg transition-colors">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
          Panel General
        </a>
        <a href="#" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          Mis Catálogos
        </a>
      </nav>

      <div class="p-4 border-t border-slate-800">
        <button @click="cerrarSesion" class="flex items-center w-full px-4 py-2 text-sm text-slate-400 hover:text-white transition-colors">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          Cerrar Sesión
        </button>
      </div>
    </aside>

    <!-- ÁREA PRINCIPAL -->
    <main class="flex-1 flex flex-col overflow-hidden">
      
      <header class="h-16 bg-white shadow-sm flex items-center justify-between px-8 border-b border-gray-200">
        <h2 class="text-xl font-semibold text-gray-800">Métricas en Tiempo Real</h2>
        
        <!-- EL BOTÓN ESTRATÉGICO DE CONTACTO -->
        <a href="https://wa.me/58400000000?text=Hola,%20necesito%20crear%20un%20nuevo%20catálogo%20para%20mi%20negocio." target="_blank" 
           class="flex items-center px-4 py-2 bg-green-500 hover:bg-green-600 text-white text-sm font-medium rounded-md transition-colors shadow-sm">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.86s.274.072.376-.043c.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564.289.13.332.202c.045.072.045.419-.101.824zm-3.392-10.416c-4.284 0-7.768 3.484-7.768 7.768 0 1.365.352 2.697 1.021 3.882l-1.087 3.974 4.067-1.066c1.139.61 2.428.932 3.763.932 4.281 0 7.766-3.484 7.768-7.766 0-4.284-3.484-7.768-7.768-7.768z"/></svg>
          Solicitar un Catálogo
        </a>
      </header>

      <div class="flex-1 overflow-y-auto p-8">
        
        <div class="mb-8">
          <h3 class="text-2xl font-bold text-gray-900">Hola, {{ nombreVendedor }} 👋</h3>
          <p class="text-gray-600 mt-1">Este es el rendimiento general de tus enlaces activos.</p>
        </div>

        <!-- Tarjetas de Resumen (Métricas de la Base de Datos) -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center">
            <div class="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500">Clics Registrados</p>
              <p class="text-2xl font-bold text-gray-900">0</p>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center">
            <div class="p-3 rounded-full bg-green-100 text-green-600 mr-4">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500">Dispositivos Únicos</p>
              <p class="text-2xl font-bold text-gray-900">0</p>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center">
            <div class="p-3 rounded-full bg-purple-100 text-purple-600 mr-4">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path></svg>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500">Tasa de Efectividad</p>
              <p class="text-2xl font-bold text-gray-900">0%</p>
            </div>
          </div>
        </div>

        <!-- SECCIÓN DIVIDIDA: Calculadora a la Izquierda, Catálogos a la Derecha -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          <!-- CALCULADORA DE ALCANCE (1 Columna) -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 lg:col-span-1">
            <h4 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
              <svg class="w-5 h-5 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
              Calculadora de Alcance
            </h4>
            <p class="text-xs text-gray-500 mb-6">Proyecta el impacto de tu próxima campaña de WhatsApp.</p>
            
            <div class="space-y-4">
              <div>
                <label class="block text-xs font-medium text-gray-700">Inversión (USD)</label>
                <input type="number" v-model="calcInversion" class="mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500" placeholder="Ej: 50" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700">Días de Campaña</label>
                <input type="number" v-model="calcDias" class="mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500" placeholder="Ej: 7" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700">Costo por Clic Estimado (USD)</label>
                <input type="number" v-model="calcCPC" step="0.01" class="mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500" placeholder="Ej: 0.15" />
              </div>
            </div>

            <div class="mt-6 pt-4 border-t border-gray-100">
              <p class="text-xs text-gray-500 text-center uppercase tracking-wider font-semibold">Clics Proyectados</p>
              <p class="text-3xl font-black text-center text-blue-600 mt-1">{{ proyeccionClics }}</p>
              <p class="text-xs text-center text-gray-400 mt-1">Visitantes diarios: {{ visitantesDiarios }}</p>
            </div>
          </div>

          <!-- LISTA DE CATÁLOGOS (Solo Lectura) (2 Columnas) -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden lg:col-span-2 flex flex-col">
            <div class="p-6 border-b border-gray-100 flex justify-between items-center">
              <h4 class="text-lg font-bold text-gray-800">Mis Catálogos Activos</h4>
            </div>
            
            <!-- Tabla de Datos -->
            <div class="overflow-x-auto flex-1">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre del Catálogo</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Visitas</th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acción</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <!-- Esto luego lo llenaremos desde la API de Django -->
                  <tr>
                    <td class="px-6 py-8 text-center text-sm text-gray-500" colspan="3">
                      Aún no tienes catálogos configurados. <br>
                      <a href="#" class="text-blue-600 hover:underline mt-1 inline-block font-medium">Habla con soporte para iniciar.</a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

      </div>
    </main>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const nombreVendedor = ref('')

// Variables Reactivas para la Calculadora
const calcInversion = ref(50)
const calcDias = ref(7)
const calcCPC = ref(0.15)

// Funciones Computadas (El cálculo se actualiza solo si mueven los números)
const proyeccionClics = computed(() => {
  if (calcInversion.value > 0 && calcCPC.value > 0) {
    return Math.floor(calcInversion.value / calcCPC.value).toLocaleString()
  }
  return 0
})

const visitantesDiarios = computed(() => {
  if (calcInversion.value > 0 && calcCPC.value > 0 && calcDias.value > 0) {
    const clicsTotales = calcInversion.value / calcCPC.value
    return Math.floor(clicsTotales / calcDias.value).toLocaleString()
  }
  return 0
})

onMounted(() => {
  nombreVendedor.value = localStorage.getItem('nombre_comercial') || 'Usuario'
})

const cerrarSesion = () => {
  localStorage.removeItem('vendedor_id')
  localStorage.removeItem('nombre_comercial')
  router.push('/login')
}
</script>