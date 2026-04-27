<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />
    <div class="flex-1 p-4 pb-28 md:p-8 md:pb-8 overflow-y-auto">
      <div class="max-w-[1400px] mx-auto space-y-8">
        
        <!-- Header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 md:gap-0 bg-white p-6 rounded-[2.5rem] shadow-sm border border-gray-100 relative overflow-hidden animate-in fade-in slide-in-from-top-4 duration-500">
          <div class="absolute right-0 top-0 w-64 h-64 bg-intimar-gold/5 rounded-full -mr-20 -mt-20 blur-3xl"></div>
          <div class="relative z-10 flex items-center gap-6">
            <div class="w-16 h-16 bg-gradient-to-br from-intimar-primary to-intimar-dark rounded-2xl flex items-center justify-center shadow-lg shadow-intimar-primary/20 shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/><path d="M16 18h.01"/></svg>
            </div>
            <div>
              <h1 class="text-3xl md:text-4xl font-black text-gray-900 tracking-tight italic">Gestión de Reservas</h1>
              <p class="text-gray-500 font-bold uppercase tracking-widest text-[10px] md:text-xs mt-1">
                {{ statsLoading ? 'Calculando...' : `${stats.reservas} Reservas • ${stats.personas} Personas` }}
              </p>
            </div>
          </div>
          
          <router-link to="/reservas/nueva" class="relative z-10 w-full md:w-auto justify-center bg-intimar-primary hover:bg-intimar-dark text-white font-black uppercase tracking-widest text-[11px] py-4 px-8 rounded-2xl shadow-xl shadow-intimar-primary/20 transition-all flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
            NUEVA RESERVA
          </router-link>
        </div>

        <!-- Filtros Component -->
        <ReservasFilter @filter="applyFilters" class="animate-in fade-in slide-in-from-top-4 duration-500 delay-75" />

        <!-- Tabla Component -->
        <ReservasTable :reservas="filteredReservas" :loading="loading" @refresh="fetchReservas" @asignar="openAsignarModal" class="animate-in fade-in slide-in-from-bottom-4 duration-500 delay-150" />

        <!-- Controles Inferiores (Orden y Paginación) -->
        <div v-if="!loading && filteredReservas && filteredReservas.length > 0" class="mt-4 flex flex-col sm:flex-row justify-between items-center gap-4 px-2 animate-in fade-in slide-in-from-bottom-4 duration-500 delay-200">
          
          <!-- Ordenamiento -->
          <div class="flex items-center gap-2">
            <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Creación:</span>
            <select 
              v-model="sortCreationOrder" 
              class="text-[10px] uppercase font-black tracking-widest text-gray-700 bg-white border border-gray-100 rounded-xl px-3 py-1.5 focus:ring-0 focus:border-intimar-primary outline-none shadow-sm cursor-pointer"
            >
              <option value="desc">Últimas Creadas Primero</option>
              <option value="asc">Primeras Creadas Inicio</option>
            </select>
          </div>

          <div class="flex flex-col sm:flex-row items-center gap-4">
            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest hidden sm:block">
              Mostrando {{ filteredReservas.length }} registros
            </p>
          <div class="flex items-center gap-4 bg-white px-3 py-1.5 rounded-xl shadow-sm border border-gray-100">
            <button 
              :disabled="currentPage === 1"
              @click="currentPage--"
              class="text-gray-400 hover:text-intimar-primary disabled:opacity-30 disabled:hover:text-gray-400 transition-colors flex items-center p-1"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
            </button>
            <span class="text-[10px] font-black uppercase tracking-widest text-gray-700">
              PÁGINA {{ currentPage }}
            </span>
            <button 
              :disabled="!filteredReservas || filteredReservas.length < pageSize"
              @click="currentPage++"
              class="text-gray-400 hover:text-intimar-primary disabled:opacity-30 disabled:hover:text-gray-400 transition-colors flex items-center p-1"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
            </button>
          </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Modal Asignar Mesa Rapida -->
    <Teleport to="body">
      <div v-if="showAsignarModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm" @click="closeAsignarModal"></div>
        
        <div class="bg-white rounded-[2rem] w-full max-w-md shadow-2xl relative z-10 overflow-hidden animate-in zoom-in-95 duration-200">
          <div class="p-6 md:p-8">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-black text-gray-900 tracking-tight italic">Asignar Mesa</h3>
              <button @click="closeAsignarModal" class="text-gray-400 hover:text-gray-900 transition-colors p-2 rounded-xl hover:bg-gray-100">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>

            <div class="space-y-4">
              <!-- Detalles Reserva -->
              <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100">
                <p class="text-xs font-black text-gray-500 uppercase tracking-widest mb-1">Reserva Seleccionada</p>
                <p class="text-sm font-bold text-gray-900">{{ reservaToAssign?.nombre }}</p>
                <p class="text-xs text-gray-500 font-bold">{{ reservaToAssign?.cant_adultos || 0 }} Adul. • {{ reservaToAssign?.cant_ninos || 0 }} Niñ.</p>
              </div>

              <!-- Select Mesa -->
              <div>
                <label class="block text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2 ml-1">Mesa Libre</label>
                <div class="relative">
                  <select 
                    v-model="asignarForm.mesa"
                    class="w-full appearance-none bg-gray-50 border-2 border-gray-100 text-gray-900 text-sm font-bold rounded-xl focus:ring-0 focus:border-intimar-primary block p-3.5 pr-10 transition-all cursor-pointer"
                  >
                    <option value="" disabled>Selecciona una mesa...</option>
                    <option v-for="m in mesasLibres" :key="m.name" :value="m.name">
                      {{ m.numero_mesa }} - {{ m.ubicacion_mesa || 'Principal' }}
                    </option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
                  </div>
                </div>
              </div>

              <!-- Select Mozo (Opcional) -->
              <div>
                <label class="block text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2 ml-1">Mozo (Opcional)</label>
                <div class="relative">
                  <select 
                    v-model="asignarForm.mozo"
                    class="w-full appearance-none bg-gray-50 border-2 border-gray-100 text-gray-900 text-sm font-bold rounded-xl focus:ring-0 focus:border-intimar-primary block p-3.5 pr-10 transition-all cursor-pointer"
                  >
                    <option value="">Sin mozo específico</option>
                    <option v-for="m in mozos" :key="m.name" :value="m.name">
                      {{ m.nombre }} {{ m.apellido || '' }}
                    </option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer -->
            <div class="mt-8 flex gap-3">
              <button 
                @click="closeAsignarModal"
                class="flex-1 px-6 py-4 rounded-xl text-xs font-black uppercase tracking-widest text-gray-500 bg-gray-100 hover:bg-gray-200 transition-colors"
              >
                Cancelar
              </button>
              <button 
                @click="submitAsignar"
                :disabled="!asignarForm.mesa || isSubmitting"
                class="flex-1 px-6 py-4 rounded-xl text-xs font-black uppercase tracking-widest text-white bg-intimar-primary hover:bg-intimar-dark transition-colors disabled:opacity-50 shadow-lg shadow-intimar-primary/20 flex justify-center items-center gap-2"
              >
                <svg v-if="isSubmitting" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                Asignar
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
    <!-- Toasts -->
    <Teleport to="body">
      <div class="fixed top-4 right-4 z-[200] flex flex-col gap-2 pointer-events-none">
        <TransitionGroup name="toast-slide">
          <div 
            v-for="toast in toasts" 
            :key="toast.id"
            class="flex items-center gap-3 px-4 py-3 rounded-2xl shadow-xl text-white font-black max-w-sm pointer-events-auto"
            :class="{
              'bg-green-600/90': toast.type === 'success',
              'bg-red-600/90': toast.type === 'error',
              'bg-intimar-gold/90': toast.type === 'warning'
            }"
          >
            <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            <svg v-if="toast.type === 'error'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
            <div class="flex-1">
              <h4 class="text-sm tracking-wide">{{ toast.title }}</h4>
              <p v-if="toast.message" class="text-[11px] opacity-80 font-medium mt-0.5">{{ toast.message }}</p>
            </div>
          </div>
        </TransitionGroup>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import ReservasFilter from '@/components/Reservas/ReservasFilter.vue'
