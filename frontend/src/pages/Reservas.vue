<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />
    <div class="flex-1 p-4 pb-28 md:p-8 md:pb-8 overflow-y-auto overflow-x-hidden">
      <div class="w-full space-y-8">
        
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
          
          <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto relative z-10 items-center">
            <button 
              @click="exportToPDF" 
              class="justify-center bg-white/50 hover:bg-white text-gray-400 hover:text-intimar-primary font-black uppercase tracking-widest text-[9px] py-2 px-4 rounded-xl border border-gray-100 transition-all flex items-center gap-2 opacity-60 hover:opacity-100"
              title="Descargar listado actual en PDF"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
              PDF
            </button>
            
            <router-link to="/reservas/nueva" class="justify-center bg-intimar-primary hover:bg-intimar-dark text-white font-black uppercase tracking-widest text-[11px] py-4 px-8 rounded-2xl shadow-xl shadow-intimar-primary/20 transition-all flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
              NUEVA RESERVA
            </router-link>
          </div>
        </div>

        <!-- Dashboard de Aforo Rápido -->
        <div v-if="realtimeStats" class="grid grid-cols-1 md:grid-cols-4 gap-4 animate-in fade-in slide-in-from-top-4 duration-500 delay-75">
          <!-- Aforo Total -->
          <div class="bg-white p-5 rounded-[2rem] border border-gray-100 shadow-sm relative overflow-hidden group">
            <div class="absolute right-4 top-4 text-gray-100 group-hover:text-intimar-gold/20 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9Z"/><path d="M3 9V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4"/></svg>
            </div>
            <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">General</p>
            <h3 class="text-[10px] font-black text-gray-400 mb-1 italic uppercase">Aforo total</h3>
            <h2 class="text-3xl font-black text-intimar-dark tracking-tighter">{{ realtimeStats?.kpis?.aforo_total || 0 }}</h2>
          </div>

          <!-- Aforo Actual -->
          <div class="bg-intimar-primary p-5 rounded-[2rem] shadow-xl shadow-intimar-primary/20 relative overflow-hidden group">
            <div class="absolute right-4 top-4 text-white/10 group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            </div>
            <p class="text-[9px] font-black text-white/50 uppercase tracking-widest mb-1">En Intimar</p>
            <h3 class="text-[10px] font-black text-intimar-gold mb-1 italic uppercase">Aforo actual</h3>
            <h2 class="text-3xl font-black text-white leading-none tracking-tighter mb-1">{{ realtimeStats?.kpis?.personas_en_restaurante || 0 }}</h2>
            <p class="text-[9px] font-black text-white/40 uppercase tracking-widest">de {{ realtimeStats?.kpis?.reservas_en_proceso || 0 }} reservas</p>
          </div>

          <!-- Lista de Espera -->
          <div class="bg-white p-5 rounded-[2rem] border border-gray-100 shadow-sm relative group">
            <div class="absolute right-4 top-4 text-amber-500/10">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
            </div>
            <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">Por entrar</p>
            <h3 class="text-[10px] font-black text-amber-500 mb-1 italic uppercase">Lista de espera</h3>
            <h2 class="text-3xl font-black text-intimar-dark tracking-tighter mb-1">{{ realtimeStats?.kpis?.personas_en_espera || 0 }}</h2>
            <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest">de {{ realtimeStats?.kpis?.reservas_en_espera || 0 }} reservas</p>
          </div>

          <!-- Mesas Disponibles -->
          <div class="bg-white p-5 rounded-[2rem] border-2 border-emerald-500/20 shadow-sm relative group overflow-hidden">
            <div class="absolute right-4 top-4 text-emerald-500/10">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
            </div>
            <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">Disponibilidad</p>
            <h3 class="text-[10px] font-black text-emerald-500 mb-1 italic uppercase">Mesas libres</h3>
            <h2 class="text-3xl font-black text-intimar-dark tracking-tighter">{{ realtimeStats?.kpis?.mesas_disponibles || 0 }}</h2>
          </div>
        </div>

        <!-- Filtros Component -->
        <ReservasFilter @filter="applyFilters" class="animate-in fade-in slide-in-from-top-4 duration-500 delay-75" />

        <!-- Tabla Component -->
        <ReservasTable 
          :reservas="filteredReservas" 
          :loading="loading" 
          @refresh="fetchReservas" 
          @asignar="openAsignarModal" 
          @delete="handleDelete"
          class="animate-in fade-in slide-in-from-bottom-4 duration-500 delay-150" 
        />

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
              Mostrando {{ filteredReservas.length }} registros de {{ stats.reservas }} en total
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

    <!-- Modal Confirmación Eliminar (Custom) -->
    <Teleport to="body">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[110] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="closeDeleteModal"></div>
        <div class="bg-white rounded-[2.5rem] w-full max-w-sm shadow-2xl relative z-10 overflow-hidden animate-in zoom-in-95 duration-200 border border-gray-100">
          <div class="p-8 text-center">
            <div class="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
            </div>
            <h3 class="text-xl font-black text-gray-900 tracking-tight italic mb-2">¿Eliminar Reserva?</h3>
            <p class="text-sm font-bold text-gray-500 leading-relaxed mb-8 px-4">
              Estás por borrar la reserva de <span class="text-red-500">{{ reservaToDelete?.nombre }}</span>. Esta acción no se puede deshacer.
            </p>
            <div class="flex gap-3">
              <button 
                @click="closeDeleteModal"
                class="flex-1 px-6 py-4 rounded-xl text-xs font-black uppercase tracking-widest text-gray-400 bg-gray-100 hover:bg-gray-200 transition-colors"
              >
                No, Volver
              </button>
              <button 
                @click="confirmDelete"
                class="flex-1 px-6 py-4 rounded-xl text-xs font-black uppercase tracking-widest text-white bg-red-500 hover:bg-red-600 shadow-lg shadow-red-200 transition-all"
              >
                Sí, Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Toasts Premium -->
    <Teleport to="body">
      <div class="fixed top-6 right-6 z-[200] flex flex-col gap-3 pointer-events-none">
        <TransitionGroup name="toast-fancy">
          <div 
            v-for="toast in toasts" 
            :key="toast.id"
            class="flex items-center gap-4 px-6 py-4 rounded-[1.5rem] shadow-2xl backdrop-blur-md border pointer-events-auto min-w-[320px] max-w-md"
            :class="{
              'bg-emerald-500/90 border-emerald-400/30 text-white': toast.type === 'success',
              'bg-red-500/90 border-red-400/30 text-white': toast.type === 'error',
              'bg-intimar-gold/90 border-intimar-gold/30 text-white': toast.type === 'warning'
            }"
          >
            <div class="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center shrink-0 shadow-inner">
              <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              <svg v-if="toast.type === 'error'" xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </div>
            <div class="flex-1">
              <h4 class="text-sm font-black uppercase tracking-widest italic leading-tight">{{ toast.title }}</h4>
              <p v-if="toast.message" class="text-[11px] font-bold opacity-90 mt-0.5">{{ toast.message }}</p>
            </div>
            <button @click="removeToast(toast.id)" class="text-white/40 hover:text-white transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
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

