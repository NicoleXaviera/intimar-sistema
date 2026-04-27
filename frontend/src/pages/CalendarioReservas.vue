<template>
  <div class="min-h-screen bg-gray-50 flex overflow-hidden">
    <Sidebar />
    <div class="flex-1 flex flex-col h-screen md:p-8 p-4 md:pb-8 pb-28">
      
      <!-- Contenedor Principal del Calendario -->
      <div class="bg-white flex-1 rounded-[2.5rem] shadow-sm border border-gray-100 flex flex-col overflow-hidden relative animate-in fade-in slide-in-from-top-4 duration-500">
        
        <!-- Header -->
        <div class="p-6 md:p-8 border-b border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="flex items-center gap-4">
            <div class="w-14 h-14 bg-gradient-to-br from-intimar-primary to-intimar-dark rounded-2xl flex items-center justify-center shadow-lg shadow-intimar-primary/20 shrink-0 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
            </div>
            <div>
              <h1 class="text-3xl font-black text-gray-900 tracking-tight italic capitalize">
                {{ currentView === 'day' ? currentDateFormatted : currentMonthName + ' ' + currentYear }}
              </h1>
              <p class="text-[10px] font-bold text-gray-400 uppercase tracking-[0.2em] mt-0.5">
                Vista {{ currentView === 'month' ? 'Mensual' : currentView === 'week' ? 'Semanal' : 'Diaria' }}
              </p>
            </div>
          </div>

          <div class="flex items-center gap-4">
            <!-- Selector de Vista -->
            <div class="hidden md:flex items-center bg-gray-50 p-1.5 rounded-2xl border border-gray-100">
              <button @click="currentView = 'month'" :class="currentView === 'month' ? 'bg-white shadow-sm text-intimar-primary' : 'text-gray-400 hover:text-gray-600'" class="px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all">Mes</button>
              <button @click="currentView = 'week'" :class="currentView === 'week' ? 'bg-white shadow-sm text-intimar-primary' : 'text-gray-400 hover:text-gray-600'" class="px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all">Semana</button>
              <button @click="currentView = 'day'" :class="currentView === 'day' ? 'bg-white shadow-sm text-intimar-primary' : 'text-gray-400 hover:text-gray-600'" class="px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all">Día</button>
            </div>

            <!-- Controles de Navegación -->
            <div class="flex items-center gap-2 bg-gray-50 p-1.5 rounded-2xl border border-gray-100">
              <button @click="prevPeriod" class="p-3 text-gray-400 hover:text-intimar-primary hover:bg-white rounded-xl transition-all shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
              </button>
              <button @click="goToToday" class="px-6 py-2 text-xs font-black uppercase tracking-[0.2em] text-gray-700 hover:text-intimar-primary transition-colors">
                Hoy
              </button>
              <button @click="nextPeriod" class="p-3 text-gray-400 hover:text-intimar-primary hover:bg-white rounded-xl transition-all shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Cuerpo del Calendario -->
        <div class="flex-1 flex flex-col overflow-auto bg-gray-50/50 relative">
          
          <template v-if="currentView === 'month'">
            <!-- Días de la semana -->
            <div class="grid grid-cols-7 border-b border-gray-100 bg-white sticky top-0 z-10">
              <div v-for="day in weekDays" :key="day" class="p-4 text-center">
                <span class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">{{ day }}</span>
              </div>
            </div>

            <!-- Loader Central -->
            <div v-if="loading" class="absolute inset-0 z-20 flex items-center justify-center bg-white/50 backdrop-blur-sm">
              <LoadingIndicator class="w-10 h-10 text-intimar-primary" />
            </div>

            <!-- Grilla de Días -->
            <div class="flex-1 grid grid-cols-7 auto-rows-fr">
              <div 
                v-for="(day, index) in calendarDays" 
                :key="index"
                @click="day.date && openDayDetails(day)"
                class="border-r border-b border-gray-100 p-2 sm:p-4 transition-all duration-200 group relative min-h-[120px]"
                :class="[
                  !day.isCurrentMonth ? 'bg-gray-50/50 opacity-50 cursor-not-allowed' : 'bg-white cursor-pointer hover:bg-intimar-primary/5',
                  isToday(day.date) ? 'ring-2 ring-inset ring-intimar-primary/20 bg-intimar-primary/5' : '',
                  selectedDay === day.date ? 'ring-2 ring-inset ring-intimar-primary bg-intimar-primary/10 shadow-inner' : ''
                ]"
              >
                <div v-if="day.date" class="flex flex-col h-full">
                  <div class="flex justify-between items-start mb-2">
                    <span 
                      class="w-8 h-8 flex items-center justify-center rounded-full text-sm font-black transition-colors"
                      :class="[
                        isToday(day.date) ? 'bg-intimar-primary text-white shadow-md' : 'text-gray-700 group-hover:text-intimar-primary',
                        selectedDay === day.date && !isToday(day.date) ? 'bg-intimar-primary/20 text-intimar-primary' : ''
                      ]"
                    >
                      {{ day.dayNumber }}
                    </span>
                    
                    <span v-if="day.reservations.length > 0" class="text-[9px] font-black tracking-widest text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full">
                      {{ day.totalPax }} PAX
                    </span>
                  </div>

                  <!-- Indicadores de Reservas (Max 3) -->
                  <div class="flex-1 flex flex-col gap-1.5 justify-end">
                    <div 
                      v-for="(res, i) in day.reservations.slice(0, 3)" 
                      :key="i"
                      class="text-[10px] font-bold px-2 py-1 rounded-lg truncate transition-all shadow-sm border border-transparent"
                      :class="getStatusColor(res.estado_reserva)"
                    >
                      <span class="font-black">{{ res.hora_reserva.substring(0,5) }}</span> - {{ res.nombre }}
                    </div>
                    <div v-if="day.reservations.length > 3" class="text-[9px] font-bold text-gray-400 text-center py-0.5 bg-gray-50 rounded-lg">
                      +{{ day.reservations.length - 3 }} más
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <template v-else-if="currentView === 'week'">
            <div class="grid grid-cols-7 border-b border-gray-100 bg-white sticky top-0 z-10">
              <div v-for="(day, index) in calendarWeekDays" :key="index" class="p-4 text-center border-r border-gray-100 last:border-0 flex flex-col items-center">
                <span class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">{{ weekDays[index] }}</span>
                <span class="text-xl font-black" :class="isToday(day.date) ? 'text-intimar-primary' : 'text-gray-900'">{{ day.dayNumber }}</span>
              </div>
            </div>
            <div class="flex-1 grid grid-cols-7 bg-white">
              <div v-for="(day, index) in calendarWeekDays" :key="index" class="border-r border-gray-100 p-2 sm:p-4 min-h-[500px]">
                <div class="flex flex-col gap-3">
                  <div v-for="res in day.reservations" :key="res.name" @click="router.push(`/reservas/${res.name}`)" class="bg-white border border-gray-100 p-3 rounded-2xl shadow-sm hover:shadow-md transition-all cursor-pointer hover:border-intimar-primary/20 relative group">
                     <span class="text-[9px] font-black bg-gray-50 px-2 py-1 rounded-lg text-gray-500">{{ res.hora_reserva.substring(0,5) }}</span>
                     <h4 class="font-black text-[11px] text-gray-900 mt-2 truncate">{{ res.nombre }}</h4>
                     <div class="flex items-center gap-1.5 mt-1">
                        <span class="w-2 h-2 rounded-full" :class="getDotColor(res.estado_reserva)"></span>
                        <span class="text-[9px] font-bold text-gray-400">{{ (res.cant_adultos || 0) + (res.cant_ninos || 0) }} PAX</span>
                     </div>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <template v-else-if="currentView === 'day'">
            <div class="flex-1 overflow-auto bg-white p-6 md:p-12">
               <div class="max-w-3xl mx-auto">
                  <div class="flex items-center justify-between mb-8 pb-4 border-b border-gray-100">
                    <div class="flex items-center gap-4">
                      <div class="w-12 h-12 bg-intimar-primary/10 rounded-2xl flex items-center justify-center text-intimar-primary font-black text-xl">
                        {{ currentDayData.date ? currentDayData.date.split('-')[2] : '--' }}
                      </div>
                      <div>
                        <p class="text-2xl font-black text-gray-900 italic tracking-tight">{{ currentDayData.reservations.length }} Reservas</p>
                        <p class="text-[10px] font-bold text-intimar-primary uppercase tracking-[0.2em]">{{ currentDayData.totalPax }} Personas en Total</p>
                      </div>
                    </div>
                  </div>

                  <div v-if="currentDayData.reservations.length === 0" class="text-center py-20 opacity-40">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-4"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                    <p class="font-black text-xl italic">Sin reservas</p>
                  </div>

                  <div v-else class="relative border-l-2 border-gray-100 ml-4 space-y-8 pb-8">
                    <div v-for="res in currentDayData.reservations" :key="res.name" class="relative pl-8">
                      <div class="absolute -left-[9px] top-1 w-4 h-4 rounded-full border-4 border-white shadow-sm" :class="getDotColor(res.estado_reserva)"></div>
                      <div @click="router.push(`/reservas/${res.name}`)" class="bg-white border border-gray-100 p-6 rounded-[2rem] shadow-sm hover:shadow-lg transition-all group cursor-pointer hover:border-intimar-primary/20 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div>
                          <div class="flex items-center gap-3 mb-2">
                            <span class="font-black text-2xl tracking-tighter text-gray-900">{{ res.hora_reserva.substring(0,5) }}</span>
                            <span class="text-[9px] font-black uppercase tracking-[0.2em] px-2 py-1 rounded-full border" :class="getStatusBadge(res.estado_reserva)">{{ res.estado_reserva }}</span>
                          </div>
                          <h4 class="font-black text-xl italic text-intimar-primary leading-tight">{{ res.nombre }}</h4>
                        </div>
                        <div class="flex items-center gap-4 text-xs font-bold text-gray-500 uppercase tracking-widest bg-gray-50 px-4 py-3 rounded-2xl">
                          <span class="flex items-center gap-2 text-intimar-red"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> {{ (res.cant_adultos || 0) + (res.cant_ninos || 0) }} PAX</span>
                          <span class="w-1 h-1 rounded-full bg-gray-300"></span>
                          <span class="flex items-center gap-2"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><polyline points="10 9 9 9 8 9"/></svg> ID: {{ res.name.split('-').pop() }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
               </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- Panel Lateral: Detalles del Día -->
    <Teleport to="body">
      <div 
        class="fixed inset-0 z-[200] flex transition-all duration-500"
        :class="showSidePanel ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'"
      >
        <!-- Overlay -->
        <div 
          class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity duration-500"
          :class="showSidePanel ? 'opacity-100' : 'opacity-0'"
          @click="closeDayDetails"
        ></div>

        <!-- Sidebar Panel -->
        <div 
          class="absolute top-0 right-0 h-full w-full max-w-md bg-white shadow-2xl transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] flex flex-col"
          :class="showSidePanel ? 'translate-x-0' : 'translate-x-full'"
        >
          <!-- Panel Header -->
          <div class="p-8 border-b border-gray-100 flex justify-between items-start bg-gray-50/50">
            <div>
              <h2 class="text-3xl font-black italic text-gray-900 tracking-tight">{{ selectedDayFormatted }}</h2>
              <div class="mt-2 flex items-center justify-between gap-4">
                <p class="text-[11px] font-black text-intimar-red uppercase tracking-[0.2em] bg-intimar-red/10 px-3 py-1.5 rounded-xl inline-block border border-intimar-red/20 shadow-sm">
                  {{ selectedDayReservations.length }} Reservas • {{ selectedDayPax }} PAX Totales
                </p>
                <select v-model="selectedTimeFilter" class="bg-white border border-gray-100 rounded-xl px-3 py-1.5 text-[10px] font-bold text-gray-600 uppercase tracking-widest outline-none focus:ring-2 focus:ring-intimar-primary/20">
                  <option value="Todas">Todas las horas</option>
                  <option value="11">11:00 - 11:59</option>
                  <option value="12">12:00 - 12:59</option>
                  <option value="13">13:00 - 13:59</option>
                  <option value="14">14:00 - 14:59</option>
                  <option value="15">15:00 - 15:59</option>
                  <option value="16">16:00 - 16:59</option>
                  <option value="17">17:00 - 17:59</option>
                </select>
              </div>
            </div>
            <button @click="closeDayDetails" class="p-2 bg-white rounded-full text-gray-400 hover:text-gray-900 shadow-sm border border-gray-100 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            </button>
          </div>

          <!-- Panel Body (Lista de Reservas por Hora) -->
          <div class="flex-1 overflow-y-auto p-6 space-y-6">
            <div v-if="selectedDayReservations.length === 0" class="text-center py-20 opacity-40">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-4"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
              <p class="font-black text-xl italic">Sin reservas</p>
              <p class="text-xs font-bold uppercase tracking-widest mt-1">Para este día</p>
            </div>

            <!-- Timeline de Reservas -->
            <div v-else class="relative border-l-2 border-gray-100 ml-4 space-y-8 pb-8">
              <div 
                v-for="res in filteredDayReservations" 
                :key="res.name"
                class="relative pl-6"
              >
                <!-- Timeline Dot -->
                <div 
                  class="absolute -left-[9px] top-1 w-4 h-4 rounded-full border-4 border-white shadow-sm"
                  :class="getDotColor(res.estado_reserva)"
                ></div>

                <!-- Tarjeta de Reserva -->
                <div @click="router.push(`/reservas/${res.name}`)" class="bg-white border border-gray-100 p-5 rounded-[2rem] shadow-sm hover:shadow-lg transition-all group cursor-pointer hover:border-intimar-primary/20 relative">
                  <div class="absolute top-5 right-5 text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>
                  </div>
                  <div class="flex justify-between items-start mb-3 pr-6">
                    <span class="font-black text-xl tracking-tighter text-gray-900">{{ res.hora_reserva.substring(0,5) }}</span>
                    <span 
                      class="text-[9px] font-black uppercase tracking-[0.2em] px-2 py-1 rounded-full border"
                      :class="getStatusBadge(res.estado_reserva)"
                    >
                      {{ res.estado_reserva }}
                    </span>
                  </div>

                  <h4 class="font-black text-lg italic text-intimar-primary leading-tight truncate mb-1">{{ res.nombre }}</h4>
                  <div class="flex items-center gap-2 text-[10px] font-bold text-gray-400 uppercase tracking-widest mt-3">
                    <span class="flex items-center gap-1.5"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> {{ (res.cant_adultos || 0) + (res.cant_ninos || 0) }} PAX</span>
                    <span class="w-1 h-1 rounded-full bg-gray-200"></span>
                    <span class="flex items-center gap-1.5 truncate"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><polyline points="10 9 9 9 8 9"/></svg> Reserva: {{ res.name.split('-').pop() }}</span>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <!-- Botón ir a tabla de reservas filtrada -->
          <div class="p-6 border-t border-gray-100 bg-white">
            <button @click="irAReservasDelDia" class="w-full py-4 bg-gray-900 hover:bg-intimar-primary text-white font-black uppercase tracking-widest text-[10px] rounded-2xl shadow-xl transition-all flex justify-center items-center gap-2">
              Ver en Tabla Completa
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { call, LoadingIndicator } from 'frappe-ui'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const loading = ref(true)
const rawReservations = ref([])

// Calendar State
const currentView = ref('month')
const currentDate = ref(new Date())
const weekDays = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
const selectedDay = ref(null)
const showSidePanel = ref(false)
const selectedTimeFilter = ref('Todas')

// Formatting utilities
const currentDateFormatted = computed(() => {
  return currentDate.value.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' })
})

const currentMonthName = computed(() => {
  return currentDate.value.toLocaleString('es-ES', { month: 'long' })
})
const currentYear = computed(() => {
  return currentDate.value.getFullYear()
})

const isToday = (dateString) => {
  if (!dateString) return false
  const today = new Date()
  const d = new Date(dateString + 'T00:00:00')
  return d.getDate() === today.getDate() && 
         d.getMonth() === today.getMonth() && 
         d.getFullYear() === today.getFullYear()
}

// Fetch Reservations for the current month view
const fetchMonthReservations = async () => {
  loading.value = true
  try {
    const year = currentDate.value.getFullYear()
    const month = currentDate.value.getMonth()
    
    // Obtenemos un rango amplio para incluir días previos/siguientes visibles en la grilla
    const firstDayOfMonth = new Date(year, month, 1)
    const lastDayOfMonth = new Date(year, month + 1, 0)
    
    // Restamos 7 días al inicio y sumamos 7 al final para la grilla
    const startDate = new Date(firstDayOfMonth)
    startDate.setDate(startDate.getDate() - 7)
    
    const endDate = new Date(lastDayOfMonth)
    endDate.setDate(endDate.getDate() + 7)

    const startDateStr = startDate.toISOString().split('T')[0]
    const endDateStr = endDate.toISOString().split('T')[0]

    const data = await call('frappe.client.get_list', {
      doctype: 'Reserva Intimar',
      fields: ['name', 'fecha_reserva', 'hora_reserva', 'nombre', 'estado_reserva', 'cant_adultos', 'cant_ninos'],
      filters: [
        ['fecha_reserva', 'between', [startDateStr, endDateStr]],
        ['docstatus', '<', 2] // Ignorar eliminadas
      ],
      limit_page_length: 2000,
      order_by: 'hora_reserva asc'
    })
    
    rawReservations.value = data || []
  } catch (error) {
    console.error('Error fetching calendar data:', error)
  } finally {
    loading.value = false
  }
}

// Calendar Generator
const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  
  const firstDayOfMonth = new Date(year, month, 1)
  const lastDayOfMonth = new Date(year, month + 1, 0)
  
  const daysInMonth = lastDayOfMonth.getDate()
  
  // getDay() retorna 0 para Domingo, ajustamos para que Lunes sea 0
  let startingDayIndex = firstDayOfMonth.getDay() - 1
  if (startingDayIndex === -1) startingDayIndex = 6 // Domingo
  
  const days = []
  
  // Días del mes anterior
  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = startingDayIndex - 1; i >= 0; i--) {
    days.push({
      date: null,
      dayNumber: prevMonthLastDay - i,
      isCurrentMonth: false,
      reservations: [],
      totalPax: 0
    })
  }
  
  // Días del mes actual
  for (let i = 1; i <= daysInMonth; i++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    
    // Filtrar reservas para este día
    const dayReservations = rawReservations.value.filter(r => r.fecha_reserva === dateStr)
    const pax = dayReservations.reduce((acc, curr) => acc + (curr.cant_adultos || 0) + (curr.cant_ninos || 0), 0)

    days.push({
      date: dateStr,
      dayNumber: i,
      isCurrentMonth: true,
      reservations: dayReservations,
      totalPax: pax
    })
  }
  
  // Completar grilla hasta tener múltiplos de 7 (filas completas)
  const totalDaysSoFar = days.length
  const daysToFill = Math.ceil(totalDaysSoFar / 7) * 7 - totalDaysSoFar
  
  for (let i = 1; i <= daysToFill; i++) {
    days.push({
      date: null,
      dayNumber: i,
      isCurrentMonth: false,
      reservations: [],
      totalPax: 0
    })
  }
  
  return days
})

