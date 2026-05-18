<template>
  <div class="min-h-screen bg-gray-50 flex overflow-x-hidden">
    <Sidebar />
    <div class="flex-1 p-4 pb-24 md:p-8 md:pb-8 overflow-y-auto mt-14 md:mt-0 transition-all duration-300">
      <div class="w-full space-y-6 md:space-y-8">
        
        <!-- Header Principal -->
        <div class="flex flex-col lg:flex-row justify-between items-stretch lg:items-center gap-4 bg-white p-5 md:p-8 rounded-[1.5rem] md:rounded-[2.5rem] shadow-sm border border-gray-100 relative z-30 animate-in fade-in slide-in-from-top-4 duration-500">
          <div class="absolute right-0 top-0 w-64 h-64 bg-intimar-gold/5 rounded-full -mr-20 -mt-20 blur-3xl hidden md:block"></div>
          
          <div class="relative z-10 flex items-center gap-4 md:gap-6 text-left">
            <div class="hidden md:flex w-16 h-16 bg-gradient-to-br from-intimar-primary to-intimar-dark rounded-2xl items-center justify-center shadow-lg shadow-intimar-primary/20 shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/><path d="M16 18h.01"/></svg>
            </div>
            <div>
              <h1 class="text-xl md:text-4xl font-black text-gray-900 tracking-tight italic leading-tight">Reservas</h1>
              <p class="text-gray-500 font-bold uppercase tracking-widest text-[8px] md:text-xs mt-0.5">
                {{ statsLoading ? 'Calculando...' : `${stats.reservas} Reservas • ${stats.personas} Personas` }}
              </p>
            </div>
          </div>
          
          <div class="flex flex-wrap items-center gap-2 md:gap-3 relative z-10">
            <button @click="openAforoRadar" class="flex-1 md:flex-none justify-center bg-gray-900 hover:bg-black text-white font-black uppercase tracking-widest text-[9px] md:text-[10px] py-3 md:py-4 px-5 md:px-6 rounded-xl md:rounded-2xl shadow-xl transition-all flex items-center gap-2">
              <div class="relative w-2.5 h-2.5"><div class="absolute inset-0 bg-[#00938f] rounded-full animate-ping opacity-75"></div><div class="relative bg-[#00938f] w-2.5 h-2.5 rounded-full border-2 border-white"></div></div>
              SIMULACIÓN
            </button>
            <button @click="exportToPDF" class="flex-none bg-white hover:bg-gray-50 text-gray-400 hover:text-intimar-primary font-black uppercase tracking-widest text-[9px] py-3 md:py-4 px-4 rounded-xl border border-gray-100 transition-all flex items-center gap-2" title="Descargar PDF">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
              PDF
            </button>

            <div class="relative" v-click-outside="() => showColumnToggle = false">
              <button @click="showColumnToggle = !showColumnToggle; showSortToggle = false" class="bg-white hover:bg-gray-50 text-gray-500 font-black uppercase tracking-widest text-[9px] py-3 md:py-4 px-4 rounded-xl border border-gray-100 transition-all flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3h10"/><path d="M12 12h10"/><path d="M12 21h10"/><path d="M3 3h1"/><path d="M3 12h1"/><path d="M3 21h1"/></svg>
                TABLA
              </button>
              <div v-if="showColumnToggle" class="absolute top-full right-0 mt-2 w-48 bg-white rounded-xl shadow-2xl border border-gray-100 py-2 z-[100] animate-in fade-in zoom-in-95 duration-200">
                <p class="px-4 py-1 text-[8px] font-black text-gray-400 uppercase tracking-widest mb-1">Ver en tabla:</p>
                <label v-for="(val, col) in columnLabels" :key="col" class="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 cursor-pointer transition-colors">
                  <input type="checkbox" v-model="visibleColumns[col]" class="w-3 h-3 rounded text-intimar-gold focus:ring-intimar-gold border-gray-300">
                  <span class="text-[10px] font-bold text-gray-700 uppercase tracking-wider">{{ val }}</span>
                </label>
              </div>
            </div>

            <div class="relative" v-click-outside="() => showSortToggle = false">
              <button @click="showSortToggle = !showSortToggle; showColumnToggle = false" class="bg-white hover:bg-gray-50 text-gray-500 font-black uppercase tracking-widest text-[9px] py-3 md:py-4 px-4 rounded-xl border border-gray-100 transition-all flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m3 16 4 4 4-4"/><path d="M7 20V4"/><path d="m21 8-4-4-4 4"/><path d="M17 4v16"/></svg>
                ORDEN
              </button>
              <div v-if="showSortToggle" class="absolute top-full right-0 mt-2 w-56 bg-white rounded-xl shadow-2xl border border-gray-100 py-2 z-[100] animate-in fade-in zoom-in-95 duration-200">
                <p class="px-4 py-1 text-[8px] font-black text-gray-400 uppercase tracking-widest mb-1">Ordenar por:</p>
                <button v-for="(label, value) in sortOptions" :key="value" @click="currentSort = value; showSortToggle = false; fetchReservas()" class="w-full text-left px-4 py-2.5 hover:bg-gray-50 transition-colors flex items-center justify-between" :class="currentSort === value ? 'bg-intimar-primary/5 text-intimar-primary' : 'text-gray-600'">
                  <span class="text-[10px] font-bold uppercase tracking-wider">{{ label }}</span>
                  <svg v-if="currentSort === value" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" class="text-intimar-primary"><polyline points="20 6 9 17 4 12"/></svg>
                </button>
              </div>
            </div>

            <router-link to="/reservas/nueva" class="flex-1 md:flex-none justify-center bg-intimar-primary hover:bg-intimar-dark text-white font-black uppercase tracking-widest text-[9px] md:text-[11px] py-3 md:py-4 px-6 md:px-8 rounded-xl md:rounded-2xl shadow-xl shadow-intimar-primary/20 transition-all flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
              NUEVA RESERVA
            </router-link>
          </div>
        </div>


        <!-- Filtros Component -->
        <ReservasFilter :totalReservas="stats.reservas" :totalPersonas="stats.personas" @filter="applyFilters" class="animate-in fade-in duration-500 delay-100" />

        <!-- Tabla Component -->
        <div class="bg-white rounded-[1.5rem] md:rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500 delay-150">
          <ReservasTable :reservas="filteredReservas" :loading="loading" :columns="visibleColumns" :currentSort="currentSort" @sort="handleSort" @refresh="fetchReservas" @asignar="openAsignarModal" @delete="handleDelete" />
        </div>

        <!-- Paginación -->
        <div v-if="!loading && filteredReservas && filteredReservas.length > 0" class="flex flex-col md:flex-row justify-between items-center gap-4 bg-white p-4 md:p-6 rounded-2xl shadow-sm border border-gray-100 animate-in fade-in slide-in-from-bottom-4 duration-500 delay-200">
          <p class="text-[9px] md:text-[10px] font-bold text-gray-400 uppercase tracking-widest">
            Mostrando {{ filteredReservas.length }} de {{ stats.reservas }} registros
          </p>
          <div class="flex items-center gap-4">
            <button :disabled="currentPage === 1" @click="currentPage--" class="p-2 text-gray-400 hover:text-intimar-primary disabled:opacity-30 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
            </button>
            <span class="text-[10px] font-black uppercase tracking-widest text-gray-700">PÁGINA {{ currentPage }}</span>
            <button :disabled="!filteredReservas || filteredReservas.length < pageSize" @click="currentPage++" class="p-2 text-gray-400 hover:text-intimar-primary disabled:opacity-30 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
            </button>
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
              <!-- Aviso Notas Especiales -->
              <div v-if="hasSpecialNotes" class="mb-4 bg-red-50 border-2 border-red-100 rounded-2xl p-4 animate-pulse">
                <div class="flex items-center gap-2 text-red-600 mb-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
                  <span class="text-[10px] font-black uppercase tracking-widest">¡Notas Especiales Detectadas!</span>
                </div>
                <div class="space-y-1">
                  <p v-if="reservaToAssign.alergias" class="text-[10px] text-gray-700 font-bold"><span class="text-red-500">ALERGIAS:</span> {{ reservaToAssign.alergias }}</p>
                  <p v-if="reservaToAssign.necesidades" class="text-[10px] text-gray-700 font-bold"><span class="text-amber-600">NECESIDADES:</span> {{ reservaToAssign.necesidades }}</p>
                  <p v-if="reservaToAssign.requerimientos" class="text-[10px] text-gray-700 font-bold"><span class="text-blue-600">REQUERIMIENTOS:</span> {{ reservaToAssign.requerimientos }}</p>
                  <div v-if="reservaToAssign.total_pagado > 0" class="mt-2 pt-2 border-t border-red-100 flex justify-between items-center">
                    <span class="text-[10px] font-black text-green-600 uppercase tracking-widest">Anticipo Pagado:</span>
                    <span class="text-sm font-black text-green-700 italic">{{ reservaToAssign.total_pagado_txt }}</span>
                  </div>
                </div>
              </div>

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

    <!-- SIMULACIÓN DE AFORO (DRAWER) -->
    <Teleport to="body">
      <transition name="drawer-slide">
        <div v-if="showAforoRadar" class="fixed inset-0 z-[1000] flex justify-end">
          <div class="absolute inset-0 bg-[#002e2c]/40 backdrop-blur-sm" @click="showAforoRadar = false"></div>
          
          <div class="relative w-full max-w-md bg-white h-full shadow-2xl flex flex-col animate-drawerIn overflow-hidden border-l border-intimar-gold/20">
            <!-- Header Simulación Ultra Compact -->
            <div class="p-5 bg-gradient-to-r from-[#00938f] to-[#007b77] text-white relative">
               <div class="relative z-10 flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-white/20 backdrop-blur-md rounded-xl flex items-center justify-center border border-white/30 shadow-lg">
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2v10l4 4"/></svg>
                    </div>
                    <div>
                      <h3 class="text-xl font-black italic tracking-tighter uppercase leading-none">Simulación Aforo</h3>
                      <p class="text-[9px] font-bold text-white/70 uppercase tracking-widest">Intimar Simulación</p>
                    </div>
                  </div>
                  <button @click="showAforoRadar = false" class="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center hover:bg-white/20 transition-all text-white/80 border border-white/20">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  </button>
               </div>
            </div>

            <div class="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide">
              <!-- Selector y Simulador en una sola Card Compacta -->
              <div class="bg-gray-50/50 border border-gray-100 rounded-3xl p-4 space-y-4">
                <div class="flex items-center gap-3">
                  <div class="flex-1">
                    <label class="text-[8px] font-black uppercase tracking-widest text-gray-400 mb-1 block ml-1">Fecha</label>
                    <input v-model="radarDate" type="date" @change="fetchRadarData" class="w-full bg-white border border-gray-100 rounded-xl px-3 py-2 font-black text-sm outline-none text-[#00938f] focus:ring-2 focus:ring-[#00938f]/10 transition-all">
                  </div>
                  <div class="w-24">
                    <label class="text-[8px] font-black uppercase tracking-widest text-gray-400 mb-1 block ml-1">Personas</label>
                    <input v-model="simulator.pax" type="number" class="w-full bg-white border border-gray-100 rounded-xl px-3 py-2 font-black text-sm outline-none focus:ring-2 focus:ring-[#00938f]/10 transition-all text-center">
                  </div>
                  <div class="w-28">
                    <label class="text-[8px] font-black uppercase tracking-widest text-gray-400 mb-1 block ml-1">Horario</label>
                    <select v-model="simulator.hora" class="w-full bg-white border border-gray-100 rounded-xl px-3 py-2 font-black text-sm outline-none focus:ring-2 focus:ring-[#00938f]/10 transition-all appearance-none text-center">
                      <option v-for="h in ['11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00']" :key="h" :value="h">{{ h }}</option>
                    </select>
                  </div>
                </div>

                <!-- Resultado Simulación Mini -->
                <transition name="fade">
                  <div v-if="simulationResult" class="p-3 rounded-2xl flex items-center gap-3 border transition-all" :class="simulationResult.status === 'ok' ? 'bg-[#00938f]/5 border-[#00938f]/20' : 'bg-red-50 border-red-200'">
                    <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" :class="simulationResult.status === 'ok' ? 'bg-[#00938f] text-white' : 'bg-red-500 text-white'">
                      <svg v-if="simulationResult.status === 'ok'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                    </div>
                    <div class="flex-1">
                      <h5 class="text-[10px] font-black uppercase tracking-widest leading-none mb-0.5" :class="simulationResult.status === 'ok' ? 'text-[#00938f]' : 'text-red-700'">{{ simulationResult.status === 'ok' ? 'Disponible' : 'Completo' }}</h5>
                      <p class="text-[9px] font-bold text-gray-500 leading-tight">{{ simulationResult.detail }}</p>
                    </div>
                  </div>
                </transition>
              </div>

              <!-- Cronograma Ultra Compacto -->
              <div class="space-y-2">
                <div class="flex items-center justify-between px-2 mb-1">
                  <h4 class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Proyección por Horarios</h4>
                  <span class="text-[9px] font-black text-[#00938f] uppercase">{{ radarData?.length || 0 }} Slots</span>
                </div>

                <div v-if="radarLoading" class="space-y-2 px-2">
                  <div v-for="i in 6" :key="i" class="h-12 bg-gray-50 animate-pulse rounded-xl"></div>
                </div>

                <div v-else class="space-y-1">
                  <div 
                    v-for="slot in simulatedRadarData" 
                    :key="slot.hora" 
                    :id="'radar-slot-' + slot.hora"
                    class="group bg-white border border-gray-50 hover:border-[#00938f]/30 p-2.5 rounded-2xl transition-all cursor-pointer overflow-hidden relative" 
                    @click="toggleSlot(slot.hora)" 
                    :class="{
                      'ring-2 ring-[#00938f]/10 bg-gray-50/50': expandedSlot === slot.hora,
                      'ring-2 ring-[#00938f] bg-[#00938f]/5 shadow-lg z-10 scale-[1.01] border-transparent': simulator.hora === slot.hora
                    }"
                  >
                    <!-- Badge de Hora Simulada -->
                    <div v-if="simulator.hora === slot.hora" class="absolute top-0 right-0 bg-[#00938f] text-white text-[7px] font-black px-2 py-0.5 rounded-bl-lg uppercase tracking-widest animate-pulse">
                      Simulando
                    </div>
                    <div class="flex items-center gap-4">
                      <!-- Hora -->
                      <div class="w-10 text-center">
                        <span class="text-xs font-black text-gray-900 italic tracking-tighter">{{ slot.hora }}</span>
                      </div>
                      
                      <!-- Info y Barra -->
                      <div class="flex-1 space-y-1.5">
                        <div class="flex items-center justify-between">
                          <div class="flex items-center gap-3">
                            <!-- Sillas -->
                            <div class="flex items-center gap-1">
                              <span class="text-[9px] font-black text-gray-700">{{ slot.simOcupado }} / {{ slot.limite }}</span>
                              <span class="text-[7px] font-bold text-gray-400 uppercase tracking-tighter">Sillas</span>
                            </div>
                            <!-- Cocina -->
                            <div class="flex items-center gap-1 border-l border-gray-100 pl-3">
                              <span class="text-[9px] font-black" :class="slot.simPorcentajeCocina > 90 ? 'text-orange-600' : 'text-orange-500'">{{ slot.simLlegando }} / {{ slot.limite_cocina }}</span>
                              <span class="text-[7px] font-bold text-gray-400 uppercase tracking-tighter">Cocina</span>
                            </div>
                          </div>
                          
                          <!-- Indicador de click -->
                          <div class="text-[7px] font-bold text-gray-300 uppercase tracking-widest flex items-center gap-1">
                             {{ expandedSlot === slot.hora ? 'Cerrar' : 'Detalles' }}
                             <svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="transition-transform" :class="{'rotate-180': expandedSlot === slot.hora}"><path d="m6 9 6 6 6-6"/></svg>
                          </div>
                        </div>
                            <!-- Barras Apiladas -->
                        <div class="flex gap-1 h-1.5">
                           <!-- Barra Sillas -->
                           <div class="h-full flex-1 bg-gray-100 rounded-full overflow-hidden">
                             <div class="h-full transition-all duration-700" 
                                  :style="`width: ${Math.min(slot.simPorcentaje, 100)}%`" 
                                  :class="slot.simPorcentaje > 100 ? 'bg-red-600' : slot.simPorcentaje > 85 ? 'bg-red-500' : 'bg-intimar-primary'">
                             </div>
                           </div>
                           <!-- Barra Cocina -->
                           <div class="h-full w-1/3 bg-gray-100 rounded-full overflow-hidden">
                             <div class="h-full transition-all duration-700" 
                                  :style="`width: ${Math.min(slot.simPorcentajeCocina, 100)}%`" 
                                  :class="slot.simPorcentajeCocina > 100 ? 'bg-red-600' : slot.simPorcentajeCocina > 90 ? 'bg-orange-600' : 'bg-orange-400'">
                             </div>
                           </div>
                        </div>
                      </div>
                    </div>
 
                    <!-- DESPLIEGUE DE DETALLES -->
                    <transition name="fade">
                      <div v-if="expandedSlot === slot.hora" class="mt-3 pt-3 border-t border-gray-100 space-y-2">
                        <div v-if="slot.detalles.length === 0" class="text-center py-4">
                          <p class="text-[10px] font-bold text-gray-400 italic">No hay reservas activas en este horario.</p>
                        </div>
                        <div v-else v-for="d in slot.detalles" :key="d.reserva" class="bg-white p-2 rounded-xl border border-gray-50 flex items-center justify-between group/item hover:border-[#00938f]/20 transition-all">
                          <div class="flex items-center gap-3">
                            <div class="w-7 h-7 bg-[#00938f]/10 text-[#00938f] rounded-lg flex items-center justify-center font-black text-[9px]">
                              {{ d.pax }}
                            </div>
                            <div>
                              <p class="text-[10px] font-black text-gray-800 leading-tight">{{ d.nombre }}</p>
                              <div class="flex items-center gap-2 mt-0.5">
                                <span class="text-[8px] font-bold text-gray-400 flex items-center gap-1">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                                  {{ d.hora }} → {{ d.hora_fin }}
                                </span>
                              </div>
                            </div>
                          </div>
                          <div class="text-right">
                             <span class="px-2 py-0.5 rounded-full text-[7px] font-black uppercase tracking-widest border" 
                                   :class="{
                                     'bg-emerald-50 text-emerald-600 border-emerald-100': d.estado === 'En proceso',
                                     'bg-blue-50 text-blue-600 border-blue-100': d.estado === 'Confirmada',
                                     'bg-gray-50 text-gray-500 border-gray-100': d.estado === 'Solicitud de reserva'
                                   }">
                               {{ d.estado }}
                             </span>
                          </div>
                        </div>
                      </div>
                    </transition>
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer Drawer Compact -->
            <div class="p-4 border-t border-gray-50 bg-gray-50/30 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="w-1 h-1 bg-emerald-500 rounded-full animate-pulse"></div>
                <p class="text-[8px] font-bold text-gray-400 uppercase tracking-widest">En Vivo</p>
              </div>
              <button @click="showAforoRadar = false" class="px-6 py-2.5 bg-[#00938f] text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-[#007b77] transition-all shadow-md shadow-[#00938f]/10">Cerrar</button>
            </div>
          </div>
        </div>
      </transition>
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
import { ref, onMounted, computed, reactive, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import ReservasFilter from '@/components/Reservas/ReservasFilter.vue'
import ReservasTable from '@/components/Reservas/ReservasTable.vue'
import { call, Button } from 'frappe-ui'
import { session } from '@/data/session'
import { generateReservasPDF } from '@/utils/pdfExport.js'

const router = useRouter()

const expandedSlot = ref(null)
const toggleSlot = (hora) => {
  if (expandedSlot.value === hora) expandedSlot.value = null
  else expandedSlot.value = hora
}

const exportToPDF = async () => {
  if (!window.jspdf) {
    showToast('Error', 'La librería de PDF aún se está cargando. Reintenta en un segundo.', 'error')
    return
  }
  
  // Mostrar feedback al usuario mientras carga
  showToast('Generando Reporte', 'Obteniendo todas las reservas que coinciden con los filtros...', 'info')
  
  let allReservas = []
  try {
    const response = await call('intimar_erp.api.get_reservas_list', {
      filters: JSON.stringify(buildFilters()),
      limit_start: 0,
      limit_page_length: 5000,
      order_by: currentSort.value
    })
    allReservas = response?.data || response || []
  } catch (err) {
    console.error('Error al obtener listado completo para PDF:', err)
    showToast('Error', 'No se pudieron descargar todas las reservas filtradas.', 'error')
    return
  }

  if (allReservas.length === 0) {
    showToast('Reporte Vacío', 'No hay ninguna reserva con los filtros activos.', 'info')
    return
  }

  try {
    generateReservasPDF(allReservas, activeFilters.value, visibleColumns)
    showToast('¡PDF Generado!', 'El reporte se ha descargado correctamente.', 'success')
  } catch (err) {
    console.error('Error al generar PDF:', err)
  }
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
const defaultOrder = 'fecha_reserva asc, hora_reserva asc'

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
    if (activeFilters.value.hora && activeFilters.value.hora !== 'Todas') {
        const h = activeFilters.value.hora
        f.push(['hora_reserva', '>=', `${h}:00:00`])
        f.push(['hora_reserva', '<=', `${h}:59:59`])
    }
    
    if (activeFilters.value.estado && activeFilters.value.estado.length > 0) {
        if (activeFilters.value.estado.length === 1) {
            f.push(['estado_reserva', '=', activeFilters.value.estado[0]])
        } else {
            f.push(['estado_reserva', 'in', activeFilters.value.estado])
        }
    }

    if (activeFilters.value.anticipo && activeFilters.value.anticipo !== 'Todos') {
        if (activeFilters.value.anticipo === 'Pagado') {
            f.push(['total_pagado', '>', 0])
        } else {
            // Considerar tanto 0 como null/None para Sin Anticipo
            f.push(['total_pagado', '<=', 0])
        }
    }

    if (activeFilters.value.llegada && activeFilters.value.llegada !== 'Todos') {
        if (activeFilters.value.llegada === 'Si') {
            f.push(['hora_llegada', 'is', 'set'])
        } else if (activeFilters.value.llegada === 'No') {
            f.push(['hora_llegada', 'is', 'not set'])
        } else {
            const h = activeFilters.value.llegada
            f.push(['hora_llegada', '>=', `${h}:00:00`])
            f.push(['hora_llegada', '<=', `${h}:59:59`])
        }
    }

    if (activeFilters.value.salida && activeFilters.value.salida !== 'Todos') {
        if (activeFilters.value.salida === 'Si') {
            f.push(['hora_salida', 'is', 'set'])
        } else if (activeFilters.value.salida === 'No') {
            f.push(['hora_salida', 'is', 'not set'])
        } else {
            const h = activeFilters.value.salida
            f.push(['hora_salida', '>=', `${h}:00:00`])
            f.push(['hora_salida', '<=', `${h}:59:59`])
        }
    }

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
    const response = await call('intimar_erp.api.get_reservas_list', {
      filters: JSON.stringify(buildFilters()),
      limit_start: (currentPage.value - 1) * pageSize.value,
      limit_page_length: pageSize.value,
      order_by: currentSort.value
    })
    // Aseguramos que tomamos la lista de datos, sea que venga envuelta o directa
    reservas.value = response?.data || response || []
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
    let [summary, rStats] = await Promise.all([
      call('intimar_erp.api.get_reservas_summary', {
        filters: buildFilters()
      }),
      call('intimar_erp.api.get_dashboard_stats', {
        start_date: activeFilters.value.fecha || null
      })
    ])
    
    // Extraer datos si vienen envueltos en .data
    if (summary?.data) summary = summary.data
    if (rStats?.data) rStats = rStats.data
    
    stats.value = {
      reservas: summary?.reservas || 0,
      personas: summary?.personas || 0
    }
    realtimeStats.value = rStats
    // Sincronizar fecha del radar si está vacío
    if (!radarDate.value) radarDate.value = activeFilters.value.fecha || frappe.utils.today()
  } catch (error) {
    console.error('Error calculando estadísticas:', error)
  } finally {
    statsLoading.value = false
  }
}

