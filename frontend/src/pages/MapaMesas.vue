<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />

    <div class="flex-1 p-6 md:p-12 pb-32 md:pb-12 overflow-y-auto overflow-x-hidden">
      <div class="w-full">

        <!-- Header -->
        <div class="flex flex-col md:flex-row items-center md:items-center justify-between mb-4 md:mb-10 gap-4 md:gap-6">
          <div class="flex flex-col md:flex-row items-center gap-3 text-center md:text-left">
            <img :src="'/files/intimar-logo.png'" alt="Intimar Logo" class="h-8 md:h-12 w-auto" />
            <div>
              <h1 class="text-2xl md:text-4xl font-black text-gray-900 tracking-tight italic leading-tight">Gestión de Mesas</h1>
              <p class="text-gray-500 font-medium uppercase tracking-widest text-[8px] md:text-[10px] mt-0.5">Bay · Paracas · Real-Time</p>
            </div>
          </div>


          <div class="grid grid-cols-2 md:flex md:flex-wrap items-center gap-1.5 md:gap-3 bg-white p-1 md:p-2 rounded-2xl md:rounded-2xl shadow-sm border border-gray-100 w-full md:w-auto">
            <!-- Mesas -->
            <div class="px-2 py-1.5 md:py-3 bg-intimar-green/10 text-intimar-green rounded-xl text-[10px] md:text-xs font-black uppercase tracking-tight flex flex-col items-center justify-center min-w-0">
              <span class="text-[7px] md:text-[8px] opacity-70 whitespace-nowrap">Libres</span>
              <span class="text-xs md:text-sm font-black">{{ libres }}</span>
            </div>
            <div class="px-2 py-1.5 md:py-3 bg-intimar-red/10 text-intimar-red rounded-xl text-[10px] md:text-xs font-black uppercase tracking-tight flex flex-col items-center justify-center min-w-0">
              <span class="text-[7px] md:text-[8px] opacity-70 whitespace-nowrap">Ocupadas</span>
              <span class="text-xs md:text-sm font-black">{{ ocupadas }}</span>
            </div>
            
            <div class="w-px h-6 md:h-8 bg-gray-200 mx-1 hidden md:block"></div>
 
            <!-- Personas -->
            <div class="px-2 py-1.5 md:py-3 bg-intimar-primary/10 text-intimar-primary rounded-xl text-[10px] md:text-xs font-black uppercase tracking-tight flex flex-col items-center justify-center min-w-0">
              <span class="text-[7px] md:text-[8px] opacity-70 whitespace-nowrap">En Sala</span>
              <span class="text-xs md:text-sm font-black">{{ personasEnRestaurante }}</span>
            </div>
            <div class="px-2 py-1.5 md:py-3 bg-intimar-gold/10 text-intimar-gold rounded-xl text-[10px] md:text-xs font-black uppercase tracking-tight flex flex-col items-center justify-center min-w-0">
              <span class="text-[7px] md:text-[8px] opacity-70 whitespace-nowrap">Llegando</span>
              <span class="text-xs md:text-sm font-black">{{ personasPorLlegar }}</span>
            </div>
            
            <div class="w-px h-6 md:h-8 bg-gray-200 mx-1 hidden md:block"></div>
            
            <div class="col-span-2 md:col-span-1 flex justify-center border-t md:border-t-0 pt-1 md:pt-0 border-gray-50">
              <Button icon="refresh-cw" variant="ghost" class="text-gray-400 hover:text-gray-900 w-full md:w-auto h-8 md:h-auto" @click="mesas.fetch(); reservasPendientes.fetch()" />
            </div>
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
                <!-- Checkbox de Selección Directa (Solo si está libre) -->
                <div 
                  v-if="mesa.estado_mesa"
                  @click.stop="toggleMesaSelection(mesa)"
                  class="absolute top-5 left-5 z-20 cursor-pointer group/check"
                >
                  <div 
                    :class="[
                      'w-7 h-7 rounded-lg border-2 transition-all flex items-center justify-center shadow-sm', 
                      isMesaSelectedForMulti(mesa) 
                        ? 'bg-intimar-gold border-intimar-gold scale-110 shadow-intimar-gold/40' 
                        : 'bg-white/80 border-gray-200 hover:border-intimar-gold hover:bg-white'
                    ]"
                  >
                    <svg v-if="isMesaSelectedForMulti(mesa)" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                    <div v-else class="w-2 h-2 rounded-full bg-gray-200 group-hover/check:bg-intimar-gold/30 transition-colors"></div>
                  </div>
                </div>

                <div 
                  @click="handleMesaClick(mesa)"
                  :class="[
                    'min-h-[220px] p-6 flex flex-col items-center justify-center rounded-[2.5rem] border-b-8 transition-all duration-300 shadow-lg hover:shadow-2xl cursor-pointer transform hover:-translate-y-2',
                    mesa.estado_mesa 
                        ? (isMesaSelectedForMulti(mesa) ? 'bg-intimar-gold/5 border-intimar-gold text-intimar-gold' : 'bg-white border-intimar-green text-gray-900 shadow-intimar-green/10')
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
                      <span>{{ formatTime(mesa.reserva.hora_llegada) }}</span>
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

        <!-- Botón Flotante Confirmar Multiselección -->
        <div v-if="selectedMesasForMulti.length > 0" class="fixed bottom-10 left-1/2 -translate-x-1/2 z-[100] animate-in slide-in-from-bottom-10 flex flex-col items-center gap-4">
            <div class="bg-gray-900 text-white px-6 py-3 rounded-full text-[10px] font-black uppercase tracking-widest shadow-2xl flex items-center gap-3">
                <span class="w-2 h-2 bg-intimar-gold rounded-full animate-pulse"></span>
                {{ selectedMesasForMulti.length }} mesas seleccionadas
                <button @click="selectedMesasForMulti = []" class="ml-2 text-white/50 hover:text-white transition-colors">Limpiar</button>
            </div>
            <button 
                v-if="session.isAdmin || session.hasRole('Anfitriona')"
                @click="openMultiAssignModal"
                class="bg-intimar-primary text-white px-10 py-5 rounded-[2.5rem] font-black uppercase tracking-[0.2em] shadow-[0_20px_50px_rgba(0,147,143,0.3)] hover:scale-105 active:scale-95 transition-all flex items-center gap-4 border-4 border-white"
            >
                Asignar a Reserva
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
            </button>
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
                            <h3 v-if="selectedMesasForMulti.length <= 1" class="text-xl font-black text-gray-900 leading-tight italic tracking-tighter text-center">
                                Mesa <span class="text-intimar-primary">{{ selectedMesa?.numero_mesa || selectedMesasForMulti[0]?.numero_mesa }}</span>
                            </h3>
                            <h3 v-else class="text-xl font-black text-gray-900 leading-tight italic tracking-tighter text-center">
                                Asignar <span class="text-intimar-gold">{{ selectedMesasForMulti.length }} Mesas</span>
                            </h3>
                            <p class="text-gray-400 text-[8px] font-bold uppercase tracking-[0.2em] text-center mt-0.5">Seleccionar Reserva</p>
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

                        <!-- Botón Reserva Rápida (NUEVO) -->
                        <button 
                            v-if="session.isAdmin || session.hasRole('Anfitriona')"
                            @click="assignStep = 1.3; resetQuickForm()"
                            class="w-full py-4 border-2 border-dashed border-intimar-primary/30 text-intimar-primary rounded-[1.2rem] font-black uppercase text-[10px] tracking-[0.2em] hover:bg-intimar-primary hover:text-white hover:border-intimar-primary transition-all flex items-center justify-center gap-2"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
                            Nueva Reserva Rápida
                        </button>

                        <div v-if="reservasPendientes.loading" class="py-8 flex justify-center"><LoadingIndicator class="w-8 h-8 text-intimar-primary" /></div>
                        <div v-else-if="!filteredReservas.length" class="py-12 text-center bg-gray-50 rounded-[2rem] border-2 border-dashed border-gray-200">
                            <p class="text-gray-400 font-bold italic text-sm">No hay reservas</p>
                        </div>
                        <div v-else class="max-h-[300px] overflow-y-auto pr-1 space-y-2 custom-scrollbar">
                            <div 
                                v-for="res in filteredReservas" 
                                :key="res.name"
                                @click="selectReservaForAssign(res)"
                                class="p-3.5 bg-white border-2 border-gray-50 rounded-2xl hover:border-intimar-primary hover:shadow-lg transition-all flex justify-between items-center group relative overflow-hidden"
                            >
                                <div class="flex-1">
                                    <div class="font-black text-sm text-gray-900 group-hover:text-intimar-primary transition-colors flex items-center gap-2">
                                        {{ res.cliente_nombre }}
                                        <span class="text-[8px] opacity-40 font-bold tracking-widest">{{ res.name.split('-').pop() }}</span>
                                    </div>
                                    <div class="flex items-center gap-2 mt-0.5">
                                        <span class="text-[8px] bg-gray-100 px-2 py-0.5 rounded-lg font-black text-gray-500 uppercase tracking-widest">{{ res.hora_reserva }}</span>
                                        <span class="text-[8px] bg-intimar-gold/10 px-2 py-0.5 rounded-lg font-black text-intimar-gold uppercase tracking-widest">{{ res.cant_adultos + res.cant_ninos }}P</span>
                                    </div>
                                </div>
                                <div class="w-8 h-8 rounded-lg bg-gray-50 flex items-center justify-center group-hover:bg-intimar-primary group-hover:text-white transition-all text-gray-300">
                                     <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- PASO 1.3: FORMULARIO RESERVA RÁPIDA (NUEVO) -->
                    <div v-if="assignStep === 1.3" class="space-y-6">
                        <div class="text-center">
                            <button @click="assignStep = 1" class="text-intimar-primary text-[8px] font-black uppercase tracking-[0.2em] mb-1 flex items-center justify-center gap-2 hover:translate-x-[-2px] transition-transform mx-auto">
                                 <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
                                 VOLVER
                            </button>
                            <h3 class="text-2xl font-black text-gray-900 leading-tight italic tracking-tighter uppercase">Reserva Rápida</h3>
                            <p class="text-gray-400 text-[10px] font-bold uppercase tracking-[0.2em] mt-0.5">Crear y ocupar mesa</p>
                        </div>

                        <div class="space-y-4">
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                <div class="space-y-1">
                                    <label class="text-[8px] font-black uppercase text-gray-400 tracking-widest ml-4">Nombre</label>
                                    <input v-model="quickReservaForm.nombre" type="text" class="w-full px-5 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none font-bold text-base md:text-sm">
                                </div>
                                <div class="space-y-1">
                                    <label class="text-[8px] font-black uppercase text-gray-400 tracking-widest ml-4">Apellido</label>
                                    <input v-model="quickReservaForm.apellido" type="text" class="w-full px-5 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none font-bold text-base md:text-sm">
                                </div>
                            </div>
                            <div class="space-y-1">
                                <label class="text-[8px] font-black uppercase text-gray-400 tracking-widest ml-4 flex justify-between">
                                    Celular
                                </label>
                                <vue-tel-input
                                    v-model="quickReservaForm.celular"
                                    v-bind="telInputOptions"
                                    @on-input="onPhoneInput"
                                    class="quick-tel-input"
                                ></vue-tel-input>
                            </div>
                            <div class="space-y-1">
                                <label class="text-[8px] font-black uppercase text-gray-400 tracking-widest ml-4">Correo (Opcional)</label>
                                <input v-model="quickReservaForm.email" type="email" class="w-full px-5 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none font-bold text-base md:text-sm">
                            </div>
                            
                            <div class="bg-gray-50 p-6 rounded-[2rem] border-2 border-gray-100 space-y-4">
                                <p class="text-center text-[10px] font-black uppercase tracking-widest text-gray-400">Cantidad de PERS.</p>
                                <div class="flex items-center justify-center gap-8">
                                    <div class="text-center space-y-2">
                                        <label class="text-[8px] font-black uppercase text-gray-500 tracking-widest block">Adultos</label>
                                        <div class="flex items-center gap-3">
                                            <button @click="quickReservaForm.adultos = Math.max(1, quickReservaForm.adultos - 1)" class="w-10 h-10 rounded-xl bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-500">-</button>
                                            <span class="text-3xl font-black italic text-gray-900 w-8 text-center">{{ quickReservaForm.adultos }}</span>
                                            <button @click="quickReservaForm.adultos++" class="w-10 h-10 rounded-xl bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-500">+</button>
                                        </div>
                                    </div>
                                    <div class="text-center space-y-2">
                                        <label class="text-[8px] font-black uppercase text-gray-500 tracking-widest block">Niños</label>
                                        <div class="flex items-center gap-3">
                                            <button @click="quickReservaForm.ninos = Math.max(0, quickReservaForm.ninos - 1)" class="w-10 h-10 rounded-xl bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-500">-</button>
                                            <span class="text-3xl font-black italic text-gray-900 w-8 text-center">{{ quickReservaForm.ninos }}</span>
                                            <button @click="quickReservaForm.ninos++" class="w-10 h-10 rounded-xl bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-500">+</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <button 
                            @click="confirmarReservaRapida" 
                            :disabled="!quickReservaForm.nombre || !quickReservaForm.celular || creatingQuickReserva"
                            class="w-full bg-intimar-gold text-white py-5 rounded-[1.8rem] font-black uppercase text-[11px] tracking-[0.2em] shadow-xl shadow-intimar-gold/20 transition-all flex items-center justify-center gap-3 border-4 border-white disabled:opacity-50"
                        >
                            <LoadingIndicator v-if="creatingQuickReserva" class="w-4 h-4 text-white" />
                            <span v-else>CREAR Y CONTINUAR</span>
                            <svg v-if="!creatingQuickReserva" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
                        </button>
                    </div>

                    <!-- PASO 1.2: RESUMEN DE CLIENTE Y PERS. (NUEVO) -->
                    <div v-if="assignStep === 1.2" class="space-y-6">
                        <div class="text-center">
                            <button @click="assignStep = 1" class="text-intimar-primary text-[8px] font-black uppercase tracking-[0.2em] mb-1 flex items-center justify-center gap-2 hover:translate-x-[-2px] transition-transform mx-auto">
                                 <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
                                 VOLVER
                            </button>
                            <h3 class="text-2xl font-black text-gray-900 leading-tight italic tracking-tighter uppercase">Resumen de Cliente</h3>
                            <p class="text-gray-400 text-[10px] font-bold uppercase tracking-[0.2em] mt-0.5">{{ selectedReservaForAssign?.cliente_nombre }}</p>
                        </div>

                        <!-- Info Especial (Solo si existe) -->
                        <div v-if="selectedReservaForAssign?.alergias || selectedReservaForAssign?.necesidades || selectedReservaForAssign?.requerimientos" class="bg-red-50 p-5 rounded-[1.5rem] border-2 border-red-100 space-y-3">
                            <div v-if="selectedReservaForAssign?.alergias">
                                <label class="text-[8px] font-black uppercase text-red-500 tracking-widest">Alergias</label>
                                <p class="text-xs font-black text-gray-900 leading-tight italic">"{{ selectedReservaForAssign.alergias }}"</p>
                            </div>
                            <div v-if="selectedReservaForAssign?.necesidades">
                                <label class="text-[8px] font-black uppercase text-amber-600 tracking-widest">Necesidades</label>
                                <p class="text-xs font-black text-gray-900 leading-tight italic">"{{ selectedReservaForAssign.necesidades }}"</p>
                            </div>
                            <div v-if="selectedReservaForAssign?.requerimientos">
                                <label class="text-[8px] font-black uppercase text-blue-600 tracking-widest">Requerimientos</label>
                                <p class="text-xs font-black text-gray-900 leading-tight italic">"{{ selectedReservaForAssign.requerimientos }}"</p>
                            </div>
                            
                            <!-- Monto de Anticipo (NUEVO en resumen) -->
                            <div v-if="selectedReservaForAssign?.total_pagado > 0" class="pt-2 border-t border-red-100 flex items-center justify-between">
                                <label class="text-[8px] font-black uppercase text-green-600 tracking-widest">Anticipo Pagado</label>
                                <span class="bg-green-100 text-green-700 px-2 py-0.5 rounded-lg text-[10px] font-black italic">
                                    {{ selectedReservaForAssign.total_pagado_txt }}
                                </span>
                            </div>
                        </div>

                        <!-- Edición de PERS. -->
                        <div class="bg-gray-50 p-6 rounded-[2rem] border-2 border-gray-100 space-y-4">
                            <p class="text-center text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">Cantidad de PERS.</p>
                            <div class="flex items-center justify-center gap-8">
                                <div class="text-center space-y-2">
                                    <label class="text-[8px] font-black uppercase text-gray-500 tracking-widest block">Adultos</label>
                                    <div class="flex items-center gap-3">
                                        <button @click="paxAdultos = Math.max(1, paxAdultos - 1)" class="w-10 h-10 rounded-xl bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-500 hover:text-intimar-primary hover:border-intimar-primary transition-all">-</button>
                                        <span class="text-3xl font-black italic text-gray-900 w-8 text-center">{{ paxAdultos }}</span>
                                        <button @click="paxAdultos++" class="w-10 h-10 rounded-xl bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-500 hover:text-intimar-primary hover:border-intimar-primary transition-all">+</button>
                                    </div>
                                </div>
                                <div class="text-center space-y-2">
                                    <label class="text-[8px] font-black uppercase text-gray-500 tracking-widest block">Niños</label>
                                    <div class="flex items-center gap-3">
                                        <button @click="paxNinos = Math.max(0, paxNinos - 1)" class="w-10 h-10 rounded-xl bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-500 hover:text-intimar-primary hover:border-intimar-primary transition-all">-</button>
                                        <span class="text-3xl font-black italic text-gray-900 w-8 text-center">{{ paxNinos }}</span>
                                        <button @click="paxNinos++" class="w-10 h-10 rounded-xl bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-500 hover:text-intimar-primary hover:border-intimar-primary transition-all">+</button>
                                    </div>
                                </div>
                            </div>

                            <!-- Alerta de Cambio -->
                            <div v-if="paxAdultos !== selectedReservaForAssign?.cant_adultos || paxNinos !== selectedReservaForAssign?.cant_ninos" class="mt-4 animate-in fade-in slide-in-from-top-2">
                                <div class="bg-intimar-gold/10 text-intimar-gold p-3 rounded-xl border border-intimar-gold/20 flex items-center gap-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
                                    <p class="text-[9px] font-black uppercase tracking-tight leading-none">¡Atención! Cantidad de PERS. modificada</p>
                                </div>
                            </div>
                        </div>

                        <button 
                            @click="proceedFromSummary" 
                            class="w-full bg-intimar-primary text-white py-5 rounded-[1.8rem] font-black uppercase text-[11px] tracking-[0.2em] shadow-xl shadow-intimar-primary/20 transition-all flex items-center justify-center gap-3 border-4 border-white"
                        >
                            CONTINUAR A MOZO
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
                        </button>
                    </div>

                    <!-- PASO 2: SELECCIONAR MOZO -->
                    <div v-if="assignStep === 2" class="space-y-6">
                        <div class="text-center">
                            <button @click="assignStep = 1.2" class="text-intimar-primary text-[8px] font-black uppercase tracking-[0.2em] mb-1 flex items-center justify-center gap-2 hover:translate-x-[-2px] transition-transform mx-auto">
                                 <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
                                 VOLVER
                            </button>
                            <h3 class="text-xl font-black text-gray-900 leading-tight italic tracking-tighter">Asignar <span class="text-intimar-primary">Mozo</span></h3>
                            <p class="text-gray-400 text-[8px] font-bold uppercase tracking-[0.2em] mt-0.5">{{ selectedReservaForAssign?.cliente_nombre }}</p>
                        </div>

                        <div v-if="mozos.loading" class="py-10 flex justify-center"><LoadingIndicator class="w-8 h-8 text-intimar-primary" /></div>
                        <div v-else class="grid grid-cols-2 gap-3 max-h-[300px] overflow-y-auto pr-1 custom-scrollbar">
                            <div 
                                v-for="mozo in mozos.data" 
                                :key="mozo.name"
                                @click="confirmarAsignacionFinal(mozo)"
                                class="p-4 bg-gray-50 border-2 border-transparent rounded-2xl hover:border-intimar-primary hover:bg-white hover:shadow-lg transition-all cursor-pointer text-center group"
                            >
                                <div class="w-10 h-10 bg-white shadow-md text-intimar-primary rounded-xl flex items-center justify-center mx-auto mb-2 text-base font-black italic group-hover:bg-intimar-primary group-hover:text-white transition-all">
                                    {{ mozo.nombre[0] }}
                                </div>
                                <p class="font-black text-gray-900 text-xs uppercase tracking-tight">{{ mozo.nombre }}</p>
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
                                <p class="font-black text-xl text-gray-700 tracking-tight text-center">{{ formatTime(selectedMesa.reserva.hora_llegada) }}</p>
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
                        v-if="session.isAdmin || session.hasRole(['Anfitriona', 'Mozo'])"
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
              <p class="text-[10px] opacity-90 leading-relaxed font-medium" v-if="toast.message" v-html="toast.message"></p>
            </div>
          </div>
        </TransitionGroup>
      </div>
    </Teleport>

    <!-- MODAL: AFORO EXCEDIDO DETALLADO -->
    <Teleport to="body">
      <transition name="modal-fade">
        <div v-if="showAforoErrorModal" class="fixed inset-0 z-[10000] flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-gray-900/70 backdrop-blur-md" @click="showAforoErrorModal = false"></div>
          <div class="relative bg-white w-full max-w-lg rounded-[2.5rem] shadow-2xl overflow-hidden animate-scaleIn border-t-8 border-red-500">
            <div class="p-8">
              <div class="flex items-center gap-4 mb-6">
                <div class="w-16 h-16 bg-red-100 text-red-600 rounded-2xl flex items-center justify-center shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
                </div>
                <div>
                  <h3 class="text-2xl font-black text-gray-900 leading-tight">Control de Aforo</h3>
                  <p class="text-xs font-bold text-gray-400 uppercase tracking-widest mt-1">Detalles de ocupación actual</p>
                </div>
              </div>

              <div class="prose prose-sm max-w-none text-gray-700" v-html="aforoErrorContent"></div>

              <div class="mt-8 flex flex-col gap-3">
                <button 
                  @click="showAforoErrorModal = false"
                  class="w-full py-4 bg-gray-900 text-white font-black rounded-2xl shadow-xl uppercase tracking-widest text-xs hover:bg-black transition-all"
                >
                  Entendido
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
    </div>
  </div>