const calendarWeekDays = computed(() => {
  // Find the monday of the current week
  const date = new Date(currentDate.value)
  const day = date.getDay()
  const diff = date.getDate() - day + (day === 0 ? -6 : 1) // adjust when day is sunday
  const monday = new Date(date.setDate(diff))
  
  const week = []
  for (let i = 0; i < 7; i++) {
    const d = new Date(monday)
    d.setDate(monday.getDate() + i)
    const dateStr = d.toISOString().split('T')[0]
    
    const dayReservations = rawReservations.value.filter(r => r.fecha_reserva === dateStr)
    const pax = dayReservations.reduce((acc, curr) => acc + (curr.cant_adultos || 0) + (curr.cant_ninos || 0), 0)

    week.push({
      date: dateStr,
      dayNumber: d.getDate(),
      reservations: dayReservations,
      totalPax: pax
    })
  }
  return week
})

const currentDayData = computed(() => {
  const dateStr = currentDate.value.toISOString().split('T')[0]
  const dayReservations = rawReservations.value.filter(r => r.fecha_reserva === dateStr)
  const pax = dayReservations.reduce((acc, curr) => acc + (curr.cant_adultos || 0) + (curr.cant_ninos || 0), 0)
  return {
    date: dateStr,
    reservations: dayReservations,
    totalPax: pax
  }
})

