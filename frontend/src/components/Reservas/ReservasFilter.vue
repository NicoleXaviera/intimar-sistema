<template>
  <div class="bg-white p-6 rounded-[2rem] shadow-sm border border-gray-100 relative z-20">
    <!-- Header del Filtro -->
    <div class="flex items-center justify-between mb-5">
      <h3 class="text-xs font-black text-gray-900 uppercase tracking-widest flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="text-intimar-gold"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
        Filtros Rápidos
      </h3>
      <button @click="clearFilters" class="text-[10px] font-black uppercase tracking-widest text-red-500 hover:text-red-700 bg-red-50 hover:bg-red-100 px-4 py-2 rounded-xl transition-all flex items-center gap-2">
        Limpiar Filtros
      </button>
    </div>

    <!-- Grid de Filtros -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-6 gap-4">
      
      <!-- Buscar por ID -->
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9h16"/><path d="M4 15h16"/><path d="M10 3 8 21"/><path d="M16 3l-2 18"/></svg>
        </div>
        <input v-model="filters.id" type="text" placeholder="ID Reserva..." class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-transparent rounded-2xl text-xs font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all placeholder:text-gray-400">
      </div>
      
      <!-- Fecha Específica -->
      <div class="relative w-full">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
        </div>
        <input v-model="filters.fecha" type="date" class="w-full pl-12 pr-3 py-3 bg-gray-50 border border-transparent rounded-2xl text-xs font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all">
      </div>

      <!-- Hora Exacta (Desplegable) -->
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        </div>
        <select v-model="filters.hora" class="w-full pl-12 pr-4 py-3 bg-gray-50 border border-transparent rounded-2xl text-xs font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all appearance-none cursor-pointer">
          <option value="Todas">Cualquier Hora</option>
          <option value="11:00:00">11:00 AM</option>
          <option value="11:30:00">11:30 AM</option>
          <option value="12:00:00">12:00 PM</option>
          <option value="12:30:00">12:30 PM</option>
          <option value="13:00:00">1:00 PM</option>
          <option value="13:30:00">1:30 PM</option>
          <option value="14:00:00">2:00 PM</option>
          <option value="14:30:00">2:30 PM</option>
          <option value="15:00:00">3:00 PM</option>
          <option value="15:30:00">3:30 PM</option>
          <option value="16:00:00">4:00 PM</option>
          <option value="16:30:00">4:30 PM</option>
          <option value="17:00:00">5:00 PM</option>
        </select>
        <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-400"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></div>
      </div>

      <!-- Textos y Selects -->
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </div>
        <input v-model="filters.nombre" type="text" placeholder="Nombre cliente..." class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-transparent rounded-2xl text-xs font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all placeholder:text-gray-400">
      </div>

      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        </div>
        <input v-model="filters.celular" type="text" placeholder="Teléfono..." class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-transparent rounded-2xl text-xs font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all placeholder:text-gray-400">
      </div>

      <div class="relative">
        <select v-model="filters.estado" class="w-full px-4 py-3 bg-gray-50 border border-transparent rounded-2xl text-xs font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all appearance-none cursor-pointer">
          <option value="Todos">Todos los Estados</option>
          <option value="Solicitud de reserva">🔴 Solicitud</option>
          <option value="Pendiente a confirmar">🟠 Pendiente</option>
          <option value="Confirmada">🟢 Confirmada</option>
          <option value="En proceso">🔵 En proceso</option>
          <option value="Finalizada">⚫ Finalizada</option>
          <option value="Cancelada">❌ Cancelada</option>
          <option value="Lista de espera">⏳ Lista de espera</option>
        </select>
        <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-400"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, watch, defineEmits } from 'vue'
import { useRoute } from 'vue-router'

const emit = defineEmits(['filter'])
const route = useRoute()

// Obtener fecha de hoy en formato YYYY-MM-DD para el filtro inicial
const today = new Date().toISOString().split('T')[0]
const initialDate = route.query.fecha || today

const filters = reactive({
  id: '',
  nombre: '',
  celular: '',
  fecha: initialDate, // Fecha del calendario o hoy
  hora: 'Todas',
  estado: 'Todos'
})

// Emitimos los filtros al padre cada vez que cambien
watch(filters, (newFilters) => {
  emit('filter', { ...newFilters })
}, { deep: true, immediate: true })

const clearFilters = () => {
  filters.id = ''
  filters.nombre = ''
  filters.celular = ''
  filters.fecha = ''
  filters.hora = 'Todas'
  filters.estado = 'Todos'
}
</script>