</template>


<script setup>
import { Button, LoadingIndicator, createResource, call } from 'frappe-ui'
import { computed, ref, watch, onMounted } from 'vue'
import { VueTelInput } from 'vue-tel-input'
import 'vue-tel-input/vue-tel-input.css'
import { session } from '@/data/session'

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  return timeStr.split('.')[0]
}
import Sidebar from '@/components/Sidebar.vue'

const showAssignModal = ref(false)
const showReleaseModal = ref(false)
const selectedMesa = ref(null)
const releasing = ref(false)
const searchQuery = ref('')
const showAforoErrorModal = ref(false)
const aforoErrorContent = ref('')

const assignStep = ref(1)
const selectedReservaForAssign = ref(null)
const paxAdultos = ref(0)
const paxNinos = ref(0)
const multiSelectMode = ref(false)
const selectedMesasForMulti = ref([])

const telInputOptions = {
  mode: 'international',
  dropdownOptions: { showFlags: true, showDialCodeInSelection: true },
  inputOptions: { placeholder: '987 654 321', showDialCode: false },
  autoDefaultCountry: true
}

const quickReservaForm = ref({
    nombre: '',
    apellido: '',
    celular: '',
    codigo_pais: '',
    fullPhone: '',
    email: '',
    adultos: 2,
    ninos: 0
})