import ReservasTable from '@/components/Reservas/ReservasTable.vue'
import { call, Button } from 'frappe-ui'
import { watch } from 'vue'

const router = useRouter()

// Sistema de Toasts
const toasts = ref([])
let toastCounter = 0

const showToast = (title, message = '', type = 'success') => {
  const id = toastCounter++
  toasts.value.push({ id, title, message, type })
  setTimeout(() => {
    removeToast(id)
  }, 3000)
}

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

const reservas = ref([])
const activeFilters = ref({})
const loading = ref(true)

const currentPage = ref(1)
const pageSize = ref(20)
const sortCreationOrder = ref('desc')

// Función para atrapar los filtros emitidos por el componente ReservasFilter
const applyFilters = (filters) => {
  activeFilters.value = filters
}

const buildFilters = () => {
    let f = []
    if (activeFilters.value.nombre) f.push(['nombre', 'like', `%${activeFilters.value.nombre}%`])
    if (activeFilters.value.celular) f.push(['celular', 'like', `%${activeFilters.value.celular}%`])
    if (activeFilters.value.fecha) f.push(['fecha_reserva', '=', activeFilters.value.fecha])
    if (activeFilters.value.hora && activeFilters.value.hora !== 'Todas') f.push(['hora_reserva', '=', activeFilters.value.hora])
    if (activeFilters.value.estado && activeFilters.value.estado !== 'Todos') f.push(['estado_reserva', '=', activeFilters.value.estado])
    return f
}

