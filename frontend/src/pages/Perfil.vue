<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />
    
    <div class="flex-1 p-4 pb-28 md:p-8 md:pb-8 overflow-y-auto">
      <div class="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-top-4 duration-500">
        
        <!-- Header del Perfil -->
        <div class="bg-white p-8 rounded-[3rem] shadow-sm border border-gray-100 relative overflow-hidden">
          <div class="absolute right-0 top-0 w-64 h-64 bg-intimar-primary/5 rounded-full -mr-20 -mt-20 blur-3xl"></div>
          
          <div class="relative z-10 flex flex-col md:flex-row items-center gap-8">
            <!-- Avatar -->
            <div class="relative group">
              <div class="w-32 h-32 bg-gradient-to-br from-intimar-primary to-intimar-dark rounded-[2.5rem] flex items-center justify-center text-white text-4xl font-black shadow-2xl shadow-intimar-primary/30 border-4 border-white overflow-hidden">
                <img v-if="userDoc.user_image" :src="userDoc.user_image" alt="Avatar" class="w-full h-full object-cover" />
                <span v-else>{{ userInitials }}</span>
              </div>
              <div class="absolute -bottom-2 -right-2 w-10 h-10 bg-intimar-gold rounded-2xl flex items-center justify-center text-white shadow-lg border-4 border-white cursor-pointer hover:scale-110 transition-transform">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>
              </div>
            </div>

            <div class="text-center md:text-left flex-1">
              <div class="inline-flex items-center gap-2 bg-intimar-gold/10 text-intimar-gold px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest mb-3 border border-intimar-gold/20">
                <span class="w-1.5 h-1.5 rounded-full bg-intimar-gold animate-pulse"></span>
                Usuario Activo
              </div>
              <h1 class="text-4xl font-black text-gray-900 tracking-tight italic">{{ userDoc.full_name || 'Cargando...' }}</h1>
              <p class="text-gray-400 font-bold text-sm mt-1 uppercase tracking-widest">{{ userDoc.name }}</p>
              
              <div class="flex flex-wrap justify-center md:justify-start gap-4 mt-6">
                <div class="bg-gray-50 px-4 py-2 rounded-xl border border-gray-100 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-intimar-primary"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>
                  <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest">Rol: Administrador</span>
                </div>
                <div class="bg-gray-50 px-4 py-2 rounded-xl border border-gray-100 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-intimar-primary"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                  <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest">Desde: {{ formatDate(userDoc.creation) }}</span>
                </div>
              </div>
            </div>

            <button @click="handleLogout" class="bg-red-50 hover:bg-red-100 text-red-600 px-6 py-4 rounded-3xl text-xs font-black uppercase tracking-[0.2em] transition-all flex items-center gap-3 group border border-red-100 shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="group-hover:translate-x-1 transition-transform"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
              Cerrar Sesión
            </button>
          </div>
        </div>

        <!-- Detalles y Ajustes -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          <!-- Información Personal -->
          <div class="md:col-span-2 space-y-6">
            <div class="bg-white p-8 rounded-[3rem] shadow-sm border border-gray-100 space-y-6">
              <div class="flex items-center gap-4 mb-2">
                <div class="w-10 h-10 bg-intimar-primary rounded-xl flex items-center justify-center text-white shadow-lg shadow-intimar-primary/20">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                </div>
                <h2 class="text-xl font-black text-gray-900 tracking-tight italic">Información de la Cuenta</h2>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Nombre Completo</label>
                  <input type="text" v-model="userDoc.full_name" disabled class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-gray-700 opacity-70 cursor-not-allowed" />
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Correo Electrónico</label>
                  <input type="email" v-model="userDoc.email" disabled class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-gray-700 opacity-70 cursor-not-allowed" />
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Usuario ID</label>
                  <input type="text" v-model="userDoc.name" disabled class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-gray-700 opacity-70 cursor-not-allowed" />
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Última Conexión</label>
                  <input type="text" :value="formatDateTime(userDoc.last_login)" disabled class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-gray-700 opacity-70 cursor-not-allowed" />
                </div>
              </div>

              <div class="pt-6 border-t border-gray-50 flex justify-end">
                <button class="px-8 py-4 bg-gray-900 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-intimar-primary transition-all shadow-xl shadow-gray-200">
                  Guardar Cambios
                </button>
              </div>
            </div>
          </div>

          <!-- Columna Lateral: Stats/Ajustes Rápidos -->
          <div class="space-y-6">
            <div class="bg-gradient-to-br from-intimar-dark to-gray-900 p-8 rounded-[3rem] shadow-2xl text-white relative overflow-hidden">
              <div class="absolute right-0 bottom-0 w-32 h-32 bg-white/5 rounded-full -mr-10 -mb-10 blur-2xl"></div>
              
              <h3 class="text-lg font-black italic tracking-tight mb-6">Seguridad</h3>
              <div class="space-y-4">
                <button class="w-full px-6 py-4 bg-white/10 hover:bg-white/20 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all text-left flex justify-between items-center group">
                  Cambiar Contraseña
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="group-hover:translate-x-1 transition-transform"><path d="m9 18 6-6-6-6"/></svg>
                </button>
                <button class="w-full px-6 py-4 bg-white/10 hover:bg-white/20 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all text-left flex justify-between items-center group">
                  Doble Factor (2FA)
                  <span class="bg-red-500/20 text-red-400 px-2 py-1 rounded text-[8px]">OFF</span>
                </button>
              </div>
            </div>

            <div class="bg-intimar-gold p-8 rounded-[3rem] shadow-xl text-intimar-dark relative group overflow-hidden">
               <div class="absolute -right-4 -top-4 w-24 h-24 bg-white/20 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-700"></div>
               <h3 class="text-lg font-black italic tracking-tight mb-2">Ayuda y Soporte</h3>
               <p class="text-[10px] font-bold uppercase tracking-wider opacity-60 mb-6">¿Necesitas asistencia?</p>
               <button class="w-full py-4 bg-intimar-dark text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:scale-[1.02] transition-all shadow-lg">
                 Contactar Soporte
               </button>
            </div>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { call } from 'frappe-ui'
import { session } from '@/data/session'
import Sidebar from '@/components/Sidebar.vue'

const userDoc = ref({})

const fetchUserDetails = async () => {
  const user = session.user || (window.frappe && window.frappe.session && window.frappe.session.user)
  if (!user || user === 'Guest') return
  
  try {
    const data = await call('intimar_erp.api.get_user_details', {
      user_id: user
    })
    userDoc.value = data
  } catch (error) {
    console.error('Error fetching user details:', error)
  }
}

watch(() => session.user, (newUser) => {
  if (newUser) fetchUserDetails()
})

const userInitials = computed(() => {
  if (!userDoc.value.full_name) return 'U'
  return userDoc.value.full_name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
})

const handleLogout = () => {
  session.logout.submit()
}

const formatDate = (dateStr) => {
  if (!dateStr) return '--'
  return new Date(dateStr).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' })
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return 'Nunca'
  return new Date(dateStr).toLocaleString('es-ES', { 
    day: '2-digit', 
    month: 'short', 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

onMounted(async () => {
  // Pequeña espera para asegurar que los cookies se procesen
  await new Promise(resolve => setTimeout(resolve, 100))
  fetchUserDetails()
})
</script>