const onPhoneInput = (phone, phoneObject) => {
  if (phoneObject && phoneObject.number) {
    quickReservaForm.value.fullPhone = phoneObject.number
    quickReservaForm.value.codigo_pais = phoneObject.countryCallingCode
  }
}

const resetQuickForm = () => {
    quickReservaForm.value = {
        nombre: '',
        apellido: '',
        celular: '',
        codigo_pais: '',
        fullPhone: '',
        email: '',
        adultos: 2,
        ninos: 0
    }
}

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
    (res.cliente_telefono && res.cliente_telefono.includes(q)) ||
    res.name.toLowerCase().includes(q)
  )
})

function handleMesaClick(mesa) {
  if (mesa.estado_mesa) {
    if (!(session.isAdmin || session.hasRole('Anfitriona'))) return
    selectedMesa.value = mesa
    searchQuery.value = '' 
    assignStep.value = 1
    selectedReservaForAssign.value = null
    reservasPendientes.fetch()
    showAssignModal.value = true
  } else {
    selectedMesa.value = mesa
    showReleaseModal.value = true
  }
}

function toggleMesaSelection(mesa) {
    const index = selectedMesasForMulti.value.findIndex(m => m.name === mesa.name)
    if (index === -1) {
      selectedMesasForMulti.value.push(mesa)
    } else {
      selectedMesasForMulti.value.splice(index, 1)
    }
}