const exportToPDF = () => {
  if (!window.jspdf) {
    showToast('Error', 'La librería de PDF aún se está cargando. Reintenta en un segundo.', 'error')
    return
  }
  
  const { jsPDF } = window.jspdf
  const doc = new jsPDF()
  
  // Estética del Header con el celeste de la marca (#00938F)
  doc.setFillColor(0, 147, 143) // RGB del #00938F
  doc.rect(0, 0, 210, 45, 'F')
  
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(24)
  doc.setFont('helvetica', 'bold')
  doc.text('INTIMAR', 14, 22)
  doc.setFontSize(14)
  doc.text('LISTADO DE RESERVAS', 14, 32)
  
  doc.setFontSize(9)
  doc.setFont('helvetica', 'normal')
  doc.text(`Generado el: ${new Date().toLocaleString()}`, 14, 40)
  
  // Filtros aplicados
  let filterText = "Reporte de disponibilidad basado en filtros actuales"
  if (activeFilters.value.fecha) filterText = `Reservas para el día: ${activeFilters.value.fecha}`
  
  doc.setTextColor(80, 80, 80)
  doc.setFontSize(9)
  doc.setFont('helvetica', 'bolditalic')
  doc.text(filterText, 14, 55)

  const columns = [
    { header: 'ID RESERVA', dataKey: 'nro' },
    { header: 'CLIENTE', dataKey: 'cliente' },
    { header: 'PERS.', dataKey: 'personas' },
    { header: 'FECHA', dataKey: 'fecha' },
    { header: 'HORA', dataKey: 'hora' },
    { header: 'ANTICIPO', dataKey: 'anticipo' }
  ]

  const rows = filteredReservas.value.map(res => {
    // Formatear fecha de YYYY-MM-DD a DD-MM-YYYY
    const dateParts = res.fecha_reserva?.split('-') || []
    const formattedDate = dateParts.length === 3 ? `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}` : res.fecha_reserva

    return {
      nro: res.name,
      cliente: res.nombre?.toUpperCase(),
      personas: (res.cant_adultos || 0) + (res.cant_ninos || 0),
      fecha: formattedDate,
      hora: `${res.hora_reserva} ${res.am_pm || ''}`,
      anticipo: res.total_pagado ? `S/ ${parseFloat(res.total_pagado).toFixed(2)}` : '---'
    }
  })

  doc.autoTable({
    columns: columns,
    body: rows,
    startY: 60,
    margin: { left: 10, right: 10 },
    styles: { 
      fontSize: 9, 
      cellPadding: 3,
      font: 'helvetica',
      valign: 'middle'
    },
    headStyles: { 
      fillColor: [0, 147, 143], 
      textColor: [255, 255, 255],
      fontStyle: 'bold',
      halign: 'center',
      fontSize: 10
    },
    columnStyles: {
      nro: { halign: 'center', fontStyle: 'bold', cellWidth: 35 },
      cliente: { fontStyle: 'bold', cellWidth: 45 },
      personas: { halign: 'center', cellWidth: 15 },
      fecha: { halign: 'center', cellWidth: 25 },
      hora: { halign: 'center', cellWidth: 25 },
      anticipo: { halign: 'right', fontStyle: 'bold', textColor: [0, 100, 0] }
    },
    alternateRowStyles: {
      fillColor: [245, 252, 252]
    }
  })

  doc.save(`reservas_intimar_${new Date().toISOString().split('T')[0]}.pdf`)
  showToast('¡PDF Generado!', 'El reporte se ha descargado correctamente.', 'success')
}

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
    if (activeFilters.value.id) f.push(['name', 'like', `%${activeFilters.value.id}%`])
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
const realtimeStats = ref(null)
const statsLoading = ref(false)

