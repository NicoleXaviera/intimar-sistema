import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
  },
  {
    path: '/mapa',
    name: 'MapaMesas',
    component: () => import('@/pages/MapaMesas.vue'),
  },
  {
    path: '/clientes',
    name: 'Clientes',
    component: () => import('@/pages/Clientes.vue'),
  },
  {
    path: '/clientes/:name',
    name: 'ClienteDetalle',
    component: () => import('@/pages/ClienteDetalle.vue'),
  },
  {
    path: '/gestion-mesas',
    name: 'GestionMesas',
    component: () => import('@/pages/GestionMesas.vue'),
  },
  {
    path: '/configuracion',
    name: 'Configuracion',
    component: () => import('@/pages/Configuracion.vue'),
  },
  {
    path: '/reservas',
    name: 'Reservas',
    component: () => import('@/pages/Reservas.vue'),
  },
  {
    path: '/calendario',
    name: 'Calendario',
    component: () => import('@/pages/CalendarioReservas.vue'),
  },
  {
    path: '/reservas/nueva',
    name: 'NuevaReserva',
    component: () => import('@/pages/ReservaForm.vue'),
  },
  {
    path: '/reservas/:name',
    name: 'EditarReserva',
    component: () => import('@/pages/ReservaForm.vue'),
  },
  {
    path: '/perfil',
    name: 'Perfil',
    component: () => import('@/pages/Perfil.vue'),
  },
  {
    path: '/usuarios',
    name: 'Usuarios',
    component: () => import('@/pages/Usuarios.vue'),
  },
  {
    path: '/insights',
    name: 'Insights',
    component: () => import('@/pages/Dashboard.vue'),
  },
  {
    path: '/notificaciones',
    name: 'HistorialNotificaciones',
    component: () => import('@/pages/Notifications.vue'),
  },
  {
    path: '/reservar',
    name: 'ReservaPublica',
    component: () => import('@/pages/ReservaPublica.vue'),
    meta: { isPublic: true }
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.DEV ? '/frontend' : '/intimar'),
  routes,
})

router.beforeEach((to, from, next) => {
  const user_id = document.cookie
    .split('; ')
    .find((row) => row.startsWith('user_id='))
    ?.split('=')[1]

  const isLoggedIn = user_id && user_id !== 'Guest'

  // Si ya está logueado e intenta ingresar a Login, redirigir a raíz para despacho de rol
  if (to.name === 'Login' && isLoggedIn) {
    next('/')
  }
  // Si la ruta no es pública y no es Login, y no está logueado -> Login
  else if (!to.meta.isPublic && to.name !== 'Login' && !isLoggedIn) {
    next('/login')
  } 
  // Si intenta entrar a la raíz y no está logueado -> Reserva Pública
  else if (to.path === '/' && !isLoggedIn) {
    next('/reservar')
  } 
  else {
    next()
  }
})

export default router
