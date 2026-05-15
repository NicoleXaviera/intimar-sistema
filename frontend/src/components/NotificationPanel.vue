<template>
  <Teleport to="body">
    <!-- Botón Flotante Superior (Z-index bajo para no tapar modales) -->
    <button 
      v-if="!isOpen"
      @click="isOpen = true"
      class="fixed top-2 right-[72px] md:top-6 md:right-6 w-12 h-12 md:w-14 md:h-14 bg-white/20 md:bg-white text-[#1a1a1a] rounded-2xl shadow-none md:shadow-[0_10px_30px_rgba(197,160,89,0.2)] flex items-center justify-center hover:scale-110 active:scale-95 transition-all z-[1001] border-none md:border md:border-gray-100 group"
      :class="{ 'animate-shake': unreadCount > 0 }"
    >
      <div class="relative">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#c5a059" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:rotate-12 transition-transform"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        <span v-if="unreadCount > 0" class="absolute -top-2.5 -right-2.5 w-5 h-5 bg-red-500 text-white text-[9px] font-black flex items-center justify-center rounded-full border-2 border-white shadow-lg">
          {{ unreadCount }}
        </span>
      </div>
    </button>

    <!-- Overlay -->
    <div 
      v-if="isOpen" 
      @click="isOpen = false" 
      class="fixed inset-0 bg-black/40 backdrop-blur-md z-[100000] transition-opacity"
    ></div>

    <!-- Sidebar Panel -->
    <div 
      class="fixed top-0 right-0 h-full w-[400px] bg-white shadow-[-20px_0_80px_rgba(0,0,0,0.2)] z-[100001] transition-transform duration-500 ease-out flex flex-col"
      :class="isOpen ? 'translate-x-0' : 'translate-x-full'"
    >
      <!-- Header -->
      <div class="p-8 border-b border-gray-100 bg-[#1a1a1a] text-white">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h2 class="text-xs font-black uppercase tracking-[0.2em] text-[#c5a059]">Centro de Control</h2>
            <p class="text-[10px] font-bold text-gray-400 mt-1 uppercase tracking-widest">Historial de Actividad</p>
          </div>
          <div class="flex gap-2">
            <button @click="testNotification" class="p-2 hover:bg-white/10 rounded-full text-gray-500 hover:text-white transition-colors" title="Probar Conexión">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
            </button>
            <button @click="isOpen = false" class="p-2 hover:bg-white/10 rounded-full transition-colors text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
          </div>
        </div>

        <!-- BUSCADOR (NUEVO) -->
        <div class="relative">
          <div class="absolute inset-y-0 left-4 flex items-center pointer-events-none text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar reserva, cliente o evento..."
            class="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-11 pr-4 text-xs font-bold text-white placeholder:text-gray-600 focus:bg-white/10 focus:border-[#c5a059]/50 focus:ring-0 transition-all outline-none"
          >
        </div>
      </div>

      <!-- Notifications List -->
      <div class="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
        <div v-if="filteredNotifications.length === 0" class="h-full flex flex-col items-center justify-center text-center opacity-20 p-10">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="mb-4"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          <p class="text-[10px] font-black uppercase tracking-widest">No se encontraron resultados</p>
        </div>

        <transition-group name="list">
          <div 
            v-for="notif in filteredNotifications" 
            :key="notif.id"
            class="group relative bg-white p-5 rounded-[1.5rem] shadow-sm border border-gray-100 hover:border-[#c5a059]/30 transition-all duration-300"
          >
            <div class="flex gap-4 items-start">
              <div class="flex-1">
                <div class="flex justify-between items-start mb-2">
                  <span class="text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full" :class="getTypeBadge(notif.type)">
                    {{ getTypeText(notif.type) }}
                  </span>
                  <span class="text-[9px] font-bold text-gray-400">{{ formatTime(notif.timestamp) }}</span>
                </div>
                <p class="text-xs font-bold text-gray-800 leading-relaxed">{{ notif.message }}</p>
                
                <div class="mt-4 flex gap-2">
                  <button 
                    v-if="notif.reserva_id"
                    @click="goToReserva(notif.reserva_id)"
                    class="px-4 py-2 bg-[#1a1a1a] text-white text-[9px] font-black uppercase tracking-widest rounded-lg hover:bg-[#c5a059] transition-all"
                  >
                    Ver Reserva
                  </button>
                  <button 
                    v-if="notif.type === 'tiempo_excedido_mesa' && notif.mesa_id"
                    @click="liberarMesaDesdeNotif(notif)"
                    class="px-4 py-2 bg-red-600 text-white text-[9px] font-black uppercase tracking-widest rounded-lg hover:bg-red-700 transition-all flex items-center gap-2"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                    Liberar Mesa
                  </button>
                  <button 
                    @click="removeNotification(notif.id)"
                    class="px-4 py-2 bg-gray-100 text-gray-400 text-[9px] font-black uppercase tracking-widest rounded-lg hover:bg-gray-200 transition-all"
                  >
                    Cerrar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition-group>

        <!-- BOTÓN VER TODO EL HISTORIAL (NUEVO) -->
        <div class="pt-4 pb-8 border-t border-gray-200 mt-4">
          <button 
            @click="router.push('/notificaciones'); isOpen = false"
            class="w-full py-4 bg-white border-2 border-dashed border-gray-200 text-gray-500 rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] hover:border-[#c5a059] hover:text-[#c5a059] transition-all flex items-center justify-center gap-3"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
            Ver Todo el Historial
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { call } from 'frappe-ui'