// LÓGICA RADAR DE AFORO
const showAforoRadar = ref(false)
const radarLoading = ref(false)
const radarData = ref([])
const radarDate = ref('')
const simulator = reactive({ pax: null, hora: '13:00' })
const simulationResult = ref(null)
const configuracionIntimar = ref(null)

const fetchConfiguracionIntimar = async () => {
  try {
    const doc = await call('frappe.client.get', {
      doctype: 'Configuracion Intimar',
      name: 'Configuracion Intimar'
    })
    configuracionIntimar.value = doc
  } catch (e) {
    console.error('Error al obtener Configuración Intimar:', e)
  }
}

const intervaloFlujo = computed(() => {
  return configuracionIntimar.value?.intervalo_flujo_cocina || 30
})

const getRoundedSlot = (horaStr) => {
  if (!horaStr) return ''
  const [h, m] = horaStr.split(':').map(Number)
  const interval = intervaloFlujo.value
  const totalMins = h * 60 + m
  const roundedMins = Math.floor(totalMins / interval) * interval
  const roundedH = Math.floor(roundedMins / 60)
  const roundedM = roundedMins % 60
  return `${String(roundedH).padStart(2, '0')}:${String(roundedM).padStart(2, '0')}`
}

const round = (value, decimals) => {
  return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals)
}

