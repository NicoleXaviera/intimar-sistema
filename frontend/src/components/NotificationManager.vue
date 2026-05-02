<template>
  <Teleport to="body">
    <div class="fixed top-24 right-6 z-[10000] flex flex-col gap-4 w-80 pointer-events-none">
      <transition-group name="notification-slide">
        <div 
          v-for="notif in notifications" 
          :key="notif.id"
          class="bg-white/95 backdrop-blur-xl border-l-4 shadow-2xl rounded-2xl p-4 pointer-events-auto flex gap-4 items-start animate-scaleIn"
          :class="notif.type === 'waitlist' ? 'border-intimar-gold' : 'border-red-500'"
        >
          <div 
            class="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
            :class="notif.type === 'waitlist' ? 'bg-intimar-gold/10 text-intimar-gold' : 'bg-red-50/80 text-red-500'"
          >
            <svg v-if="notif.type === 'waitlist'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <div class="flex-1">
            <h4 class="text-xs font-black text-gray-900 uppercase tracking-widest mb-1">{{ notif.title }}</h4>
            <p class="text-[11px] font-bold text-gray-500 leading-relaxed">{{ notif.message }}</p>
            <div class="mt-3 flex gap-2">
              <button 
                @click="goToReserva(notif.reserva_id, notif.id)"
                class="px-3 py-1.5 bg-intimar-primary text-white text-[9px] font-black uppercase tracking-widest rounded-lg hover:bg-intimar-primary/90 transition-colors"
              >
                Ver Reserva
              </button>
              <button 
                @click="removeNotification(notif.id)"
                class="px-3 py-1.5 bg-gray-100 text-gray-500 text-[9px] font-black uppercase tracking-widest rounded-lg hover:bg-gray-200 transition-colors"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </transition-group>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const notifications = ref([])
let nextId = 1

const addNotification = (data, type = 'waitlist') => {
  const id = nextId++
  
  const isWaitlist = type === 'waitlist'
  
  notifications.value.push({
    id,
    title: isWaitlist ? '¡Mesa Disponible!' : '⏰ Tiempo Excedido',
    message: data.message,
    reserva_id: isWaitlist ? data.reserva_espera : data.reserva_id,
    type: type
  })
  
  // Auto remove after 20 seconds for stay duration alerts
  setTimeout(() => removeNotification(id), isWaitlist ? 15000 : 30000)
  
  // Play sound
  try {
    const soundUrl = isWaitlist 
      ? 'https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3'
      : 'https://assets.mixkit.co/active_storage/sfx/951/951-preview.mp3'
    const audio = new Audio(soundUrl)
    audio.volume = 0.4
    audio.play()
  } catch (e) {}
}

const removeNotification = (id) => {
  notifications.value = notifications.value.filter(n => n.id !== id)
}

const goToReserva = (name, notifId) => {
  router.push(`/reservas/${name}`)
  removeNotification(notifId)
}

onMounted(() => {
  // Escuchar eventos de Frappe Realtime
  if (window.frappe && window.frappe.realtime) {
    window.frappe.realtime.on('mesa_disponible_espera', (data) => {
      addNotification(data, 'waitlist')
    })
    
    window.frappe.realtime.on('tiempo_excedido_mesa', (data) => {
      addNotification(data, 'duration')
    })
  }
})

onUnmounted(() => {
  if (window.frappe && window.frappe.realtime) {
    window.frappe.realtime.off('mesa_disponible_espera')
  }
})
</script>

<style scoped>
.notification-slide-enter-active,
.notification-slide-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.notification-slide-enter-from {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}
.notification-slide-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.animate-scaleIn {
  animation: scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
</style>