const fetchStats = async () => {
  statsLoading.value = true
  try {
    const [data, rStats] = await Promise.all([
      call('frappe.client.get_list', {
        doctype: 'Reserva Intimar',
        fields: ['cant_adultos', 'cant_ninos'],
        limit_page_length: 99999,
        filters: buildFilters()
      }),
      call('intimar_erp.api.get_dashboard_stats')
    ])
    
    let totalPersonas = 0
    data.forEach(r => {
      totalPersonas += (r.cant_adultos || 0) + (r.cant_ninos || 0)
    })
    
    stats.value = {
      reservas: data.length,
      personas: totalPersonas
    }
    realtimeStats.value = rStats
  } catch (error) {
    console.error('Error calculando estadísticas:', error)
  } finally {
    statsLoading.value = false
  }
}

const showDeleteModal = ref(false)
const reservaToDelete = ref(null)

const handleDelete = (reserva) => {
  reservaToDelete.value = reserva
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  reservaToDelete.value = null
}

const confirmDelete = async () => {
  if (!reservaToDelete.value) return
  
  try {
    const name = reservaToDelete.value.name
    const nombre = reservaToDelete.value.nombre
    
    await call('intimar_erp.api.delete_reserva', {
      name: name
    })
    
    showToast('Reserva Eliminada', `La reserva de ${nombre} ha sido borrada exitosamente.`, 'success')
    closeDeleteModal()
    fetchReservas()
    fetchStats()
  } catch (error) {
    console.error('Error eliminando reserva:', error)
    showToast('Error', 'No se pudo eliminar la reserva. Verifica tus permisos.', 'error')
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
.toast-fancy-enter-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.toast-fancy-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 1, 1);
}
.toast-fancy-enter-from {
  opacity: 0;
  transform: translateX(100px) scale(0.8);
}
.toast-fancy-leave-to {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}
</style>