const simulatedRadarData = computed(() => {
  if (!radarData.value) return []
  
  const pax = parseInt(simulator.pax) || 0
  const simHora = simulator.hora
  
  if (pax <= 0 || !simHora) {
    return radarData.value.map(slot => ({
      ...slot,
      simOcupado: slot.ocupado,
      simLlegando: slot.llegando,
      simPorcentaje: slot.porcentaje,
      simPorcentajeCocina: slot.porcentaje_cocina
    }))
  }
  
  const slotsDuration = pax > 8 ? 5 : 4
  const startIndex = radarData.value.findIndex(s => s.hora === simHora)
  const roundedSimHora = getRoundedSlot(simHora)
  
  return radarData.value.map((slot, index) => {
    let newOcupado = slot.ocupado
    let newLlegando = slot.llegando
    
    if (startIndex !== -1 && index >= startIndex && index < startIndex + slotsDuration) {
      newOcupado += pax
    }
    
    const roundedSlotHora = getRoundedSlot(slot.hora)
    if (roundedSlotHora === roundedSimHora && slot.hora === roundedSimHora) {
      newLlegando += pax
    }
    
    const pct = round((newOcupado / slot.limite * 100), 1)
    const pctCocina = round((newLlegando / slot.limite_cocina * 100), 1)
    
    return {
      ...slot,
      simOcupado: newOcupado,
      simLlegando: newLlegando,
      simPorcentaje: pct,
      simPorcentajeCocina: pctCocina
    }
  })
})