function isMesaSelectedForMulti(mesa) {
    return selectedMesasForMulti.value.some(m => m.name === mesa.name)
}

function openMultiAssignModal() {
    searchQuery.value = ''
    assignStep.value = 1
    selectedReservaForAssign.value = null
    reservasPendientes.fetch()
    showAssignModal.value = true
}

function selectReservaForAssign(reserva) {
  selectedReservaForAssign.value = reserva
  paxAdultos.value = reserva.cant_adultos || 0
  paxNinos.value = reserva.cant_ninos || 0
  assignStep.value = 1.2
}

const creatingQuickReserva = ref(false)
async function confirmarReservaRapida() {
    if (!quickReservaForm.value.nombre || !quickReservaForm.value.celular) return
    
    creatingQuickReserva.value = true
    try {
        const res = await call('intimar_erp.api.crear_reserva_rapida', {
            nombre: quickReservaForm.value.nombre,
            apellido: quickReservaForm.value.apellido,
            celular: quickReservaForm.value.fullPhone || quickReservaForm.value.celular,
            codigo_pais: quickReservaForm.value.codigo_pais,
            email: quickReservaForm.value.email,
            adultos: quickReservaForm.value.adultos,
            ninos: quickReservaForm.value.ninos
        })
        
        selectedReservaForAssign.value = res
        paxAdultos.value = res.cant_adultos
        paxNinos.value = res.cant_ninos
        assignStep.value = 2 // Ir directo a mozo
        
        if (res.cliente_reconocido) {
            showToast('Cliente Reconocido', `Se usaron los datos registrados de ${res.cliente_nombre}`, 'success')
        } else {
            showToast('Reserva Creada', 'Proceda a asignar mozo.', 'success')
        }
    } catch (e) {
        console.error(e)
        const msg = e.messages ? e.messages.join('\n') : (e.message || 'No se pudo crear la reserva rápida.')
        if (msg && msg.includes('AFORO EXCEDIDO')) {
            aforoErrorContent.value = msg
            showAforoErrorModal.value = true
        } else {
            showToast('Error', msg, 'error')
        }
    } finally {
        creatingQuickReserva.value = false
    }
}

