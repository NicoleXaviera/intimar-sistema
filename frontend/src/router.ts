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

let router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

export default router
