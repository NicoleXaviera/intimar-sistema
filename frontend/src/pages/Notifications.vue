<template>
  <div class="h-full flex flex-col w-full items-center bg-gray-50/50 min-h-screen">
    <!-- Header -->
    <div class="w-full max-w-6xl mx-auto px-4 lg:px-8 py-10">
      <header class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <router-link to="/reservas" class="p-2 bg-white rounded-xl shadow-sm hover:shadow-md transition-all text-gray-400 hover:text-intimar-gold">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
            </router-link>
            <h1 class="text-4xl font-black text-gray-900 tracking-tighter italic">Historial de <span class="text-intimar-gold">Actividad</span></h1>
          </div>
          <p class="text-sm font-bold text-gray-400 uppercase tracking-widest ml-12">Registro completo de eventos y notificaciones</p>
        </div>

        <!-- Buscador Grande -->
        <div class="relative w-full md:max-w-md">
          <div class="absolute inset-y-0 left-5 flex items-center pointer-events-none text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar por cliente, mesa o ID..."
            class="w-full pl-14 pr-6 py-4 bg-white border-none rounded-[2rem] shadow-xl shadow-gray-200/50 text-sm font-bold text-gray-700 placeholder:text-gray-300 focus:ring-4 focus:ring-intimar-gold/10 transition-all outline-none"
          >
        </div>
      </header>

      <!-- Tabla de Notificaciones -->
      <div class="bg-white rounded-[3rem] shadow-2xl shadow-gray-200/50 overflow-hidden border border-gray-100">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-gray-50/50">
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Tipo / Evento</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Mensaje Detallado</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 text-right">Fecha y Hora</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 text-center">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-if="filteredLogs.length === 0" class="hover:bg-gray-50/30 transition-colors">
                <td colspan="4" class="px-8 py-20 text-center">
                  <div class="flex flex-col items-center opacity-20">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="mb-4"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                    <p class="text-sm font-black uppercase tracking-widest">No se encontraron registros</p>
                  </div>
                </td>
              </tr>
              <tr v-for="log in filteredLogs" :key="log.name" class="hover:bg-gray-50/30 transition-colors group">
                <td class="px-8 py-6">
                  <span class="px-3 py-1.5 rounded-full text-[9px] font-black uppercase tracking-widest border" :class="getTypeBadge(log.type)">
                    {{ getTypeText(log.type) }}
                  </span>
                </td>
                <td class="px-8 py-6">
                  <p class="text-sm font-bold text-gray-800 leading-relaxed">{{ log.message }}</p>
                  <p v-if="log.reserva_id" class="text-[10px] font-black text-intimar-gold uppercase mt-1 tracking-tighter">Reserva: {{ log.reserva_id }}</p>
                </td>
                <td class="px-8 py-6 text-right">
                  <p class="text-xs font-black text-gray-900">{{ formatDate(log.timestamp) }}</p>
                  <p class="text-[10px] font-bold text-gray-400 uppercase mt-0.5">{{ formatTime(log.timestamp) }}</p>
                </td>
                <td class="px-8 py-6 text-center">
                  <button 
                    v-if="log.reserva_id"
                    @click="router.push(`/reservas/${log.reserva_id}`)"
                    class="p-3 bg-gray-900 text-white rounded-2xl hover:bg-intimar-gold transition-all shadow-lg shadow-gray-200 group-hover:scale-110"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { call } from 'frappe-ui'

const router = useRouter()
const logs = ref([])
const searchQuery = ref('')

const filteredLogs = computed(() => {
  if (!searchQuery.value) return logs.value
  const q = searchQuery.value.toLowerCase()
  return logs.value.filter(l => 
    (l.message || '').toLowerCase().includes(q) ||
    (l.reserva_id || '').toLowerCase().includes(q) ||
    getTypeText(l.type).toLowerCase().includes(q)
  )
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
  if (['aforo_lleno', 'aforo_limite', 'tiempo_excedido_mesa'].includes(type)) return 'bg-red-50 text-red-600 border-red-100'
  if (type === 'cliente_llego') return 'bg-blue-50 text-blue-600 border-blue-100'
  if (type === 'mesa_liberada') return 'bg-green-50 text-green-600 border-green-100'
  return 'bg-intimar-gold/5 text-intimar-gold border-intimar-gold/10'
}

const formatDate = (ts) => {
  if (!ts) return ''
  return new Date(ts).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' })
}

const formatTime = (ts) => {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

const fetchHistory = async () => {
  try {
    const res = await call('intimar_erp.api.get_recent_activity')
    if (res && Array.isArray(res)) {
      logs.value = res.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    }
  } catch (e) {
    console.error("Error cargando historial", e)
  }
}

onMounted(() => {
  fetchHistory()
})
</script>