// Configuración de Columnas Visibles
const showColumnToggle = ref(false)
const showSortToggle = ref(false)

const sortOptions = {
  'fecha_reserva asc, hora_reserva asc': 'Reserva (Menor a Mayor)',
  'hora_reserva desc': 'Reserva (Mayor a Menor)',
  'hora_llegada asc': 'Llegada (Más antiguo)',
  'hora_salida desc': 'Salida (Más recientes)',
  'creation desc': 'Creación (Más recientes)',
  'creation asc': 'Creación (Más antiguos)'
}
const currentSort = ref('fecha_reserva asc, hora_reserva asc')

const handleSort = (newSort) => {
  currentSort.value = newSort
  fetchReservas()
}

const visibleColumns = reactive({
  cliente: true,
  celular: true,
  detalles: true,
  pago: true,
  estado: true,
  motivo: true,
  mesas: false,
  llegada: false,
  salida: false,
  creacion: false
})

const columnLabels = {
  cliente: 'Cliente',
  celular: 'Celular',
  detalles: 'Detalles',
  pago: 'Anticipo',
  estado: 'Estado',
  motivo: 'Motivo',
  mesas: 'Asignación',
  llegada: 'Hora Llegada',
  salida: 'Hora Salida',
  creacion: 'Fecha Creación'
}

