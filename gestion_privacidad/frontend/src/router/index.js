import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import Error403 from '@/views/Error403.vue'
import auth from "@/logic/auth";

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login
  },
  {
    path: '/Dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/error-403',
    name: 'Error403',
    component: Error403
  },
  {
    path: '/:catchAll(.*)',
    redirect: { name: 'Error403' }
  },

  // Añade una nueva ruta en tu router
{
  path: '/sso-login',
  name: 'SSOLogin',
  component: () => import('@/views/SSOLogin.vue')
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!auth.isAuthenticated()) {
      next('/error-403'); // Redirige a la página de error 403 si el usuario no está autenticado
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router
