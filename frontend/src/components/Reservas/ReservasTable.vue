<template>
  <div class="bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden relative z-10">
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50/50 border-b border-gray-100">
            <th class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] w-16 text-center">ID</th>
            <th class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em]">Cliente</th>
            <th class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em]">Detalles de Reserva</th>
            <th class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em]">Asignación</th>
            <th class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em]">Estado</th>
            <th class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] text-right">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="loading" class="animate-pulse">
            <td colspan="6" class="p-8 text-center text-gray-400 font-bold">Cargando reservaciones...</td>
          </tr>
          <tr v-else-if="reservas.length === 0">
            <td colspan="6" class="p-12 text-center text-gray-400 font-bold">No hay reservaciones que coincidan con los filtros.</td>
          </tr>
          
          <tr 
            v-for="reserva in reservas" 
            :key="reserva.name"
            class="hover:bg-gray-50/50 transition-colors group"
          >
            <!-- ID -->
            <td class="px-4 py-2">
              <div class="bg-gray-100 text-gray-500 font-black text-[10px] py-1 px-2 rounded-md text-center tracking-wider">
                {{ reserva.name.split('-').pop() }}
              </div>
            </td>

            <!-- Cliente -->
            <td class="px-4 py-2">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-intimar-primary/10 rounded-lg flex items-center justify-center text-intimar-primary font-black text-xs uppercase">
                  {{ getInitials(reserva.nombre) }}
                </div>
                <div>
                  <h4 class="font-black text-gray-900 text-[13px] mb-0.5">{{ reserva.nombre }}</h4>
                  <p class="text-[10px] font-bold text-gray-400 flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    {{ reserva.celular || 'Sin teléfono' }}
                  </p>
                </div>
              </div>
            </td>

            <!-- Detalles -->
            <td class="px-4 py-2">
              <div class="flex flex-col gap-1">
                <div class="flex items-center gap-2">
                  <span class="bg-gray-100 text-gray-700 font-bold text-[11px] py-0.5 px-2 rounded flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                    {{ formatDate(reserva.fecha_reserva) }}
                  </span>
                  <span class="bg-intimar-gold/10 text-intimar-gold font-black text-[11px] py-0.5 px-2 rounded flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    {{ formatTime(reserva.hora_reserva) }}
                  </span>
                </div>
                <div class="text-[10px] font-bold text-gray-500 flex items-center gap-2 ml-0.5">
                  <span class="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    {{ reserva.cant_adultos || 0 }} Adul.
                  </span>
                  <span class="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
                    {{ reserva.cant_ninos || 0 }} Niñ.
                  </span>
                </div>
              </div>
            </td>

            <!-- Asignación -->
            <td class="px-4 py-2">
              <div v-if="reserva.mozo" class="flex items-center gap-2">
                <div class="w-6 h-6 bg-purple-50 rounded flex items-center justify-center text-purple-600">
                  <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>
                </div>
                <span class="font-bold text-[13px] text-gray-700">{{ reserva.mozo }}</span>
              </div>
              <div v-else class="text-[11px] font-bold text-gray-400 italic">
                Sin asignar
              </div>
              
              <div v-if="reserva.total_pagado" class="mt-1 inline-flex items-center gap-1 bg-green-50 text-green-700 text-[10px] font-black py-0.5 px-2 rounded-lg border border-green-200/50 shadow-sm uppercase tracking-tight">
                ANTIC. S/ {{ reserva.total_pagado }}
              </div>
              <div v-else-if="reserva.anticipo_required" class="mt-1 inline-flex items-center gap-1 bg-orange-50 text-orange-600 text-[9px] font-black uppercase tracking-widest py-0.5 px-1.5 rounded">
                Pendiente
              </div>
            </td>

            <!-- Estado -->
            <td class="px-4 py-2">
              <span :class="getStatusClass(reserva.estado_reserva)" class="inline-flex items-center gap-1.5 py-1 px-2 rounded-lg text-[10px] font-black uppercase tracking-wider">
                <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotClass(reserva.estado_reserva)"></span>
                {{ reserva.estado_reserva }}
              </span>
            </td>

            <!-- Acciones -->
            <td class="px-4 py-2 text-right">
              <div class="flex justify-end gap-2">
                <!-- Asignar Mesa -->
                <button 
                  v-if="!reserva.mesas?.length" 
                  @click="$emit('asignar', reserva)"
                  class="p-2 bg-white text-gray-400 hover:text-intimar-green border border-gray-100 hover:border-intimar-green/30 rounded-lg shadow-sm hover:shadow-md transition-all"
                  title="Asignar Mesa Rápidamente"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M16 4l-4-4-4 4"/><path d="M12 0v16"/></svg>
                </button>
                
                <!-- Editar -->
                <router-link 
                  :to="`/reservas/${reserva.name}`"
                  class="p-2 bg-white text-gray-400 hover:text-intimar-gold border border-gray-100 hover:border-intimar-gold/30 rounded-lg shadow-sm hover:shadow-md transition-all"
                  title="Gestionar Reserva"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                </router-link>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  reservas: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['refresh', 'asignar'])

// Utilidades
const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  // Extraemos manualmente el año, mes y día para evitar que JS reste horas 
  // por la zona horaria al usar new Date("YYYY-MM-DD") (lo que causaba que salga el día anterior)
  const [year, month, day] = dateString.substring(0, 10).split('-')
  const date = new Date(year, month - 1, day)
  return new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: 'short' }).format(date)
}

const formatTime = (timeString) => {
  if (!timeString) return ''
  // Asume formato "HH:MM:SS"
  return timeString.substring(0, 5)
}

// Estilos de Badges según el estado
const getStatusClass = (estado) => {
  const map = {
    'Solicitud de reserva': 'bg-red-50 text-red-600',
    'Pendiente a confirmar': 'bg-orange-50 text-orange-600',
    'Confirmada': 'bg-green-50 text-green-600',
    'En proceso': 'bg-blue-50 text-blue-600',
    'Finalizada': 'bg-gray-100 text-gray-700',
    'Cancelada': 'bg-red-100 text-red-800',
    'Lista de espera': 'bg-purple-50 text-purple-600',
  }
  return map[estado] || 'bg-gray-50 text-gray-500'
}

const getStatusDotClass = (estado) => {
  const map = {
    'Solicitud de reserva': 'bg-red-500',
    'Pendiente a confirmar': 'bg-orange-500',
    'Confirmada': 'bg-green-500',
    'En proceso': 'bg-blue-500',
    'Finalizada': 'bg-gray-500',
    'Cancelada': 'bg-red-500',
    'Lista de espera': 'bg-purple-500',
  }
  return map[estado] || 'bg-gray-400'
}
</script>