function proceedFromSummary() {
  // Si hay anticipo pagado, podríamos mostrar un aviso extra, pero el usuario pidió resumen integrado.
  // Por seguridad, si hay anticipo mostramos el paso 1.5 o simplemente avanzamos? 
  // Integraré el anticipo en el 1.2 también para limpiar el flujo.
  assignStep.value = 2
}

async function confirmarAsignacionFinal(mozo) {
  try {
    const mesaIds = selectedMesasForMulti.value.length > 0
        ? selectedMesasForMulti.value.map(m => m.name)
        : [selectedMesa.value.name]

    const paxCambiado = (paxAdultos.value !== selectedReservaForAssign.value.cant_adultos || 
                        paxNinos.value !== selectedReservaForAssign.value.cant_ninos)

    await call('intimar_erp.api.asignar_mesa_a_reserva', {
      reserva_id: selectedReservaForAssign.value.name,
      mesa_id: mesaIds,
      mozo_id: mozo.name,
      adultos: paxAdultos.value,
      ninos: paxNinos.value
    })
    
    showAssignModal.value = false
    selectedMesasForMulti.value = []
    mesas.fetch()
    
    if (paxCambiado) {
        showToast('Asignación con Ajuste', `Mesa vinculada. Se notificó el cambio a ${paxAdultos.value + paxNinos.value} personas.`, 'warning')
    } else {
        showToast('Asignación Exitosa', 'Mesa(s) vinculada(s) correctamente.', 'success')
    }
  } catch (e) {
    console.error(e)
    const msg = e.messages ? e.messages.join('\n') : (e.message || 'No se pudo completar la asignación.')
    if (msg && msg.includes('AFORO EXCEDIDO')) {
        aforoErrorContent.value = msg
        showAforoErrorModal.value = true
    } else {
        showToast('Error', msg, 'error')
    }
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

<style scoped>
.quick-tel-input {
  border: 2px solid transparent !important;
  background-color: #f9fafb !important;
  border-radius: 1rem !important;
  padding: 0.5rem 0.75rem !important;
  transition: all 0.2s !important;
  font-family: inherit !important;
}

.quick-tel-input:focus-within {
  background-color: white !important;
  border-color: #00938F !important;
  box-shadow: 0 0 0 4px rgba(0, 147, 143, 0.1) !important;
}

:deep(.vti__input) {
  background: transparent !important;
  border: none !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  color: #111827 !important;
}

:deep(.vti__dropdown) {
  border-radius: 0.8rem !important;
  transition: background 0.2s !important;
}

:deep(.vti__dropdown:hover) {
  background-color: rgba(0, 0, 0, 0.05) !important;
}
</style>
