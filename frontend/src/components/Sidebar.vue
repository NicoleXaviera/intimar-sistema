<template>
  <!-- Sidebar para Desktop -->
  <div class="w-20 bg-intimar-primary flex flex-col items-center py-8 gap-10 hidden md:flex min-h-screen sticky top-0 shrink-0 shadow-2xl z-[100]">
    <!-- Logo -->
    <router-link to="/mapa" class="w-12 h-12 flex items-center justify-center hover:scale-110 transition-transform cursor-pointer">
      <img :src="'/files/intimar-logo.png'" alt="Logo" class="w-full h-auto object-contain brightness-0 invert" />
    </router-link>

    <!-- Navegación Desktop -->
    <nav class="flex-1 flex flex-col gap-6 w-full px-2">
    <!-- Insights (Dashboard) -->
      <router-link 
        v-if="session.isAdmin"
        to="/insights" 
        class="w-full aspect-square flex flex-col items-center justify-center rounded-2xl transition-all group relative"
        :class="[isRouteActive('/insights') ? 'bg-white/15 text-white shadow-lg' : 'text-white/40 hover:bg-white/5 hover:text-white/70']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        <span class="text-[8px] font-black uppercase tracking-[0.2em] mt-2 opacity-0 group-hover:opacity-100 transition-opacity">Inicio</span>
        <div v-if="isRouteActive('/insights')" class="absolute left-[-8px] w-1 h-8 bg-intimar-gold rounded-full"></div>
      </router-link> 
      
      <!-- Mapa de Mesas -->
      <router-link 
        to="/mapa" 
        class="w-full aspect-square flex flex-col items-center justify-center rounded-2xl transition-all group relative"
        :class="[isRouteActive('/mapa') ? 'bg-white/15 text-white shadow-lg' : 'text-white/40 hover:bg-white/5 hover:text-white/70']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
        <span class="text-[8px] font-black uppercase tracking-[0.2em] mt-2 opacity-0 group-hover:opacity-100 transition-opacity">Asignadas</span>
        <div v-if="isRouteActive('/mapa')" class="absolute left-[-8px] w-1 h-8 bg-intimar-gold rounded-full"></div>
      </router-link>

      <!-- Calendario -->
      <router-link 
        v-if="session.isAdmin"
        to="/calendario" 
        class="w-full aspect-square flex flex-col items-center justify-center rounded-2xl transition-all group relative"
        :class="[isRouteActive('/calendario') ? 'bg-white/15 text-white shadow-lg' : 'text-white/40 hover:bg-white/5 hover:text-white/70']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
        <span class="text-[8px] font-black uppercase tracking-[0.2em] mt-2 opacity-0 group-hover:opacity-100 transition-opacity">Calendario</span>
        <div v-if="isRouteActive('/calendario')" class="absolute left-[-8px] w-1 h-8 bg-intimar-gold rounded-full"></div>
      </router-link>


      <!-- Reservas -->
      <router-link 
        v-if="session.isAdmin || session.hasRole(['Anfitriona', 'Vigilante'])"
        to="/reservas" 
        class="w-full aspect-square flex flex-col items-center justify-center rounded-2xl transition-all group relative"
        :class="[isRouteActive('/reservas') || isRouteActive('/reservas/nueva') ? 'bg-white/15 text-white shadow-lg' : 'text-white/40 hover:bg-white/5 hover:text-white/70']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M8 7h6"/><path d="M8 11h8"/></svg>
        <span class="text-[8px] font-black uppercase tracking-[0.2em] mt-2 opacity-0 group-hover:opacity-100 transition-opacity">Reservas</span>
        <div v-if="isRouteActive('/reservas') || isRouteActive('/reservas/nueva')" class="absolute left-[-8px] w-1 h-8 bg-intimar-gold rounded-full"></div>
      </router-link>

      <!-- Clientes -->
      <router-link 
        v-if="session.isAdmin"
        to="/clientes" 
        class="w-full aspect-square flex flex-col items-center justify-center rounded-2xl transition-all group relative"
        :class="[isRouteActive('/clientes') ? 'bg-white/15 text-white shadow-lg' : 'text-white/40 hover:bg-white/5 hover:text-white/70']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <span class="text-[8px] font-black uppercase tracking-[0.2em] mt-2 opacity-0 group-hover:opacity-100 transition-opacity">Clientes</span>
        <div v-if="isRouteActive('/clientes')" class="absolute left-[-8px] w-1 h-8 bg-intimar-gold rounded-full"></div>
      </router-link>

      <!-- Gestión de Mesas -->
      <router-link 
        v-if="session.isAdmin || session.hasRole('Anfitriona')"
        to="/gestion-mesas" 
        class="w-full aspect-square flex flex-col items-center justify-center rounded-2xl transition-all group relative"
        :class="[isRouteActive('/gestion-mesas') ? 'bg-white/15 text-white shadow-lg' : 'text-white/40 hover:bg-white/5 hover:text-white/70']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
        <span class="text-[8px] font-black uppercase tracking-[0.2em] mt-2 opacity-0 group-hover:opacity-100 transition-opacity">Mesas</span>
        <div v-if="isRouteActive('/gestion-mesas')" class="absolute left-[-8px] w-1 h-8 bg-intimar-gold rounded-full"></div>
      </router-link>
      <!-- Usuarios (Admin) -->
      <router-link 
        v-if="session.isAdmin"
        to="/usuarios" 
        class="w-full aspect-square flex flex-col items-center justify-center rounded-2xl transition-all group relative"
        :class="[isRouteActive('/usuarios') ? 'bg-white/15 text-white shadow-lg' : 'text-white/40 hover:bg-white/5 hover:text-white/70']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <span class="text-[8px] font-black uppercase tracking-[0.2em] mt-2 opacity-0 group-hover:opacity-100 transition-opacity">Usuarios</span>
        <div v-if="isRouteActive('/usuarios')" class="absolute left-[-8px] w-1 h-8 bg-intimar-gold rounded-full"></div>
      </router-link>
      
    <!-- Configuración -->
      <router-link 
        v-if="session.isAdmin"
        to="/configuracion" 
        class="w-full aspect-square flex flex-col items-center justify-center rounded-2xl transition-all group relative"
        :class="[isRouteActive('/configuracion') ? 'bg-white/15 text-white shadow-lg' : 'text-white/40 hover:bg-white/5 hover:text-white/70']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.1a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
        <span class="text-[8px] font-black uppercase tracking-[0.2em] mt-2 opacity-0 group-hover:opacity-100 transition-opacity">Ajustes</span>
        <div v-if="isRouteActive('/configuracion')" class="absolute left-[-8px] w-1 h-8 bg-intimar-gold rounded-full"></div>
      </router-link>
    </nav>
    


    <!-- Perfil de Usuario -->
    <div class="mt-auto mb-4 w-full px-2 relative">
      <button 
        @click="showProfileMenu = !showProfileMenu"
        class="w-full aspect-square flex items-center justify-center rounded-2xl transition-all group relative overflow-hidden bg-white/10 hover:bg-white/20 border border-white/10"
        :class="[isRouteActive('/perfil') ? 'ring-2 ring-intimar-gold' : '']"
      >
        <div class="w-full h-full flex items-center justify-center text-white font-black text-xs">
          <img v-if="userImage" :src="userImage" class="w-full h-full object-cover" />
          <span v-else>{{ userInitials }}</span>
        </div>
      </button>

      <!-- Menú Desplegable -->
      <div v-if="showProfileMenu" class="absolute left-full ml-4 bottom-0 w-48 bg-white rounded-3xl shadow-2xl border border-gray-100 overflow-hidden animate-in slide-in-from-left-2 duration-300 z-[200]">
        <div class="p-4 border-b border-gray-50 bg-gray-50/50">
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Sesión activa</p>
          <p class="text-xs font-black text-intimar-dark truncate italic">{{ userFullName }}</p>
        </div>
        <div class="p-2">
          <router-link to="/perfil" @click="showProfileMenu = false" class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 rounded-2xl transition-colors text-xs font-bold text-gray-600 group">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-intimar-primary"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            Ver Perfil
          </router-link>
          <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 hover:bg-red-50 rounded-2xl transition-colors text-xs font-bold text-red-600 group">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Cerrar Sesión
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Barra de Navegación Inferior para Móvil -->
  <div class="md:hidden fixed bottom-5 left-4 right-4 h-16 bg-intimar-primary rounded-full shadow-[0_15px_40px_rgba(0,147,143,0.3)] z-[1000] flex items-center justify-around px-2">
    <!-- Mapa -->
    <router-link to="/mapa" 
      class="flex flex-col items-center justify-center transition-all duration-300 w-12 h-12 rounded-2xl" 
      :class="[isRouteActive('/mapa') ? 'bg-white text-intimar-primary shadow-lg scale-110' : 'text-white/40']">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>
      </svg>
    </router-link>

    <!-- Calendario -->
    <router-link v-if="session.isAdmin" to="/calendario" 
      class="flex flex-col items-center justify-center transition-all duration-300 w-12 h-12 rounded-2xl" 
      :class="[isRouteActive('/calendario') ? 'bg-white text-intimar-primary shadow-lg scale-110' : 'text-white/40']">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/>
      </svg>
    </router-link>

    <!-- Insights -->
    <router-link v-if="session.isAdmin" to="/insights" 
      class="flex flex-col items-center justify-center transition-all duration-300 w-12 h-12 rounded-2xl" 
      :class="[isRouteActive('/insights') ? 'bg-white text-intimar-primary shadow-lg scale-110' : 'text-white/40']">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="20" x2="18" y2="10"/>
        <line x1="12" y1="20" x2="12" y2="4"/>
        <line x1="6" y1="20" x2="6" y2="14"/>
      </svg>
    </router-link>

    <!-- Reservas -->
    <router-link v-if="session.isAdmin || session.hasRole(['Anfitriona', 'Vigilante'])" to="/reservas" 
      class="flex flex-col items-center justify-center transition-all duration-300 w-12 h-12 rounded-2xl" 
      :class="[isRouteActive('/reservas') || isRouteActive('/reservas/nueva') ? 'bg-white text-intimar-primary shadow-lg scale-110' : 'text-white/40']">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M8 7h6"/><path d="M8 11h8"/>
      </svg>
    </router-link>

    <!-- Clientes -->
    <router-link v-if="session.isAdmin" to="/clientes" 
      class="flex flex-col items-center justify-center transition-all duration-300 w-12 h-12 rounded-2xl" 
      :class="[isRouteActive('/clientes') ? 'bg-white text-intimar-primary shadow-lg scale-110' : 'text-white/40']">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
      </svg>
    </router-link>

    <!-- Mesas -->
    <router-link v-if="session.isAdmin || session.hasRole('Anfitriona')" to="/gestion-mesas" 
      class="flex flex-col items-center justify-center transition-all duration-300 w-12 h-12 rounded-2xl" 
      :class="[isRouteActive('/gestion-mesas') ? 'bg-white text-intimar-primary shadow-lg scale-110' : 'text-white/40']">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>
      </svg>
    </router-link>

    <!-- Ajustes -->
    <router-link v-if="session.isAdmin" to="/configuracion" 
      class="flex flex-col items-center justify-center transition-all duration-300 w-12 h-12 rounded-2xl" 
      :class="[isRouteActive('/configuracion') ? 'bg-white text-intimar-primary shadow-lg scale-110' : 'text-white/40']">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.1a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>
      </svg>
    </router-link>
  </div>

</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed, ref, onMounted, watch } from 'vue'
import { session } from '@/data/session'
import { call } from 'frappe-ui'

const route = useRoute()
const userImage = ref(null)
const userFullName = ref('')
const showProfileMenu = ref(false)

const isRouteActive = (path) => {
  return route.path === path
}

const handleLogout = () => {
  session.logout.submit()
}

const userInitials = computed(() => {
  if (!userFullName.value) return 'U'
  return userFullName.value.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
})

const fetchUserSidebar = async () => {
  const user = session.user || (window.frappe && window.frappe.session && window.frappe.session.user)
  if (!user || user === 'Guest') return
  
  try {
    const data = await call('frappe.client.get_value', {
      doctype: 'User',
      filters: { name: user },
      fieldname: ['full_name', 'user_image']
    })
    if (data) {
      userFullName.value = data.full_name
      userImage.value = data.user_image
    }
  } catch (e) {
    console.error(e)
  }
}

watch(() => session.user, (newUser) => {
  if (newUser) fetchUserSidebar()
})

onMounted(async () => {
  await new Promise(resolve => setTimeout(resolve, 100))
  fetchUserSidebar()
})
</script>
