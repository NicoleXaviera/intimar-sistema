<template>
  <div class="h-screen w-screen bg-gray-50">
    <router-view />
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui'
import { watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// Recurso para verificar quién está logueado
const user = createResource({
  url: 'frappe.auth.get_logged_user',
  auto: true,
  onSuccess: (data) => {
    if (!data && route.name !== 'Login') {
      router.push({ name: 'Login' })
    }
  },
  onError: () => {
    if (route.name !== 'Login') {
      router.push({ name: 'Login' })
    }
  }
})

// Vigilamos la ruta para redirigir si no hay sesión
watch(() => route.name, (newName) => {
  if (newName !== 'Login' && !user.data) {
    user.fetch()
  }
})
</script>