// Watchers for filtering and pagination
watch(activeFilters, () => {
  currentPage.value = 1
  fetchReservas()
  fetchStats()
}, { deep: true })

watch(sortCreationOrder, () => {
  currentPage.value = 1
  fetchReservas()
})

watch(currentPage, () => {
  fetchReservas()
})

const filteredReservas = computed(() => reservas.value)

const fetchReservas = async () => {
  loading.value = true
  try {
    const data = await call('intimar_erp.api.get_reservas_list', {
      filters: buildFilters(),
      limit_start: (currentPage.value - 1) * pageSize.value,
      limit_page_length: pageSize.value,
      order_by: `creation ${sortCreationOrder.value}`
    })
    reservas.value = data
  } catch (error) {
    console.error('Error obteniendo reservas:', error)
  } finally {
    loading.value = false
  }
}

const stats = ref({ reservas: 0, personas: 0 })
const statsLoading = ref(false)

const fetchStats = async () => {
  statsLoading.value = true
  try {
    const data = await call('frappe.client.get_list', {
      doctype: 'Reserva Intimar',
      fields: ['cant_adultos', 'cant_ninos'],
      limit_page_length: 99999, // Obtener todos para contar
      filters: buildFilters()
    })
    
    let totalPersonas = 0
    data.forEach(r => {
      totalPersonas += (r.cant_adultos || 0) + (r.cant_ninos || 0)
    })
    
    stats.value = {
      reservas: data.length,
      personas: totalPersonas
    }
  } catch (error) {
    console.error('Error calculando estadísticas:', error)
  } finally {
    statsLoading.value = false
  }
}

// Lógica de Asignación Rápida de Mesa
const showAsignarModal = ref(false)
const isSubmitting = ref(false)
const reservaToAssign = ref(null)
const mesasLibres = ref([])
const mozos = ref([])
const asignarForm = ref({ mesa: '', mozo: '' })

const fetchMesasYMozos = async () => {
  try {
    const [m, mz] = await Promise.all([
      call('frappe.client.get_list', {
        doctype: 'Mesa Intimar',
        fields: ['name', 'numero_mesa', 'ubicacion_mesa'],
        filters: { estado_mesa: 1 },
        limit_page_length: 100
      }),
      call('frappe.client.get_list', {
        doctype: 'Mozo Intimar',
        fields: ['name', 'nombre', 'apellido'],
        limit_page_length: 100
      })
    ])
    mesasLibres.value = m
    mozos.value = mz
  } catch (err) {
    console.error('Error fetching mesas o mozos:', err)
  }
}

const openAsignarModal = async (reserva) => {
  reservaToAssign.value = reserva
  asignarForm.value = { mesa: '', mozo: '' }
  showAsignarModal.value = true
  // Cargar si están vacíos
  if (!mesasLibres.value.length || !mozos.value.length) {
    await fetchMesasYMozos()
  }
}

const closeAsignarModal = () => {
  showAsignarModal.value = false
  reservaToAssign.value = null
}

const submitAsignar = async () => {
  if (!asignarForm.value.mesa) return
  isSubmitting.value = true
  try {
    await call('intimar_erp.api.asignar_mesa_a_reserva', {
      reserva_id: reservaToAssign.value.name,
      mesa_id: asignarForm.value.mesa,
      mozo_id: asignarForm.value.mozo || null
    })
    closeAsignarModal()
    fetchReservas() // Refresca la tabla
    fetchStats()
    showToast('¡Mesa Asignada!', 'Se ha asignado la mesa a la reserva exitosamente.', 'success')
    
    // Redirigir al mapa de mesas después de un breve delay
    setTimeout(() => {
      router.push('/mapa-mesas')
    }, 1500)
  } catch (error) {
    console.error('Error al asignar mesa:', error)
    showToast('Error', 'Hubo un problema al asignar la mesa.', 'error')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchReservas()
  fetchStats()
})
</script>

<style scoped>
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.toast-slide-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}
.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}
</style>
