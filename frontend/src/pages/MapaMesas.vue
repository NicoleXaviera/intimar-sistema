<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />

    <div class="flex-1 p-6 md:p-12 pb-32 md:pb-12 overflow-y-auto">
      <div class="max-w-7xl mx-auto">

        <!-- Header -->
        <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-12 gap-6">
          <div class="flex items-center gap-4">
            <img :src="'/files/intimar-logo.png'" alt="Intimar Logo" class="h-12 w-auto" />
            <div>
              <h1 class="text-4xl font-black text-gray-900 tracking-tight">Mapa de Mesas</h1>
              <p class="text-gray-500 font-medium uppercase tracking-widest text-xs mt-1">Bay · Paracas · Gestión Real-Time</p>
            </div>
          </div>


          <div class="flex flex-wrap items-center gap-3 bg-white p-2 rounded-2xl shadow-sm border border-gray-100">
            <!-- Mesas -->
            <div class="px-4 py-2 bg-intimar-green/10 text-intimar-green rounded-xl text-xs font-black uppercase tracking-tight flex flex-col items-center">
              <span class="text-[9px] opacity-70">Mesas Libres</span>
              <span class="text-sm">{{ libres }}</span>
            </div>
            <div class="px-4 py-2 bg-intimar-red/10 text-intimar-red rounded-xl text-xs font-black uppercase tracking-tight flex flex-col items-center">
              <span class="text-[9px] opacity-70">Mesas Ocupadas</span>
              <span class="text-sm">{{ ocupadas }}</span>
            </div>
            
            <div class="w-px h-8 bg-gray-200 mx-1 hidden sm:block"></div>

            <!-- Personas -->
            <div class="px-4 py-2 bg-intimar-primary/10 text-intimar-primary rounded-xl text-xs font-black uppercase tracking-tight flex flex-col items-center">
              <span class="text-[9px] opacity-70">En Restaurante</span>
              <span class="text-sm">{{ personasEnRestaurante }} PERS.</span>
            </div>
            <div class="px-4 py-2 bg-intimar-gold/10 text-intimar-gold rounded-xl text-xs font-black uppercase tracking-tight flex flex-col items-center">
              <span class="text-[9px] opacity-70">Por Llegar</span>
              <span class="text-sm">{{ personasPorLlegar }} PERS.</span>
            </div>
            
            <Button icon="refresh-cw" variant="ghost" class="ml-2 text-gray-400 hover:text-gray-900" @click="mesas.fetch(); reservasPendientes.fetch()" />
          </div>
        </div>

        <!-- Filtro de Ubicaciones y Buscador -->
        <div v-if="!mesas.loading" class="mb-10 flex flex-col md:flex-row gap-4 justify-between items-start md:items-center">
          
          <div class="overflow-x-auto pb-2 custom-scrollbar w-full md:flex-1">
            <div class="flex items-center gap-3">
              <button 
                @click="activeFilter = 'Todas'"
                :class="['px-6 py-3 rounded-full text-xs font-black uppercase tracking-widest transition-all whitespace-nowrap border-2', activeFilter === 'Todas' ? 'bg-gray-900 border-gray-900 text-white shadow-xl shadow-gray-900/20' : 'bg-white border-transparent text-gray-400 hover:text-gray-900 hover:bg-gray-50']"
              >
                Todas
              </button>
              <button 
                v-for="ubi in ubicacionesUnicas" 
                :key="ubi"
                @click="activeFilter = ubi"
                :class="['px-6 py-3 rounded-full text-xs font-black uppercase tracking-widest transition-all whitespace-nowrap border-2', activeFilter === ubi ? 'bg-intimar-primary border-intimar-primary text-white shadow-xl shadow-intimar-primary/20' : 'bg-white border-transparent text-gray-400 hover:text-gray-900 hover:bg-gray-50']"
              >
                {{ ubi }}
              </button>
            </div>
          </div>

          <!-- Buscador General de Mesas -->
          <div class="relative w-full md:w-80 shrink-0">
            <input 
              v-model="searchQueryMesa"
              type="text" 
              placeholder="Buscar mesa, cliente o mozo..."
              class="w-full pl-12 pr-6 py-3.5 bg-white border-2 border-gray-100 rounded-full focus:bg-white focus:border-intimar-primary focus:ring-0 outline-none transition-all font-bold text-gray-700 placeholder:text-gray-300 text-sm shadow-sm hover:shadow-md"
            >
            <div class="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            </div>
          </div>
        </div>

        <div v-else class="flex justify-center py-20">
          <LoadingIndicator class="w-10 h-10 text-intimar-primary" />
        </div>

        <div v-if="!mesas.loading" class="space-y-16 pb-10">
          <div v-for="(mesasGrupo, ubicacion) in mesasAgrupadas" :key="ubicacion" class="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <!-- Título de Zona -->
            <div class="flex items-center gap-4 mb-6">
              <h2 class="text-xl font-black text-gray-900 tracking-tight italic uppercase">{{ ubicacion }}</h2>
              <div class="h-px bg-gray-200 flex-1"></div>
              <span class="text-[10px] font-black text-gray-400 uppercase tracking-widest bg-gray-100 px-3 py-1 rounded-full">{{ mesasGrupo.length }} Mesas</span>
            </div>

            <!-- Grid de Mesas de esa Zona -->
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-8">
              <div 
                v-for="mesa in mesasGrupo" 
                :key="mesa.name"
                @click="handleMesaClick(mesa)"
                class="group relative"
              >
                <div 
                  :class="[
                    'min-h-[220px] p-6 flex flex-col items-center justify-center rounded-[2.5rem] border-b-8 transition-all duration-300 shadow-lg hover:shadow-2xl cursor-pointer transform hover:-translate-y-2',
                    mesa.estado_mesa 
                        ? 'bg-white border-intimar-green text-gray-900 shadow-intimar-green/10' 
                        : 'bg-intimar-red border-[#a00e26] text-white shadow-intimar-red/30'
                  ]"
                >
                  <span class="text-6xl font-black tracking-tighter">{{ mesa.numero_mesa }}</span>
                  <span class="text-[10px] font-bold uppercase tracking-[0.2em] mt-1 opacity-60">
                    {{ mesa.ubicacion_mesa || 'Principal' }}
                  </span>

                  <div v-if="!mesa.estado_mesa && mesa.reserva" class="mt-4 w-full text-center space-y-1 bg-white/10 py-2 rounded-2xl">
                    <p class="text-xs font-black truncate px-2">{{ mesa.reserva.cliente_nombre }}</p>
                    <div class="flex items-center justify-center gap-2 text-[10px] opacity-90 font-bold uppercase">
                      <span>{{ mesa.reserva.hora_llegada }}</span>
                      <span>•</span>
                      <span>{{ mesa.reserva.mozo_nombre || 'Sin mozo' }}</span>
                    </div>
                    <p class="text-[10px] font-bold opacity-70">{{ mesa.reserva.cant_adultos + mesa.reserva.cant_ninos }} PERS.</p>
                  </div>
                  
                  <!-- Estado Visual -->
                  <div class="absolute top-6 right-6">
                      <div :class="['w-3 h-3 rounded-full', mesa.estado_mesa ? 'bg-intimar-green animate-pulse' : 'bg-white/40']"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
    </div>
    <!-- MODALES PERSONALIZADOS (USANDO TELEPORT PARA CONTROL TOTAL) -->
    <Teleport to="body">
        <!-- MODAL: ASIGNAR MESA -->
        <div v-if="showAssignModal" class="fixed inset-0 z-[9999] flex items-center justify-center p-4">
            <!-- Backdrop -->
            <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="showAssignModal = false"></div>
            
            <!-- Card del Modal -->
            <div class="relative bg-white w-full max-w-xl rounded-[2.5rem] shadow-2xl overflow-hidden transform transition-all animate-scaleIn border-none">
                <div class="p-6 sm:p-8">
                    <!-- Botón Cerrar Superior -->
                    <button @click="showAssignModal = false" class="absolute top-6 right-6 text-gray-300 hover:text-gray-900 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                    </button>

                    <!-- PASO 1: SELECCIONAR RESERVA -->
                    <div v-if="assignStep === 1" class="space-y-5">
                        <div>
                            <h3 class="text-3xl font-black text-gray-900 leading-tight italic tracking-tighter text-center">Mesa <span class="text-intimar-primary">{{ selectedMesa?.numero_mesa }}</span></h3>
                            <p class="text-gray-400 text-[9px] font-bold uppercase tracking-[0.2em] text-center mt-1">Paso 1: Seleccionar Reserva</p>
                        </div>

                        <!-- Buscador Compacto -->
                        <div class="relative group">
                            <input 
                                v-model="searchQuery"
                                type="text" 
                                placeholder="Buscar cliente..."
                                class="w-full pl-12 pr-6 py-4 bg-gray-50 border-2 border-transparent rounded-[1.2rem] focus:bg-white focus:border-intimar-primary focus:ring-0 outline-none transition-all font-bold text-gray-700 placeholder:text-gray-300 shadow-inner text-base"
                            >
                            <div class="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-intimar-primary transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                            </div>
                        </div>

                        <div v-if="reservasPendientes.loading" class="py-8 flex justify-center"><LoadingIndicator class="w-8 h-8 text-intimar-primary" /></div>
                        <div v-else-if="!filteredReservas.length" class="py-12 text-center bg-gray-50 rounded-[2rem] border-2 border-dashed border-gray-200">
                            <p class="text-gray-400 font-bold italic text-sm">No hay reservas</p>
                        </div>
                        <div v-else class="max-h-[350px] overflow-y-auto pr-1 space-y-3 custom-scrollbar">
                            <div 
                                v-for="res in filteredReservas" 
                                :key="res.name"
                                @click="selectReservaForAssign(res)"
                                class="p-5 bg-white border-2 border-gray-50 rounded-[1.8rem] hover:border-intimar-primary hover:shadow-xl hover:shadow-intimar-primary/5 cursor-pointer transition-all flex justify-between items-center group relative overflow-hidden"
                            >
                                <div class="flex-1">
                                    <div class="font-black text-lg text-gray-900 group-hover:text-intimar-primary transition-colors flex items-center gap-3">
                                        {{ res.cliente_nombre }}
                                    </div>
                                    <div class="flex items-center gap-3 mt-1">
                                        <span class="text-[9px] bg-gray-100 px-3 py-1 rounded-full font-black text-gray-500 uppercase tracking-widest">{{ res.hora_reserva }}</span>
                                        <span class="text-[9px] bg-intimar-gold/10 px-3 py-1 rounded-full font-black text-intimar-gold uppercase tracking-widest">{{ res.cant_adultos + res.cant_ninos }} PERS.</span>
                                    </div>
                                </div>
                                <div class="w-10 h-10 rounded-xl bg-gray-50 flex items-center justify-center group-hover:bg-intimar-primary group-hover:text-white transition-all text-gray-300">
                                     <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- PASO 2: SELECCIONAR MOZO -->
                    <div v-if="assignStep === 2" class="space-y-6">
                        <div class="text-center">
                            <button @click="assignStep = 1" class="text-intimar-primary text-[9px] font-black uppercase tracking-[0.2em] mb-2 flex items-center justify-center gap-2 hover:translate-x-[-4px] transition-transform mx-auto">
                                 <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
                                 VOLVER
                            </button>
                            <h3 class="text-3xl font-black text-gray-900 leading-tight italic tracking-tighter">Asignar <span class="text-intimar-primary">Mozo</span></h3>
                            <p class="text-gray-400 text-[10px] font-bold uppercase tracking-[0.2em] mt-1">{{ selectedReservaForAssign?.cliente_nombre }}</p>
                        </div>

                        <div v-if="mozos.loading" class="py-10 flex justify-center"><LoadingIndicator class="w-8 h-8 text-intimar-primary" /></div>
                        <div v-else class="grid grid-cols-2 gap-4 max-h-[350px] overflow-y-auto pr-1 custom-scrollbar">
                            <div 
                                v-for="mozo in mozos.data" 
                                :key="mozo.name"
                                @click="confirmarAsignacionFinal(mozo)"
                                class="p-5 bg-gray-50 border-2 border-transparent rounded-[2rem] hover:border-intimar-primary hover:bg-white hover:shadow-xl transition-all cursor-pointer text-center group"
                            >
                                <div class="w-14 h-14 bg-white shadow-md text-intimar-primary rounded-[1.2rem] flex items-center justify-center mx-auto mb-3 text-xl font-black italic group-hover:bg-intimar-primary group-hover:text-white transition-all">
                                    {{ mozo.nombre[0] }}
                                </div>
                                <p class="font-black text-gray-900 text-sm uppercase tracking-tight">{{ mozo.nombre }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Footer Compacto -->
                <div class="p-4 bg-gray-50 border-t border-gray-100 flex justify-center">
                    <button @click="showAssignModal = false" class="text-gray-400 hover:text-gray-900 font-black uppercase text-[10px] tracking-[0.4em] transition-colors">
                        [ CANCELAR ]
                    </button>
                </div>
            </div>
        </div>

        <!-- MODAL: LIBERAR MESA -->
        <div v-if="showReleaseModal" class="fixed inset-0 z-[9999] flex items-center justify-center p-4">
            <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="showReleaseModal = false"></div>
            
            <div class="relative bg-white w-full max-w-lg rounded-[2.5rem] shadow-2xl overflow-hidden animate-scaleIn">
                <div class="p-8">
                    <div class="mb-6 border-b border-gray-100 pb-4 text-center">
                        <h3 class="text-3xl font-black text-gray-900 italic tracking-tighter text-center">Mesa <span class="text-intimar-primary">{{ selectedMesa?.numero_mesa }}</span></h3>
                        <p class="text-gray-400 text-[10px] font-bold uppercase tracking-[0.2em] mt-1 text-center text-center">Finalizar Servicio</p>
                    </div>

                    <div v-if="selectedMesa?.reserva" class="bg-gray-50 p-7 rounded-[2.2rem] space-y-6 border border-gray-100 mb-6">
                        <div class="text-center">
                            <p class="text-[10px] uppercase text-gray-400 font-black tracking-[0.2em] mb-1">Cliente en mesa:</p>
                            <p class="font-black text-3xl text-intimar-primary leading-tight tracking-tight italic">{{ selectedMesa.reserva.cliente_nombre }}</p>
                            <p class="text-xs font-bold text-gray-400 mt-3 inline-block bg-white px-3 py-1.5 rounded-lg border border-gray-100 shadow-sm">
                                Reserva: <span class="text-gray-900 font-black">{{ selectedMesa.reserva.name.split('-').pop() }}</span>
                            </p>
                        </div>

                        <div class="flex justify-center gap-10 border-t border-gray-200 pt-6">
                            <div class="text-center">
                                <p class="text-[10px] uppercase text-gray-400 font-black tracking-[0.2em] mb-1 text-center">Llegada:</p>
                                <p class="font-black text-xl text-gray-700 tracking-tight text-center">{{ selectedMesa.reserva.hora_llegada }}</p>
                            </div>
                            <div class="text-center">
                                <p class="text-[10px] uppercase text-gray-400 font-black tracking-[0.2em] mb-1 text-center">Mozo:</p>
                                <p class="font-black text-xl text-gray-700 tracking-tight text-center">{{ selectedMesa.reserva.mozo_nombre || '---' }}</p>
                            </div>
                        </div>
                    </div>

                    <div class="flex items-center gap-5 text-intimar-red bg-intimar-red/5 p-6 rounded-[1.8rem] border-2 border-intimar-red/10">
                        <div class="w-12 h-12 shrink-0 rounded-2xl bg-intimar-red text-white flex items-center justify-center font-black italic shadow-lg text-xl">!</div>
                        <p class="text-xs font-black uppercase tracking-tight leading-relaxed">¿Confirmas la liberación?</p>
                    </div>
                </div>

                <div class="p-6 flex gap-4 w-full bg-gray-50 border-t border-gray-100">
                    <Button 
                        class="flex-[2] py-7 bg-intimar-red hover:bg-[#a00e26] text-white font-black rounded-2xl shadow-xl uppercase tracking-[0.2em] text-xs transition-all"
                        @click="confirmarLiberacion" 
                        :loading="releasing"
                    >
                        LIBERAR MESA
                    </Button>
                    <Button 
                        variant="ghost" 
                        class="flex-1 py-7 text-gray-400 font-black uppercase tracking-[0.2em] text-xs hover:text-gray-900" 
                        @click="showReleaseModal = false"
                    >
                        VOLVER
                    </Button>
                </div>
            </div>
        </div>
    </Teleport>

    <!-- Toasts -->
    <Teleport to="body">
      <div class="fixed top-4 right-4 z-[99999] flex flex-col gap-2 pointer-events-none">
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
  </div>
</template>


<script setup>
import { Button, LoadingIndicator, createResource, call, Dialog } from 'frappe-ui'
import { computed, ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'

const showAssignModal = ref(false)
const showReleaseModal = ref(false)
const selectedMesa = ref(null)
const releasing = ref(false)
const searchQuery = ref('')

const assignStep = ref(1)
const selectedReservaForAssign = ref(null)

// Recurso principal de mesas con datos de reserva
const mesas = createResource({
  url: 'intimar_erp.api.get_mesas_with_reserva',
  auto: true
})

// Recurso de reservas pendientes para hoy
const reservasPendientes = createResource({
  url: 'intimar_erp.api.get_reservas_pendientes_hoy',
})

// Recurso de mozos
const mozos = createResource({
  url: 'intimar_erp.api.get_mozos',
  auto: true
})

const libres = computed(() => mesas.data?.filter(m => m.estado_mesa).length || 0)
const ocupadas = computed(() => mesas.data?.filter(m => !m.estado_mesa).length || 0)
const reservasHoy = computed(() => reservasPendientes.data || [])

const personasEnRestaurante = computed(() => {
  if (!mesas.data) return 0
  return mesas.data.reduce((total, m) => {
    // Si la mesa está ocupada (estado_mesa = 0/false) y tiene reserva asignada
    if (!m.estado_mesa && m.reserva) {
      return total + (m.reserva.cant_adultos || 0) + (m.reserva.cant_ninos || 0)
    }
    return total
  }, 0)
})

const personasPorLlegar = computed(() => {
  if (!reservasPendientes.data) return 0
  return reservasPendientes.data.reduce((total, r) => {
    return total + (r.cant_adultos || 0) + (r.cant_ninos || 0)
  }, 0)
})

const activeFilter = ref('Todas')
const searchQueryMesa = ref('')

const ubicacionesUnicas = computed(() => {
  if (!mesas.data) return []
  const ubs = mesas.data.map(m => m.ubicacion_mesa || 'Principal')
  return [...new Set(ubs)].sort()
})

const filteredMesas = computed(() => {
  if (!mesas.data) return []
  
  let result = mesas.data

  // Filtro por ubicación
  if (activeFilter.value !== 'Todas') {
    result = result.filter(m => (m.ubicacion_mesa || 'Principal') === activeFilter.value)
  }

  // Filtro por texto (mesa, cliente, mozo)
  if (searchQueryMesa.value) {
    const q = searchQueryMesa.value.toLowerCase()
    result = result.filter(m => {
      const matchMesa = m.numero_mesa?.toString().includes(q)
      const matchCliente = m.reserva?.cliente_nombre?.toLowerCase().includes(q)
      const matchMozo = m.reserva?.mozo_nombre?.toLowerCase().includes(q)
      return matchMesa || matchCliente || matchMozo
    })
  }

  return result
})

const mesasAgrupadas = computed(() => {
  const grupos = {}
  
  filteredMesas.value.forEach(m => {
    const ubicacion = m.ubicacion_mesa || 'Principal'
    if (!grupos[ubicacion]) {
      grupos[ubicacion] = []
    }
    grupos[ubicacion].push(m)
  })

  // Ordenar cada grupo por numero_mesa inteligentemente
  Object.keys(grupos).forEach(k => {
    grupos[k].sort((a, b) => {
      const numA = a.numero_mesa?.toString() || ''
      const numB = b.numero_mesa?.toString() || ''
      return numA.localeCompare(numB, undefined, { numeric: true, sensitivity: 'base' })
    })
  })

  // Ordenar las llaves de ubicaciones alfabéticamente
  const orderedGrupos = {}
  Object.keys(grupos).sort().forEach(k => {
    orderedGrupos[k] = grupos[k]
  })

  return orderedGrupos
})

import { watch } from 'vue'
watch(() => mesas.data, (newData) => {
  console.log('MESAS DATA:', newData)
}, { deep: true })

watch(() => reservasPendientes.data, (newData) => {
  console.log('RESERVAS DATA:', newData)
}, { deep: true })

const filteredReservas = computed(() => {
  if (!searchQuery.value) return reservasHoy.value
  const q = searchQuery.value.toLowerCase()
  return reservasHoy.value.filter(res => 
    res.cliente_nombre.toLowerCase().includes(q) || 
    (res.cliente_telefono && res.cliente_telefono.includes(q))
  )
})

function handleMesaClick(mesa) {
  selectedMesa.value = mesa
  searchQuery.value = '' 
  assignStep.value = 1
  selectedReservaForAssign.value = null
  if (mesa.estado_mesa) {
    reservasPendientes.fetch()
    showAssignModal.value = true
  } else {
    showReleaseModal.value = true
  }
}

function selectReservaForAssign(reserva) {
  selectedReservaForAssign.value = reserva
  assignStep.value = 2
}

async function confirmarAsignacionFinal(mozo) {
  try {
    await call('intimar_erp.api.asignar_mesa_a_reserva', {
      reserva_id: selectedReservaForAssign.value.name,
      mesa_id: selectedMesa.value.name,
      mozo_id: mozo.name
    })
    showAssignModal.value = false
    mesas.fetch()
  } catch (e) {
    console.error(e)
  }
}


async function confirmarLiberacion() {
  releasing.value = true
  const reservaIdShort = selectedMesa.value.reserva?.name?.split('-').pop()
  try {
    await call('intimar_erp.api.liberar_mesa', {
      mesa_id: selectedMesa.value.name
    })
    showReleaseModal.value = false
    mesas.fetch()
    showToast('¡Mesa Liberada!', `La reserva ${reservaIdShort || ''} finalizó. Mesa disponible.`, 'success')
  } catch (e) {
    console.error(e)
    showToast('Error', 'No se pudo liberar la mesa', 'error')
  } finally {
    releasing.value = false
  }
}

// Sistema de Toasts
const toasts = ref([])
let toastCounter = 0

const showToast = (title, message = '', type = 'success') => {
  const id = toastCounter++
  toasts.value.push({ id, title, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 4000)
}
</script>

<style scoped>
.grid > div {
  animation: scaleIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) backwards;
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}

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