const router = useRouter()
const isOpen = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const searchQuery = ref('')
let nextId = 1

// Filtrado de notificaciones por búsqueda
const filteredNotifications = computed(() => {
  if (!searchQuery.value) return notifications.value
  
  const q = searchQuery.value.toLowerCase()
  return notifications.value.filter(n => 
    (n.message || '').toLowerCase().includes(q) ||
    (n.reserva_id || '').toLowerCase().includes(q) ||
    getTypeText(n.type).toLowerCase().includes(q)
  )
})

// Limpiar contador al abrir
watch(isOpen, (newVal) => {
  if (newVal) unreadCount.value = 0
})

const getTypeText = (type) => {
  const map = {
    'nueva_reserva': 'Nueva Reserva',
    'cliente_llego': 'Cliente Llegó',
    'mesa_liberada': 'Mesa Liberada',
    'aforo_lleno': 'Aforo Lleno',
    'aforo_limite': 'Aforo Límite',
    'tiempo_excedido_mesa': 'Tiempo Excedido',
    'mesa_disponible_espera': 'Mesa Disponible'
  }
  return map[type] || type
}

const getTypeBadge = (type) => {
  if (['aforo_lleno', 'aforo_limite', 'tiempo_excedido_mesa'].includes(type)) return 'bg-red-100 text-red-600'
  if (type === 'cliente_llego') return 'bg-blue-100 text-blue-600'
  if (type === 'mesa_liberada') return 'bg-green-100 text-green-600'
  return 'bg-[#c5a059]/10 text-[#c5a059]'
}