// Directiva para cerrar al clickear fuera
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  },
}

// Watcher para simular en tiempo real con precisión total
watch(() => [simulator.pax, simulator.hora, radarDate.value], async ([pax, hora, fecha]) => {
  if (!pax || !hora || !fecha) {
    simulationResult.value = null
    return
  }
  
  if (!radarData.value || !radarData.value.length) {
    await fetchRadarData()
  }
  
  const roundedHora = getRoundedSlot(hora)
  const targetSlot = radarData.value.find(s => s.hora === roundedHora)
  if (!targetSlot) {
    simulationResult.value = null
    return
  }
  
  const numPax = parseInt(pax) || 0
  const startIndex = radarData.value.findIndex(s => s.hora === hora)
  const slotsDuration = numPax > 8 ? 5 : 4
  
  let peakSalonOcupado = 0
  if (startIndex !== -1) {
    for (let i = startIndex; i < startIndex + slotsDuration && i < radarData.value.length; i++) {
      const slot = radarData.value[i]
      if (slot.ocupado > peakSalonOcupado) {
        peakSalonOcupado = slot.ocupado
      }
    }
  }
  
  const nuevoTotalSalon = peakSalonOcupado + numPax
  const nuevoTotalCocina = targetSlot.llegando + numPax
  
  const salonExceeded = nuevoTotalSalon > targetSlot.limite
  const cocinaExceeded = nuevoTotalCocina > targetSlot.limite_cocina
  
  if (salonExceeded && cocinaExceeded) {
    simulationResult.value = {
      status: 'error',
      message: 'Límites de Salón y Cocina Excedidos',
      detail: `Se excederían ambos límites. Salón alcanzará un pico de ${nuevoTotalSalon}/${targetSlot.limite} sillas. Cocina recibirá ${nuevoTotalCocina}/${targetSlot.limite_cocina} personas.`
    }
  } else if (salonExceeded) {
    simulationResult.value = {
      status: 'error',
      message: 'Aforo de Salón Excedido',
      detail: `El salón alcanzaría un pico de ${nuevoTotalSalon} personas en el rango simulado (Límite: ${targetSlot.limite} sillas).`
    }
  } else if (cocinaExceeded) {
    simulationResult.value = {
      status: 'error',
      message: 'Capacidad de Cocina Excedida',
      detail: `La cocina recibiría un flujo de ${nuevoTotalCocina} personas en este bloque de ${intervaloFlujo.value} min (Límite: ${targetSlot.limite_cocina} personas).`
    }
  } else {
    simulationResult.value = {
      status: 'ok',
      message: 'Simulación Exitosa',
      detail: `El salón alcanzará un pico de ${nuevoTotalSalon}/${targetSlot.limite} sillas y la cocina recibirá un flujo de ${nuevoTotalCocina}/${targetSlot.limite_cocina} personas. ¡Espacio disponible!`
    }
  }
}, { deep: true })

