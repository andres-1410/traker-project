import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/registro',
      name: 'registro',
      component: () => import('../views/RegistroView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      // Esta meta etiqueta le dice al router que esta ruta es privada
      meta: { requiereAutenticacion: true }
    },
    {
      path: '/',
      redirect: '/login'
    }
  ]
})

// Guarda de Seguridad: Revisa antes de cada cambio de página
router.beforeEach((to, from, next) => {
  const vendedorId = localStorage.getItem('vendedor_id')
  
  if (to.meta.requiereAutenticacion && !vendedorId) {
    // Si la ruta es privada y no hay llave, lo pateamos al login
    next('/login')
  } else if ((to.name === 'login' || to.name === 'registro') && vendedorId) {
    // Si ya está logueado y trata de ir al login, lo mandamos al dashboard
    next('/dashboard')
  } else {
    next()
  }
})

export default router