// Navigation
const prevPeriod = () => {
  if (currentView.value === 'month') {
    currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
  } else if (currentView.value === 'week') {
    currentDate.value = new Date(currentDate.value.setDate(currentDate.value.getDate() - 7))
  } else {
    currentDate.value = new Date(currentDate.value.setDate(currentDate.value.getDate() - 1))
  }
  fetchMonthReservations()
}

const nextPeriod = () => {
  if (currentView.value === 'month') {
    currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
  } else if (currentView.value === 'week') {
    currentDate.value = new Date(currentDate.value.setDate(currentDate.value.getDate() + 7))
  } else {
    currentDate.value = new Date(currentDate.value.setDate(currentDate.value.getDate() + 1))
  }
  fetchMonthReservations()
}

const goToToday = () => {
  currentDate.value = new Date()
  fetchMonthReservations()
  selectedDay.value = currentDate.value.toISOString().split('T')[0]
}

// Side Panel Logic
const selectedDayData = computed(() => {
  if (!selectedDay.value) return null
  return calendarDays.value.find(d => d.date === selectedDay.value)
})

const selectedDayReservations = computed(() => {
  return selectedDayData.value?.reservations || []
})

const filteredDayReservations = computed(() => {
  const res = selectedDayReservations.value
  if (selectedTimeFilter.value === 'Todas') return res
  
  const selectedHour = parseInt(selectedTimeFilter.value)
  return res.filter(r => parseInt(r.hora_reserva.split(':')[0]) === selectedHour)
})