const formatTime = (ts) => {
  if (!ts) return ''
  const d = new Date(ts)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const addNotification = (data) => {
  const exists = notifications.value.some(n => n.message === data.message && Math.abs(new Date(n.timestamp) - new Date(data.timestamp)) < 5000)
  if (exists) return

  const id = nextId++
  notifications.value.unshift({
    id,
    ...data,
    timestamp: data.timestamp || new Date().toISOString()
  })
  
  if (!isOpen.value) unreadCount.value++
  if (notifications.value.length > 50) notifications.value.pop()
  
  const audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3')
  audio.volume = 0.5
  
  const playPromise = audio.play()
  if (playPromise !== undefined) {
    playPromise.catch(() => {
      console.log("Audio play prevented")
    })
  }

  setTimeout(() => {
    audio.pause()
    audio.currentTime = 0
  }, 250)
}

const removeNotification = (id) => {
  notifications.value = notifications.value.filter(n => n.id !== id)
}

const testNotification = async () => {
  try {
    await call('intimar_erp.intimar.doctype.reserva_intimar.reserva_intimar.test_realtime_connection')
  } catch (e) {
    addNotification({
      type: 'aforo_lleno',
      message: 'Error de conexión. Intentando vía radar...',
      timestamp: new Date().toISOString()
    })
  }
}

const goToReserva = (name) => {
  const targetPath = `/reservas/${name}`
  if (router.currentRoute.value.path === targetPath) {
    // Si ya estamos ahí, forzamos recarga
    window.location.reload()
  } else {
    router.push(targetPath)
  }
  isOpen.value = false
}

const fetchRecentActivity = async () => {
  try {
    const events = await call('intimar_erp.api.get_recent_activity')
    if (events && Array.isArray(events)) {
      events.forEach(addNotification)
    }
  } catch (e) {
    console.log("Radar esperando señal...")
  }

  // CONSULTAR ALERTAS DE TIEMPO (NUEVO)
  try {
    const alerts = await call('intimar_erp.api.get_occupancy_alerts')
    if (alerts && Array.isArray(alerts)) {
      alerts.forEach(alert => {
        addNotification({
          type: 'tiempo_excedido_mesa',
          message: `[MESA ${alert.mesa_numero}] El cliente ${alert.cliente} lleva ${alert.duracion_minutos} min. ¿Deseas liberar la mesa?`,
          reserva_id: alert.reserva_id,
          mesa_id: alert.mesa_id,
          timestamp: new Date().toISOString()
        })
      })
    }
  } catch (e) {
    console.error("Error al consultar alertas de tiempo:", e)
  }
}

const liberarMesaDesdeNotif = async (notif) => {
  if (!confirm(`¿Confirmas liberar la Mesa ${notif.message.match(/\[MESA (.*?)\]/)?.[1] || ''}?`)) return
  
  try {
    await call('intimar_erp.api.liberar_mesa', { mesa_id: notif.mesa_id })
    removeNotification(notif.id)
    // Emitir evento para que otras pantallas se enteren (si usan recursos auto-refrescables)
    window.dispatchEvent(new CustomEvent('mesa-liberada', { detail: { mesa_id: notif.mesa_id } }))
  } catch (e) {
    console.error("Error al liberar desde notificación:", e)
  }
}

onMounted(() => {
  // 1. CARGAR LIBRERIA SOCKET.IO
  const script = document.createElement('script')
  script.src = 'https://cdn.socket.io/4.7.2/socket.io.min.js'
  script.onload = () => {
    const connectSocket = () => {
      if (window.io) {
        const socket = window.io(window.location.origin, {
          path: '/socket.io',
          withCredentials: true,
          transports: ['websocket', 'polling']
        })
        
        socket.on('connect', () => {
          socket.emit('subscribe_site', window.location.hostname)
        })

        socket.on('intimar_notification', addNotification)
        socket.on('mesa_disponible_espera', (data) => {
          addNotification({ type: 'mesa_disponible_espera', message: data.message, reserva_id: data.reserva_espera })
        })
        socket.on('tiempo_excedido_mesa', (data) => {
          addNotification({ type: 'tiempo_excedido_mesa', message: data.message, reserva_id: data.reserva_id })
        })
      }
    }
    connectSocket()
  }
  document.head.appendChild(script)

  // 2. RADAR DE RESPALDO (Polling) - Cada 10 segundos
  fetchRecentActivity() // Carga inicial
  const pollInterval = setInterval(fetchRecentActivity, 10000)

  onUnmounted(() => {
    clearInterval(pollInterval)
  })
})
</script>

<style scoped>
.list-enter-active, .list-leave-active { transition: all 0.5s ease; }
.list-enter-from { opacity: 0; transform: translateX(30px); }
.list-leave-to { opacity: 0; transform: scale(0.9); }

@keyframes shake {
  0%, 100% { transform: rotate(0); }
  25% { transform: rotate(10deg); }
  75% { transform: rotate(-10deg); }
}
.animate-shake {
  animation: shake 0.3s ease-in-out infinite;
}
</style>
