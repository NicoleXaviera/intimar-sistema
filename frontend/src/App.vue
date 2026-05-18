<template>
  <div class="min-h-screen w-full bg-gray-50 overflow-x-hidden flex flex-col">
    <NotificationPanel v-if="route.name && route.name !== 'Login' && !route.meta.isPublic" />
    <router-view />
  </div>
</template>

<script setup>
import { createResource, call } from 'frappe-ui'
import { watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NotificationPanel from '@/components/NotificationPanel.vue'
import { session } from '@/data/session'

const router = useRouter()
const route = useRoute()

// Recurso para verificar quién está logueado
const user = createResource({
  url: 'frappe.auth.get_logged_user',
  auto: true
})

const roles = createResource({
  url: 'intimar_erp.api.get_current_user_roles',
  onSuccess: (data) => {
    session.roles = data || []
    if (route.path === '/') {
      if (session.isAdmin) {
        router.replace('/insights')
      } else {
        router.replace('/mapa')
      }
    }
  }
})

watch(() => user.data, (newUser) => {
  if (newUser) {
    roles.fetch()
  }
})

// Vigilamos cambios de ruta a raíz para despachar según rol
watch(() => route.path, (newPath) => {
  if (newPath === '/' && session.roles.length > 0) {
    if (session.isAdmin) {
      router.replace('/insights')
    } else {
      router.replace('/mapa')
    }
  }
})

// Inactivity Timeout (1 hora)
let inactivityTimer
const INACTIVITY_LIMIT = 60 * 60 * 1000 // 60 min

const resetInactivityTimer = () => {
  clearTimeout(inactivityTimer)
  inactivityTimer = setTimeout(async () => {
    if (route.name !== 'Login') {
      try {
        await call('frappe.auth.logout')
        window.location.reload() // Redirige al login vía el watcher de usuario
      } catch (e) {
        console.error("Error al cerrar sesión por inactividad", e)
      }
    }
  }, INACTIVITY_LIMIT)
}

// Vigilamos la ruta para redirigir si no hay sesión
watch(() => route.name, (newName) => {
  if (newName !== 'Login' && !route.meta.isPublic && !user.data) {
    user.fetch()
  }
})

onMounted(() => {
  // Listeners para actividad
  window.addEventListener('mousemove', resetInactivityTimer)
  window.addEventListener('keydown', resetInactivityTimer)
  window.addEventListener('scroll', resetInactivityTimer)
  window.addEventListener('click', resetInactivityTimer)
  resetInactivityTimer()
})

onUnmounted(() => {
  window.removeEventListener('mousemove', resetInactivityTimer)
  window.removeEventListener('keydown', resetInactivityTimer)
  window.removeEventListener('scroll', resetInactivityTimer)
  window.removeEventListener('click', resetInactivityTimer)
  clearTimeout(inactivityTimer)
})
</script>