// Watcher para scroll automático al cambiar horario de simulación
watch(() => simulator.hora, (newHora) => {
  if (newHora) {
    nextTick(() => {
      const el = document.getElementById(`radar-slot-${newHora}`)
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    })
  }
})

const openAforoRadar = () => {
  try {
    // Sincronizar con el filtro actual si existe, sino con hoy
    const filterDate = activeFilters.value?.fecha
    radarDate.value = filterDate || frappe.utils.today()
    
    showAforoRadar.value = true
    
    if (!filterDate) {
      showToast('Simulación Aforo', 'Mostrando proyección para el día de hoy.', 'info')
    } else {
      showToast('Simulación Aforo', `Proyectando disponibilidad para el ${filterDate}`, 'success')
    }
    
    fetchRadarData()
  } catch (err) {
    console.error('Error al abrir simulación:', err)
    showToast('Error', 'No se pudo abrir la simulación. Reintenta en un momento.', 'error')
  }
}

const fetchRadarData = async () => {
  radarLoading.value = true
  try {
    await fetchConfiguracionIntimar()
    const data = await call('intimar_erp.api.get_ocupacion_proyectada', {
      fecha: radarDate.value
    })
    radarData.value = data
    
    // Auto-scroll a la hora simulada si existe
    if (simulator.hora) {
      nextTick(() => {
        const el = document.getElementById(`radar-slot-${simulator.hora}`)
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      })
    }
  } catch (err) {
    console.error('Error radar:', err)
  } finally {
    radarLoading.value = false
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

const hasSpecialNotes = computed(() => {
  if (!reservaToAssign.value) return false
  return !!(reservaToAssign.value.alergias || reservaToAssign.value.necesidades || reservaToAssign.value.requerimientos || (reservaToAssign.value.total_pagado > 0))
})

const fetchMesasYMozos = async () => {
  try {
    const [m, mz] = await Promise.all([
      call('intimar_erp.api.get_mesas_libres'),
      call('intimar_erp.api.get_mozos')
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
      router.push('/mapa')
    }, 1500)
  } catch (error) {
    console.error('Error al asignar mesa:', error)
    const msg = error.messages ? error.messages.join('\n') : (error.message || 'Hubo un problema al asignar la mesa.')
    showToast('Error', msg, 'error')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchReservas()
  fetchStats()
  fetchConfiguracionIntimar()
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