const selectedDayPax = computed(() => {
  return selectedDayData.value?.totalPax || 0
})

const selectedDayFormatted = computed(() => {
  if (!selectedDay.value) return ''
  const d = new Date(selectedDay.value + 'T00:00:00')
  return d.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' })
})

const openDayDetails = (day) => {
  if (!day.isCurrentMonth) return
  selectedDay.value = day.date
  showSidePanel.value = true
}

const closeDayDetails = () => {
  showSidePanel.value = false
  selectedDay.value = null
}

const irAReservasDelDia = () => {
  // Redirigir a reservas pasando el filtro de fecha por query (esto requiere que Reservas lo soporte, si no, lo podemos implementar luego)
  router.push({ path: '/reservas', query: { fecha: selectedDay.value } })
}

// Colors and Styles logic
const getStatusColor = (status) => {
  switch (status) {
    case 'Confirmada':
      return 'bg-intimar-green/10 text-intimar-green border-intimar-green/20'
    case 'Pendiente':
      return 'bg-intimar-gold/10 text-intimar-gold border-intimar-gold/20'
    case 'Cancelada':
    case 'No Asistió':
      return 'bg-intimar-red/10 text-intimar-red border-intimar-red/20'
    default:
      return 'bg-gray-100 text-gray-500 border-gray-200'
  }
}

const getDotColor = (status) => {
  switch (status) {
    case 'Confirmada': return 'bg-intimar-green'
    case 'Pendiente': return 'bg-intimar-gold'
    case 'Cancelada':
    case 'No Asistió': return 'bg-intimar-red'
    default: return 'bg-gray-400'
  }
}

const getStatusBadge = (status) => {
  switch (status) {
    case 'Confirmada':
      return 'bg-intimar-green/10 text-intimar-green border-intimar-green/20'
    case 'Pendiente':
      return 'bg-intimar-gold/10 text-intimar-gold border-intimar-gold/20'
    case 'Cancelada':
    case 'No Asistió':
      return 'bg-intimar-red/10 text-intimar-red border-intimar-red/20'
    default:
      return 'bg-gray-100 text-gray-500 border-gray-200'
  }
}

onMounted(() => {
  fetchMonthReservations()
})
</script>
