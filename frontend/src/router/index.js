import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/registro',
      name: 'registro',
      component: () => import('../views/RegistroView.vue')
    },
    // Si entran a la raíz, los mandamos al registro por ahora
    {
      path: '/',
      redirect: '/registro'
    }
  ]
})

export default router