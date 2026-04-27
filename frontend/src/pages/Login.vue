<template>
  <div class="min-h-screen bg-white flex flex-col md:flex-row">
    <!-- Lado Izquierdo: Branding Visual -->
    <div class="md:w-1/2 bg-intimar-primary flex flex-col items-center justify-center p-12 text-white relative overflow-hidden">
      <!-- Círculo decorativo tipo Sol -->
      <div class="absolute -top-20 -left-20 w-96 h-96 bg-intimar-gold/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-20 -right-20 w-64 h-64 bg-intimar-orange/20 rounded-full blur-2xl"></div>
      
      <div class="relative z-10 text-center">
        <h1 class="text-7xl font-black italic tracking-tighter mb-2">Intimar</h1>
        <p class="text-xl font-light tracking-[0.3em] uppercase opacity-80">Bay · Paracas</p>
        <div class="w-24 h-1 bg-intimar-gold mx-auto mt-6 rounded-full"></div>
      </div>
    </div>

    <!-- Lado Derecho: Formulario -->
    <div class="md:w-1/2 flex items-center justify-center p-8 bg-gray-50">
      <div class="w-full max-w-md">
        <div class="mb-10">
          <h2 class="text-3xl font-bold text-gray-900">Bienvenido</h2>
          <p class="text-gray-500">Ingresa tus credenciales para gestionar el sistema</p>
        </div>

        <form @submit.prevent="login" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Usuario</label>
            <input 
              v-model="email"
              type="text" 
              class="w-full px-5 py-4 rounded-2xl border border-gray-200 focus:ring-4 focus:ring-intimar-primary/10 focus:border-intimar-primary outline-none transition-all"
              placeholder="admin@intimar.com"
              required
            >
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Contraseña</label>
            <input 
              v-model="password"
              type="password" 
              class="w-full px-5 py-4 rounded-2xl border border-gray-200 focus:ring-4 focus:ring-intimar-primary/10 focus:border-intimar-primary outline-none transition-all"
              placeholder="••••••••"
              required
            >
          </div>

          <div v-if="error" class="p-4 bg-intimar-bordeaux/10 border border-intimar-bordeaux/20 rounded-2xl text-intimar-bordeaux text-sm font-medium">
            {{ error }}
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="w-full bg-intimar-primary hover:bg-[#007a77] text-white font-bold py-4 rounded-2xl shadow-xl shadow-intimar-primary/20 transition-all transform active:scale-95 disabled:opacity-50"
          >
            {{ loading ? 'Iniciando...' : 'Entrar al Sistema' }}
          </button>
        </form>

        <div class="mt-12 flex justify-center gap-4">
            <div class="w-3 h-3 rounded-full bg-intimar-bordeaux"></div>
            <div class="w-3 h-3 rounded-full bg-intimar-orange"></div>
            <div class="w-3 h-3 rounded-full bg-intimar-gold"></div>
            <div class="w-3 h-3 rounded-full bg-intimar-primary"></div>
            <div class="w-3 h-3 rounded-full bg-intimar-green"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { call } from 'frappe-ui'

const email = ref('')
const password = ref('')
const error = ref(null)
const loading = ref(false)

async function login() {
  loading.value = true
  error.value = null
  
  try {
    const response = await call('login', {
      usr: email.value,
      pwd: password.value
    })
    
    if (response.message === 'Logged In') {
      window.location.href = '/frontend/mapa'
    } else {
      error.value = 'Las credenciales no coinciden con nuestros registros.'
    }
  } catch (e) {
    error.value = 'No se pudo conectar con el servidor.'
  } finally {
    loading.value = false
  }
}
</script>
