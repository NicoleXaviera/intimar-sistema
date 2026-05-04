<template>
  <div class="h-full flex flex-col relative w-full items-center">
    
    <!-- Toast Notifications -->
    <Teleport to="body">
      <transition-group 
        name="toast-slide" 
        tag="div" 
        class="fixed top-6 right-6 z-[9999] flex flex-col gap-3 pointer-events-none"
      >
        <div 
          v-for="toast in toasts" 
          :key="toast.id"
          class="min-w-[300px] pointer-events-auto flex items-start gap-3 px-5 py-4 rounded-2xl shadow-xl backdrop-blur-md border border-white/20 text-white font-bold"
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
          
          <button @click="removeToast(toast.id)" class="opacity-50 hover:opacity-100 transition-opacity">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
      </transition-group>
    </Teleport>

    <!-- Visor de Imágenes Pantalla Completa (Lightbox) -->
    <Teleport to="body">
      <transition name="modal-fade">
        <div v-if="imagePreviewUrl" class="fixed inset-0 z-[1000] flex items-center justify-center p-4 lg:p-12 bg-black/90 backdrop-blur-md" @click="imagePreviewUrl = null">
          <button @click="imagePreviewUrl = null" class="absolute top-6 right-6 text-white hover:text-white/70 w-12 h-12 flex items-center justify-center bg-white/10 hover:bg-white/20 rounded-full transition-all">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
          <img :src="imagePreviewUrl" class="max-w-full max-h-full object-contain rounded-2xl shadow-2xl" @click.stop>
        </div>
      </transition>
    </Teleport>

    <!-- Contenedor Central para alejar del borde -->
    <div class="w-full max-w-6xl mx-auto px-4 lg:px-8 pb-12">
      <!-- Header Fijo Superior -->
      <header class="flex items-center justify-between mb-8 sticky top-0 bg-gray-50/95 backdrop-blur-md py-4 z-[100] border-b border-gray-200/50">
        <div class="flex items-center gap-4">
        <router-link to="/reservas" class="w-10 h-10 bg-white border border-gray-100 rounded-2xl flex items-center justify-center text-gray-400 hover:text-intimar-gold hover:border-intimar-gold/30 hover:shadow-lg transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
        </router-link>
        <div>
          <h1 class="text-2xl font-black text-gray-900 tracking-tight flex items-center gap-3">
            {{ isEditing ? 'Editar Reserva' : 'Nueva Reserva' }}
            <span v-if="isEditing" class="text-xs font-black uppercase tracking-widest bg-gray-100 text-gray-400 px-3 py-1 rounded-full">{{ form.name }}</span>
          </h1>
          <p class="text-xs font-bold text-gray-400 mt-1 flex items-center gap-2">
            Gestiona la información operativa y financiera de la reserva.
          </p>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <button 
          @click="saveReserva" 
          :disabled="saving"
          class="bg-intimar-gold hover:bg-intimar-gold/90 text-white font-black text-xs uppercase tracking-[0.2em] px-8 py-3.5 rounded-2xl shadow-lg shadow-intimar-gold/20 hover:shadow-xl hover:shadow-intimar-gold/30 transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg v-if="saving" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          {{ saving ? 'Guardando...' : 'Guardar Reserva' }}
        </button>
      </div>
    </header>

      <div v-if="loading" class="flex-1 flex flex-col items-center justify-center p-12 text-gray-400">
        <svg class="animate-spin h-10 w-10 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        <h3 class="font-black tracking-widest uppercase">Cargando datos...</h3>
      </div>

      <!-- Contenido del Formulario -->
      <div v-else>
        <!-- GRAN SELECTOR DE ESTADO PERSONALIZADO -->
        <div class="mb-8 flex justify-center relative z-50">
          <div class="relative w-full max-w-lg">
            
            <!-- Botón Disparador -->
            <button 
              type="button"
              @click.stop="showEstadoDropdown = !showEstadoDropdown"
              class="w-full pl-8 pr-12 py-5 text-center text-lg font-black uppercase tracking-widest rounded-full border-4 shadow-xl transition-all focus:outline-none flex justify-center items-center gap-2"
              :class="[estadoColors.bgText, estadoColors.border]"
            >
              {{ form.estado_reserva.toUpperCase() }}
              <div class="absolute inset-y-0 right-0 pr-6 flex items-center pointer-events-none" :class="estadoColors.icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" class="transition-transform duration-300" :class="{'rotate-180': showEstadoDropdown}"><path d="m6 9 6 6 6-6"/></svg>
              </div>
            </button>

            <!-- Menú Desplegable Custom -->
            <transition name="dropdown-fade">
              <div v-if="showEstadoDropdown">
                <!-- Overlay invisible para cerrar al clickear fuera -->
                <div class="fixed inset-0 z-40" @click.stop="showEstadoDropdown = false"></div>
                
                <div class="absolute top-full left-0 w-full mt-2 bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden z-50">
                  <div class="p-1.5">
                    <button 
                      v-for="estado in estadosPermitidos" 
                      :key="estado.value"
                      @click="seleccionarEstado(estado.value)"
                      type="button"
                      class="w-full text-left px-5 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all flex items-center gap-3 relative z-50"
                      :class="form.estado_reserva === estado.value ? 'bg-gray-100 text-gray-900' : 'text-gray-500 hover:bg-gray-50 hover:text-gray-900'"
                    >
                      <span class="w-2.5 h-2.5 rounded-full shrink-0" :class="estado.colorDot"></span>
                      {{ estado.label }}
                    </button>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>

        <!-- Grid 2 Columnas -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          <!-- ================= COLUMNA IZQUIERDA: CLIENTE Y TIEMPOS ================= -->
      <div class="flex flex-col gap-6">
        
        <!-- Tarjeta: Cliente -->
        <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 relative">
          <div class="flex items-center gap-3 mb-6 border-b border-gray-100 pb-4">
            <div class="w-10 h-10 bg-intimar-primary/10 rounded-xl flex items-center justify-center text-intimar-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            </div>
            <div>
              <h3 class="font-black text-gray-900 tracking-wide">Datos del Cliente</h3>
              <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-0.5">Responsable de la mesa</p>
            </div>
          </div>

          <div class="space-y-5">
            <!-- Buscador de Cliente con Autocompletado -->
            <div>
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1">Buscar Cliente Registrado <span class="text-red-500">*</span></label>
              <div class="relative">
                <input 
                  type="text" 
                  v-model="clienteSearch" 
                  @focus="showClienteDropdown = true"
                  @blur="onClienteBlur"
                  placeholder="Escribe el nombre o celular..."
                  class="w-full pl-4 pr-10 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-intimar-primary/30 focus:bg-white focus:ring-4 focus:ring-intimar-primary/10 transition-all"
                >
                <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-400">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                </div>
                
                <!-- Lista Desplegable y Botón Crear -->
                <div v-if="showClienteDropdown" class="absolute z-50 w-full mt-2 bg-white rounded-2xl shadow-xl border border-gray-100 max-h-72 flex flex-col overflow-hidden">
                  <div class="overflow-y-auto flex-1 max-h-60">
                    <div 
                      v-for="c in filteredClientes" 
                      :key="c.name"
                      @mousedown.prevent="selectCliente(c)"
                      class="px-4 py-3 hover:bg-intimar-primary/5 cursor-pointer text-sm text-gray-700 font-bold border-b border-gray-50 last:border-0 flex justify-between items-center"
                    >
                      <span>{{ c.nombre_y_apellido_completo }}</span>
                      <span class="text-[10px] text-gray-400 bg-gray-100 px-2 py-1 rounded-md">{{ c.phone || 'Sin tel' }}</span>
                    </div>
                    <div v-if="filteredClientes.length === 0 && clienteSearch.length > 0" class="p-4 text-center">
                      <p class="text-xs font-bold text-gray-400">No se encontraron clientes.</p>
                    </div>
                  </div>
                  <!-- Botón crear nuevo -->
                  <div class="p-2 border-t border-gray-100 bg-gray-50">
                    <button 
                      @mousedown.prevent="openNewClienteModal" 
                      class="w-full py-2.5 bg-intimar-primary/10 hover:bg-intimar-primary/20 text-intimar-primary font-black uppercase tracking-widest text-[10px] rounded-xl transition-all flex items-center justify-center gap-2"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
                      CREAR NUEVO CLIENTE
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1 flex justify-between items-center">
                  Nombre Completo
                  <button 
                    v-if="form.cliente" 
                    @click="router.push('/clientes/' + form.cliente)" 
                    type="button" 
                    class="text-intimar-primary hover:text-intimar-dark transition-colors flex items-center gap-1 bg-intimar-primary/10 px-2 py-0.5 rounded-lg border border-intimar-primary/20"
                  >
                    <span class="lowercase font-black tracking-normal text-[9px]">ver perfil</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>
                  </button>
                </label>
                <input v-model="form.nombre" type="text" readonly class="w-full px-4 py-3 bg-gray-100 border border-transparent rounded-xl text-xs font-bold text-gray-500 cursor-not-allowed">
              </div>
              <div>
                <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1 flex justify-between">
                  Celular
                  <button v-if="form.celular" @click="openWhatsApp" type="button" class="text-green-600 hover:text-green-700 flex items-center gap-1 lowercase font-black tracking-normal">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    chatear
                  </button>
                </label>
                <input v-model="form.celular" type="text" readonly class="w-full px-4 py-3 bg-gray-100 border border-transparent rounded-xl text-xs font-bold text-gray-500 cursor-not-allowed">
              </div>
            </div>
          </div>
        </div>


        <!-- Tarjeta: Fecha, Hora y Asistentes -->
        <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 relative">
          <div class="flex items-center gap-3 mb-6 border-b border-gray-100 pb-4">
            <div class="w-10 h-10 bg-intimar-orange/10 rounded-xl flex items-center justify-center text-intimar-orange">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            </div>
            <div class="flex-1">
              <h3 class="font-black text-gray-900 tracking-wide">Cuándo y Cuántos</h3>
              <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-0.5">Tiempos y personas</p>
            </div>
            <!-- CAMPO: FECHA DE CREACIÓN (NUEVO) -->
            <div v-if="form.creation" class="text-right">
              <label class="block text-[8px] font-black uppercase tracking-widest text-gray-300">Registrada el</label>
              <p class="text-[10px] font-bold text-gray-400">{{ formatDateDisplay(form.creation) }}</p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-5">
            <!-- Fecha -->
            <div>
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1">Fecha Reserva <span class="text-red-500">*</span></label>
              <input v-model="form.fecha_reserva" type="date" class="w-full px-4 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all">
            </div>

            <!-- Selector de Hora Ultra-Práctico -->
            <div class="col-span-2 lg:col-span-1">
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-3 pl-1">Hora de Reserva <span class="text-red-500">*</span></label>
              
              <!-- Input para escribir hora personalizada -->
              <div class="relative mb-4">
                <input 
                  v-model="form.hora_reserva" 
                  type="text"
                  placeholder="Escribe hora (ej: 14:15) o elige abajo..."
                  class="w-full pl-12 pr-4 py-4 bg-white border-2 border-gray-100 rounded-2xl text-sm font-black text-gray-700 focus:border-intimar-gold focus:ring-0 transition-all outline-none shadow-sm"
                >
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-intimar-gold">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                </div>
              </div>

              <!-- Grid de Horas Sugeridas (DINÁMICO según Configuración) -->
              <div class="grid grid-cols-4 sm:grid-cols-5 md:grid-cols-7 lg:grid-cols-4 gap-2">
                <template v-for="h in ['11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00', '17:00:00', '17:30:00', '18:00:00', '18:30:00', '19:00:00', '19:30:00', '20:00:00', '20:30:00', '21:00:00', '21:30:00', '22:00:00']" :key="h">
                  <button 
                    v-if="isTimeInRange(h)"
                    type="button"
                    @click="form.hora_reserva = h"
                    :class="[
                      'py-2 rounded-xl text-[10px] font-black transition-all border-2',
                      form.hora_reserva === h 
                        ? 'bg-intimar-gold border-intimar-gold text-white shadow-md shadow-intimar-gold/20 scale-105' 
                        : 'bg-white border-gray-50 text-gray-400 hover:border-intimar-gold/30 hover:text-gray-600'
                    ]"
                  >
                    {{ h.substring(0, 5) }}
                  </button>
                </template>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-5 mt-5">
            <!-- Adultos -->
            <div>
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1">Cant. Adultos <span class="text-red-500">*</span></label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
                <input v-model.number="form.cant_adultos" type="number" min="1" class="w-full pl-12 pr-4 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all">
              </div>
            </div>

            <!-- Niños -->
            <div>
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1">Cant. Niños</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg></div>
                <input v-model.number="form.cant_ninos" type="number" min="0" class="w-full pl-12 pr-4 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ================= COLUMNA DERECHA: OPERATIVA, MESAS Y DINERO ================= -->
      <div class="flex flex-col gap-6">
        
        <!-- Tarjeta: Estado y Asignación -->
        <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 relative" :class="{'opacity-60': !canEditOperativa}">
          <div class="flex items-center gap-3 mb-6 border-b border-gray-100 pb-4">
            <div class="w-10 h-10 bg-intimar-gold/10 rounded-xl flex items-center justify-center text-intimar-gold">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
            </div>
            <div>
              <h3 class="font-black text-gray-900 tracking-wide">Operativa</h3>
              <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-0.5">Estado y responsables</p>
            </div>
            <div v-if="!canEditOperativa" class="ml-auto bg-amber-50 text-amber-600 px-3 py-1 rounded-full text-[8px] font-black uppercase tracking-widest border border-amber-100 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              Bloqueado: Confirma primero
            </div>
          </div>

          <div class="space-y-5">
            <!-- Mozo -->
            <div class="border-b border-gray-50 pb-5">
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1">Mozo Asignado</label>
              <div class="relative">
                <select v-model="form.mozo" @change="onMozoChange" :disabled="!canEditOperativa" class="w-full pl-4 pr-10 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-purple-500/30 focus:bg-white focus:ring-4 focus:ring-purple-500/10 transition-all appearance-none cursor-pointer disabled:cursor-not-allowed">
                  <option value="">-- Ninguno asignado todavía --</option>
                  <option v-for="m in mozosList" :key="m.name" :value="m.name">
                    {{ m.name }}
                  </option>
                </select>
                <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-400"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></div>
              </div>
            </div>

            <!-- Mesas Asignadas (INTEGRADO AQUÍ) -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 pl-1">Mesas Asignadas</label>
                <button @click="addMesaRow" type="button" :disabled="!canEditOperativa" class="flex items-center gap-1.5 px-3 py-1.5 bg-intimar-gold/10 text-intimar-gold rounded-lg hover:bg-intimar-gold/20 transition-all disabled:opacity-50">
                  <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span class="text-[9px] font-black uppercase">Añadir</span>
                </button>
              </div>

              <div class="space-y-3">
                <div v-for="(m, index) in form.mesas" :key="index" class="flex gap-2">
                  <div class="flex-1 relative">
                    <select v-model="m.mesa" :disabled="!canEditOperativa" class="w-full pl-4 pr-10 py-3 bg-gray-50 border border-transparent rounded-xl text-xs font-bold text-gray-700 focus:border-green-600 focus:bg-white transition-all appearance-none cursor-pointer">
                      <option value="">Elegir mesa...</option>
                      <option v-for="mesa in mesasList" :key="mesa.name" :value="mesa.name">
                        {{ mesa.numero_mesa }} - {{ mesa.ubicacion_mesa || 'Principal' }}
                      </option>
                    </select>
                    <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-gray-300"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m6 9 6 6 6-6"/></svg></div>
                  </div>
                  <button v-if="canEditOperativa" @click="removeMesaRow(index)" type="button" class="p-3 text-red-400 hover:text-red-600 bg-red-50 rounded-xl transition-all">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                  </button>
                </div>

                <!-- Tiempos de Ocupación -->
                <div v-if="form.hora_llegada || form.hora_salida" class="mt-4 p-4 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-100 grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-[8px] font-black uppercase tracking-widest text-blue-500 mb-0.5">Llegada</label>
                      <p class="text-xs font-black text-gray-800">{{ formatTimeDisplay(form.hora_llegada) }}</p>
                    </div>
                    <div>
                      <label class="block text-[8px] font-black uppercase tracking-widest text-green-500 mb-0.5">Salida</label>
                      <p class="text-xs font-black text-gray-800">{{ formatTimeDisplay(form.hora_salida) || '--:--' }}</p>
                    </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tarjeta: Anticipos (Sub-tabla) -->
        <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 relative">
          <div class="flex items-center justify-between mb-4 border-b border-gray-100 pb-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-intimar-dark/10 rounded-xl flex items-center justify-center text-intimar-dark">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              </div>
              <div>
                <h3 class="font-black text-gray-900 tracking-wide">Anticipos Registrados</h3>
                <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-0.5">Sub-tabla (Anticipo Reserva)</p>
              </div>
            </div>
            
            <button @click="addAnticipoRow" type="button" class="bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-black px-4 py-2 rounded-xl transition-colors flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              Anticipo
            </button>
          </div>

          <div class="mb-4 flex items-center gap-2 p-3 rounded-xl border transition-all" :class="requireAnticipoAlert ? 'bg-intimar-gold/10 border-intimar-gold text-intimar-gold' : 'bg-gray-50 border-transparent text-gray-600'">
            <input type="checkbox" v-model="form.anticipo_required" :disabled="requireAnticipoAlert" :true-value="1" :false-value="0" class="w-5 h-5 rounded text-intimar-gold focus:ring-intimar-gold cursor-pointer border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed">
            <label class="text-xs font-black uppercase tracking-widest select-none" :class="{'cursor-pointer': !requireAnticipoAlert}" @click="!requireAnticipoAlert && (form.anticipo_required = form.anticipo_required ? 0 : 1)">Requiere Anticipo</label>
            <span v-if="requireAnticipoAlert" class="ml-auto text-[10px] font-bold bg-white px-2 py-1 rounded-md shadow-sm text-intimar-gold">⚠️ OBLIGATORIO POR AFORO</span>
          </div>

          <div v-if="form.anticipos.length === 0" class="text-center py-6 border-2 border-dashed border-gray-100 rounded-2xl">
            <p class="text-xs font-bold text-gray-400">No hay anticipos registrados.</p>
          </div>

          <div v-else class="space-y-3">
            <div v-for="(row, idx) in form.anticipos" :key="idx" class="bg-gray-50 p-4 rounded-2xl relative border border-gray-100 flex items-center gap-4">
              <!-- Miniatura del comprobante -->
              <button v-if="row.comprobante" @click="isImage(row.comprobante) ? (imagePreviewUrl = row.comprobante) : window.open(row.comprobante, '_blank')" type="button" class="w-14 h-14 rounded-xl overflow-hidden shrink-0 border border-gray-200 block hover:opacity-80 transition-opacity shadow-sm bg-white cursor-zoom-in">
                <img v-if="isImage(row.comprobante)" :src="row.comprobante" class="w-full h-full object-cover">
                <div v-else class="w-full h-full flex flex-col items-center justify-center text-gray-400 bg-gray-100 cursor-pointer">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
                </div>
              </button>
              <div v-else class="w-14 h-14 rounded-xl bg-gray-100 border border-gray-200 border-dashed flex items-center justify-center text-gray-300 shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
              </div>

              <div class="flex-1">
                <p class="text-sm font-black text-gray-900">{{ row.moneda }} {{ row.monto_anticipo }}</p>
                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-widest mt-1">{{ row.banco || 'Sin ref' }} • {{ row.estado_anticipo }}</p>
              </div>
              
              <div class="flex items-center gap-1 shrink-0">
                <button @click="editAnticipoRow(idx)" type="button" class="w-8 h-8 flex items-center justify-center bg-gray-100 text-gray-500 rounded-xl hover:bg-gray-200 hover:text-gray-900 transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                </button>
                <button @click="removeAnticipoRow(idx)" type="button" class="w-8 h-8 flex items-center justify-center bg-red-100 text-red-500 rounded-xl hover:bg-red-500 hover:text-white transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Tarjeta: Personalización y Notas -->
        <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 relative">
          <div class="flex items-center gap-3 mb-6 border-b border-gray-100 pb-4">
            <div class="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center text-purple-600">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
            </div>
            <div>
              <h3 class="font-black text-gray-900 tracking-wide">Personalización y Notas</h3>
              <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-0.5">Peticiones especiales del cliente</p>
            </div>
          </div>

          <div class="space-y-6">
            <div>
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1">Requerimientos Especiales</label>
              <textarea v-model="form.requerimientos" rows="2" class="w-full px-4 py-3 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-purple-500/30 focus:bg-white focus:ring-4 focus:ring-purple-500/10 transition-all outline-none" placeholder="Sin requerimientos..."></textarea>
            </div>
            <div>
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1">Necesidades Especiales</label>
              <textarea v-model="form.necesidades" rows="2" class="w-full px-4 py-3 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-purple-500/30 focus:bg-white focus:ring-4 focus:ring-purple-500/10 transition-all outline-none" placeholder="Sin necesidades especiales..."></textarea>
            </div>
            <div>
              <label class="block text-[10px] font-black uppercase tracking-widest text-red-400 mb-2 pl-1">Alergias o Intolerancias</label>
              <textarea v-model="form.alergias" rows="2" class="w-full px-4 py-3 bg-red-50 border border-transparent rounded-2xl text-sm font-bold text-red-900 focus:border-red-500/30 focus:bg-white focus:ring-4 focus:ring-red-500/10 transition-all outline-none" placeholder="Sin alergias reportadas..."></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL DE ANTICIPO -->
    <transition name="modal-fade">
      <div v-if="showAnticipoModal" class="fixed inset-0 z-[999] flex items-center justify-center px-4">
        <div class="fixed inset-0 bg-gray-900/40 backdrop-blur-sm" @click="showAnticipoModal = false"></div>
        <div class="bg-white rounded-[2.5rem] p-8 shadow-2xl relative z-10 w-full max-w-md transform transition-all">
          <div class="flex items-center gap-3 mb-6 border-b border-gray-100 pb-4">
            <div class="w-10 h-10 bg-intimar-gold/10 rounded-xl flex items-center justify-center text-intimar-gold">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            </div>
            <div>
              <h3 class="font-black text-gray-900 tracking-wide">Registrar Anticipo</h3>
              <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-0.5">Comprobante de pago</p>
            </div>
          </div>

          <div class="space-y-4 mb-6">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1 pl-1">Monto</label>
                <input v-model.number="anticipoForm.monto_anticipo" type="number" step="0.01" min="0" class="w-full px-4 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all">
              </div>
              <div>
                <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1 pl-1">Moneda</label>
                <div class="relative">
                  <select v-model="anticipoForm.moneda" class="w-full pl-4 pr-10 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all appearance-none cursor-pointer">
                    <option value="PEN">PEN</option>
                    <option value="USD">USD</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-400"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></div>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1 pl-1">Estado Pago</label>
                <div class="relative">
                  <select v-model="anticipoForm.estado_anticipo" class="w-full pl-4 pr-10 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all appearance-none cursor-pointer">
                    <option value="Pendiente">Pendiente</option>
                    <option value="Pagado">Pagado</option>
                    <option value="Rechazado">Rechazado</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-400"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></div>
                </div>
              </div>
              <div>
                <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1 pl-1">Fecha Pago</label>
                <input v-model="anticipoForm.fecha_pago" type="date" class="w-full px-4 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all">
              </div>
            </div>

            <div>
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1 pl-1">Banco / Referencia</label>
              <input v-model="anticipoForm.banco" type="text" placeholder="Ej. BCP, Yape, Plin..." class="w-full px-4 py-3.5 bg-gray-50 border border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-intimar-gold/30 focus:bg-white focus:ring-4 focus:ring-intimar-gold/10 transition-all">
            </div>
            
            <div>
              <label class="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1 pl-1">Voucher / Comprobante</label>
              <div class="relative group">
                <input 
                  type="file" 
                  accept="image/*,.pdf"
                  @change="onComprobanteChange"
                  :disabled="uploadingFile"
                  class="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed z-20"
                >
                <div class="w-full h-32 bg-gray-50 border-2 border-dashed border-gray-200 group-hover:border-intimar-gold/50 rounded-2xl text-sm font-bold text-gray-500 transition-all flex flex-col items-center justify-center gap-2 overflow-hidden relative" :class="{'bg-intimar-gold/5 border-intimar-gold': anticipoForm.comprobante}">
                  
                  <!-- Estado: Subiendo -->
                  <template v-if="uploadingFile">
                    <svg class="animate-spin h-6 w-6 text-intimar-gold z-10" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    <span class="z-10 text-intimar-gold">Subiendo...</span>
                  </template>
                  
                  <!-- Estado: Imagen Subida -->
                  <template v-else-if="anticipoForm.comprobante">
                    <!-- Botón para agrandar (Z-index mayor al input de archivo para que sea clickeable) -->
                    <button v-if="isImage(anticipoForm.comprobante)" @click.prevent="imagePreviewUrl = anticipoForm.comprobante" type="button" class="absolute top-2 right-2 w-8 h-8 bg-white/90 backdrop-blur text-gray-700 rounded-lg flex items-center justify-center shadow-sm hover:bg-white transition-all z-30">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
                    </button>

                    <!-- Cambiamos object-cover a object-contain y agregamos un padding para que no choque con los bordes -->
                    <img v-if="isImage(anticipoForm.comprobante)" :src="anticipoForm.comprobante" class="absolute inset-0 w-full h-full object-contain p-2 opacity-80 group-hover:opacity-40 transition-opacity z-0 pointer-events-none">
                    <div v-else class="absolute inset-0 w-full h-full bg-gray-200 flex flex-col items-center justify-center text-gray-400 z-0">
                      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
                    </div>
                    
                    <div class="relative z-10 bg-white/95 backdrop-blur-md px-4 py-2 rounded-xl text-intimar-gold text-[10px] uppercase tracking-widest border border-white/50 shadow-sm opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                      Clic en la caja para cambiar foto
                    </div>
                  </template>
                  
                  <!-- Estado: Vacío -->
                  <template v-else>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400 pointer-events-none"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                    <span class="pointer-events-none">Clic para adjuntar comprobante</span>
                  </template>
                </div>
              </div>
              <button v-if="anticipoForm.comprobante && isImage(anticipoForm.comprobante)" @click="imagePreviewUrl = anticipoForm.comprobante" type="button" class="text-[10px] text-intimar-gold font-bold hover:underline mt-1 inline-block">Agrandar imagen de voucher</button>
              <a v-else-if="anticipoForm.comprobante" :href="anticipoForm.comprobante" target="_blank" class="text-[10px] text-intimar-gold font-bold hover:underline mt-1 inline-block">Abrir comprobante PDF en nueva pestaña</a>
            </div>
          </div>

          <div class="flex gap-3">
            <button @click="showAnticipoModal = false" class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-black text-xs uppercase tracking-widest px-4 py-3.5 rounded-2xl transition-all">Cancelar</button>
            <button @click="confirmarAnticipo" :disabled="uploadingFile" class="flex-1 bg-gray-900 hover:bg-black text-white font-black text-xs uppercase tracking-widest px-4 py-3.5 rounded-2xl transition-all shadow-lg shadow-black/20 disabled:opacity-50 disabled:cursor-not-allowed">
              {{ editingAnticipoIndex > -1 ? 'Actualizar' : 'Agregar' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</div>
</div>

    <!-- MODAL: NUEVO CLIENTE -->
    <Teleport to="body">
      <div v-if="showNewClienteModal" class="fixed inset-0 z-[9999] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="showNewClienteModal = false"></div>
        <div class="relative bg-white w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden animate-scaleIn">
          <div class="p-8">
            <h3 class="text-3xl font-black text-gray-900 italic tracking-tighter mb-8">
              Nuevo <span class="text-intimar-primary">Cliente</span>
            </h3>

            <div class="space-y-6">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Nombres <span class="text-red-500">*</span></label>
                  <input 
                    v-model="newClienteForm.name1"
                    type="text" 
                    placeholder="Ej. Juan"
                    class="w-full px-4 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary focus:ring-0 outline-none transition-all font-bold text-sm"
                  >
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Apellidos</label>
                  <input 
                    v-model="newClienteForm.lastname"
                    type="text" 
                    placeholder="Ej. Pérez"
                    class="w-full px-4 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary focus:ring-0 outline-none transition-all font-bold text-sm"
                  >
                </div>
              </div>

              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Celular (con código de país)</label>
                <vue-tel-input 
                  v-model="newClienteForm.phone" 
                  @on-input="onPhoneInput"
                  v-bind="telInputOptions"
                  class="bg-gray-50 border-2 border-transparent rounded-2xl focus-within:bg-white focus-within:border-intimar-primary transition-all font-bold"
                ></vue-tel-input>
              </div>
            </div>

            <div class="mt-8 flex gap-4">
              <button 
                class="flex-1 py-4 bg-intimar-primary hover:bg-[#007a77] text-white font-black rounded-2xl shadow-xl uppercase tracking-widest text-xs transition-all flex justify-center items-center gap-2 disabled:opacity-50"
                @click="saveNewCliente" 
                :disabled="savingCliente"
              >
                <svg v-if="savingCliente" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                {{ savingCliente ? 'Guardando...' : 'Guardar Cliente' }}
              </button>
              <button 
                class="py-4 px-6 text-gray-400 font-black uppercase tracking-widest text-[10px] hover:text-gray-900 bg-gray-50 rounded-2xl transition-colors" 
                @click="showNewClienteModal = false"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- MODAL: NUEVO MOZO -->
    <Teleport to="body">
      <div v-if="showNewMozoModal" class="fixed inset-0 z-[9999] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="showNewMozoModal = false"></div>
        <div class="relative bg-white w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden animate-scaleIn">
          <div class="p-8">
            <h3 class="text-3xl font-black text-gray-900 italic tracking-tighter mb-8">
              Nuevo <span class="text-purple-600">Mozo</span>
            </h3>

            <div class="space-y-6">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Nombre <span class="text-red-500">*</span></label>
                  <input 
                    v-model="newMozoForm.nombre"
                    type="text" 
                    class="w-full px-4 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-purple-600 focus:ring-0 outline-none transition-all font-bold text-sm"
                  >
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Apellido <span class="text-red-500">*</span></label>
                  <input 
                    v-model="newMozoForm.apellido"
                    type="text" 
                    class="w-full px-4 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-purple-600 focus:ring-0 outline-none transition-all font-bold text-sm"
                  >
                </div>
              </div>
              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Celular</label>
                <input 
                  v-model="newMozoForm.telefono"
                  type="text" 
                  class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-purple-600 focus:ring-0 outline-none transition-all font-bold"
                >
              </div>
            </div>

            <div class="mt-8 flex gap-4">
              <button 
                class="flex-1 py-4 bg-purple-600 hover:bg-purple-700 text-white font-black rounded-2xl shadow-xl uppercase tracking-widest text-xs transition-all flex justify-center items-center gap-2 disabled:opacity-50"
                @click="saveNewMozo" 
                :disabled="savingMozo"
              >
                <svg v-if="savingMozo" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                {{ savingMozo ? 'Guardando...' : 'Guardar Mozo' }}
              </button>
              <button class="py-4 px-6 text-gray-400 font-black uppercase tracking-widest text-[10px] hover:text-gray-900 bg-gray-50 rounded-2xl transition-colors" @click="showNewMozoModal = false">Cancelar</button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- MODAL: NUEVA MESA -->
    <Teleport to="body">
      <div v-if="showNewMesaModal" class="fixed inset-0 z-[9999] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="showNewMesaModal = false"></div>
        <div class="relative bg-white w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden animate-scaleIn">
          <div class="p-8">
            <h3 class="text-3xl font-black text-gray-900 italic tracking-tighter mb-8">
              Nueva <span class="text-green-600">Mesa</span>
            </h3>

            <div class="space-y-6">
              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Número de Mesa <span class="text-red-500">*</span></label>
                <input 
                  v-model.number="newMesaForm.numero_mesa"
                  type="number" 
                  min="1"
                  class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-green-600 focus:ring-0 outline-none transition-all font-bold"
                >
              </div>

              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Ubicación <span class="text-red-500">*</span></label>
                <div class="relative">
                  <select v-model="newMesaForm.ubicacion_mesa" class="w-full pl-6 pr-10 py-4 bg-gray-50 border-2 border-transparent rounded-2xl text-sm font-bold text-gray-700 focus:border-green-600 focus:bg-white focus:ring-0 transition-all appearance-none cursor-pointer">
                    <option value="">Selecciona una ubicación...</option>
                    <option v-for="u in ubicacionesList" :key="u.name" :value="u.name">
                      {{ u.name }}
                    </option>
                  </select>
                  <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-400"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></div>
                </div>
              </div>
            </div>

            <div class="mt-8 flex gap-4">
              <button 
                class="flex-1 py-4 bg-green-600 hover:bg-green-700 text-white font-black rounded-2xl shadow-xl uppercase tracking-widest text-xs transition-all flex justify-center items-center gap-2 disabled:opacity-50"
                @click="saveNewMesa" 
                :disabled="savingMesa"
              >
                <svg v-if="savingMesa" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                {{ savingMesa ? 'Guardando...' : 'Guardar Mesa' }}
              </button>
              <button class="py-4 px-6 text-gray-400 font-black uppercase tracking-widest text-[10px] hover:text-gray-900 bg-gray-50 rounded-2xl transition-colors" @click="showNewMesaModal = false">Cancelar</button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { call } from 'frappe-ui'
import { VueTelInput } from 'vue-tel-input'
import 'vue-tel-input/vue-tel-input.css'

const route = useRoute()
const router = useRouter()

const telInputOptions = {
  mode: 'international',
  dropdownOptions: { showFlags: true, showDialCodeInSelection: true },
  inputOptions: { placeholder: '987 654 321', showDialCode: false },
  autoDefaultCountry: true
}

const onPhoneInput = (phone, phoneObject) => {
  if (phoneObject && phoneObject.number) {
    newClienteForm.fullPhone = phoneObject.number
  }
}

const isEditing = ref(false)
const loading = ref(false)
const saving = ref(false)

// Utils
const imagePreviewUrl = ref(null)

const isImage = (url) => {
  if (!url) return false
  return /\.(jpg|jpeg|png|gif|webp)$/i.test(url)
}

const canEditOperativa = computed(() => {
  return ['Pendiente a confirmar', 'Confirmada', 'En proceso', 'Finalizada'].includes(form.estado_reserva)
})

const formatDateDisplay = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const calcularTiempoTranscurrido = (horaLlegada) => {
  if (!horaLlegada) return ''
  try {
    const [h, m, s] = horaLlegada.split(':')
    const llegada = new Date()
    llegada.setHours(h, m, s)
    const ahora = new Date()
    const diffMs = ahora - llegada
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 60) return `${diffMins} min`
    const diffHrs = Math.floor(diffMins / 60)
    const minsRestantes = diffMins % 60
    return `${diffHrs}h ${minsRestantes}m`
  } catch (e) { return '' }
}

const formatTimeDisplay = (timeStr) => {
  if (!timeStr) return ''
  // Limpiar microsegundos si existen (ej: 13:25:18.431818 -> 13:25:18)
  return timeStr.split('.')[0]
}

const isTimeInRange = (timeStr) => {
  if (!timeStr || !configuracion.value) return true
  const min = configuracion.value.hora_minima || '00:00:00'
  const max = configuracion.value.hora_maxima || '23:59:59'
  
  // Normalizar a HH:mm:ss
  const t = timeStr.includes(':') ? (timeStr.split(':').length === 2 ? timeStr + ':00' : timeStr) : timeStr
  
  return t >= min && t <= max
}

// Listas para desplegables
const clientesList = ref([])
const mozosList = ref([])
const mesasList = ref([])
const configuracion = ref(null)

// Computed: Colores dinámicos para el Estado de Reserva
const estadoColors = computed(() => {
  const e = form.estado_reserva;
  switch (e) {
    case 'Confirmada': return { bgText: 'bg-green-500 text-white', border: 'border-green-600/50', icon: 'text-green-200' }
    case 'En proceso': return { bgText: 'bg-blue-500 text-white', border: 'border-blue-600/50', icon: 'text-blue-200' }
    case 'Cancelada': return { bgText: 'bg-red-500 text-white', border: 'border-red-600/50', icon: 'text-red-200' }
    case 'Finalizada': return { bgText: 'bg-gray-800 text-white', border: 'border-gray-900/50', icon: 'text-gray-400' }
    case 'Pendiente a confirmar': return { bgText: 'bg-orange-500 text-white', border: 'border-orange-600/50', icon: 'text-orange-200' }
    case 'Lista de espera': return { bgText: 'bg-yellow-500 text-white', border: 'border-yellow-600/50', icon: 'text-yellow-200' }
    default: return { bgText: 'bg-red-500 text-white', border: 'border-red-600/50', icon: 'text-red-200' } // Solicitud
  }
})

// === CUSTOM DROPDOWN ESTADO ===
const showEstadoDropdown = ref(false)
const estadosPermitidos = [
  { value: 'Solicitud de reserva', label: 'Solicitud de reserva', colorDot: 'bg-red-500' },
  { value: 'Pendiente a confirmar', label: 'Pendiente a confirmar', colorDot: 'bg-orange-500' },
  { value: 'Confirmada', label: 'Confirmada', colorDot: 'bg-green-500' },
  { value: 'En proceso', label: 'En proceso', colorDot: 'bg-blue-500' },
  { value: 'Finalizada', label: 'Finalizada', colorDot: 'bg-gray-800' },
  { value: 'Cancelada', label: 'Cancelada', colorDot: 'bg-red-500' },
  { value: 'Lista de espera', label: 'Lista de espera', colorDot: 'bg-yellow-500' }
]

const seleccionarEstado = (estado) => {
  form.estado_reserva = estado
  showEstadoDropdown.value = false
}

// Computed: ¿Requiere anticipo por cantidad de personas?
const requireAnticipoAlert = computed(() => {
  if (!configuracion.value || !configuracion.value.anticipo_persona) return false
  const totalPersonas = (form.cant_adultos || 0) + (form.cant_ninos || 0)
  return totalPersonas >= configuracion.value.anticipo_persona
})

// Watcher para forzar el checkbox si se cumple el aforo
watch(requireAnticipoAlert, (isObligatorio) => {
  if (isObligatorio) {
    form.anticipo_required = 1
  }
}, { immediate: true })

// Toast System
const toasts = ref([])
let toastCounter = 0

const showToast = (title, message = '', type = 'success') => {
  const id = toastCounter++
  toasts.value.push({ id, title, message, type })
  setTimeout(() => removeToast(id), 5000)
}

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

// Form State
const today = new Date().toISOString().split('T')[0]

// Documento original desde Frappe para evitar CannotChangeConstantError
const originalDoc = ref(null)

const form = reactive({
  name: '',
  cliente: '',
  nombre: '',
  celular: '',
  cant_adultos: 2,
  cant_ninos: 0,
  fecha_reserva: today,
  hora_reserva: '19:00:00',
  estado_reserva: 'Solicitud de reserva',
  mozo: '',
  anticipo_required: 0,
  mesas: [],
  anticipos: [],
  hora_llegada: null,
  hora_salida: null,
  modified: null
})

// Carga Inicial
onMounted(async () => {
  const id = route.params.name
  loading.value = true

  try {
    // 1. Cargar datos base para los selects
    await Promise.all([
      fetchMozos(),
      fetchMesas(),
      fetchConfiguracion()
    ])
    // 2. Determinar si es nueva o edición
    if (id && id !== 'nueva') {
      isEditing.value = true
      form.name = id
      await fetchReservaData(id)
    } else {
      isEditing.value = false
    }

  } catch (error) {
    console.error("Error cargando formulario:", error)
    showToast("Error", "No se pudo cargar la información necesaria.", "error")
  } finally {
    loading.value = false
  }
})

const fetchMozos = async () => {
  try {
    const res = await call('frappe.client.get_list', {
      doctype: 'Mozo Intimar',
      fields: ['name'],
      limit: 100
    })
    mozosList.value = res || []
  } catch (e) { console.error(e) }
}

const fetchMesas = async () => {
  try {
    const res = await call('frappe.client.get_list', {
      doctype: 'Mesa Intimar',
      fields: ['name', 'numero_mesa', 'ubicacion_mesa'],
      limit: 500
    })
    mesasList.value = res || []
  } catch (e) { console.error(e) }
}

const fetchConfiguracion = async () => {
  try {
    const doc = await call('frappe.client.get', {
      doctype: 'Configuracion Intimar',
      name: 'Configuracion Intimar'
    })
    configuracion.value = doc
  } catch (e) { console.error("Configuración general no encontrada", e) }
}

// === BÚSQUEDA DE CLIENTE EN SERVIDOR ===
const clienteSearch = ref('')
const showClienteDropdown = ref(false)
const filteredClientes = ref([])
const searchingCliente = ref(false)
let searchTimeout = null

watch(clienteSearch, (query) => {
  if (!query || query.length < 3) {
    filteredClientes.value = []
    return
  }

  // Debounce para no saturar el servidor
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    searchingCliente.value = true
    try {
      const res = await call('frappe.client.get_list', {
        doctype: 'Cliente Intimar',
        or_filters: [
          ['nombre_y_apellido_completo', 'like', `%${query}%`],
          ['phone', 'like', `%${query}%`],
          ['name1', 'like', `%${query}%`],
          ['lastname', 'like', `%${query}%`]
        ],
        fields: ['name', 'nombre_y_apellido_completo', 'phone'],
        limit: 20
      })
      filteredClientes.value = res || []
    } catch (e) {
      console.error("Error buscando clientes:", e)
    } finally {
      searchingCliente.value = false
    }
  }, 300)
})

const selectCliente = (c) => {
  form.cliente = c.name
  form.nombre = c.nombre_y_apellido_completo
  form.celular = c.phone
  clienteSearch.value = c.nombre_y_apellido_completo // Mostrar el nombre en el input
  showClienteDropdown.value = false
}

const onClienteBlur = () => {
  // Ocultamos el dropdown. Si el input está vacío, limpiamos la selección real
  showClienteDropdown.value = false
  if (!clienteSearch.value) {
    form.cliente = ''
    form.nombre = ''
    form.celular = ''
  } else if (!form.cliente) {
    // Si escribió algo pero no seleccionó de la lista
    clienteSearch.value = ''
  }
}

// === MESAS SUBTABLE ===
const addMesaRow = () => {
  form.mesas.push({ mesa: '' })
}

const removeMesaRow = (index) => {
  form.mesas.splice(index, 1)
}

// === ANTICIPOS SUBTABLE Y MODAL ===
const showAnticipoModal = ref(false)
const uploadingFile = ref(false)
const editingAnticipoIndex = ref(-1)

const anticipoForm = reactive({
  monto_anticipo: 0,
  banco: '',
  moneda: 'PEN',
  estado_anticipo: 'Pendiente',
  fecha_pago: today,
  comprobante: ''
})

const addAnticipoRow = () => {
  editingAnticipoIndex.value = -1
  // Reset y mostrar modal
  Object.assign(anticipoForm, {
    monto_anticipo: 0,
    banco: '',
    moneda: 'PEN',
    estado_anticipo: 'Pendiente',
    fecha_pago: today,
    comprobante: ''
  })
  showAnticipoModal.value = true
}

const editAnticipoRow = (idx) => {
  editingAnticipoIndex.value = idx
  // Cargar datos al formulario para editar
  Object.assign(anticipoForm, form.anticipos[idx])
  showAnticipoModal.value = true
}

const onComprobanteChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  uploadingFile.value = true
  const formData = new FormData()
  formData.append('file', file, file.name)
  
  try {
    const res = await fetch('/api/method/upload_file', {
      method: 'POST',
      body: formData,
      credentials: 'include' // Necesario para que Frappe acepte la petición autenticada
    })
    const data = await res.json()
    if (data.message && data.message.file_url) {
      anticipoForm.comprobante = data.message.file_url
      showToast("Listo", "Voucher subido correctamente.", "success")
    } else {
      throw new Error("No se obtuvo la URL del archivo")
    }
  } catch (error) {
    console.error("Error subiendo archivo:", error)
    showToast("Error", "No se pudo subir la imagen del voucher.", "error")
  } finally {
    uploadingFile.value = false
    // Limpiar input file para permitir subir la misma foto si hubo un error
    event.target.value = ''
  }
}

const confirmarAnticipo = () => {
  if (anticipoForm.monto_anticipo <= 0) {
    showToast("Monto Inválido", "Ingresa un monto mayor a 0.", "warning")
    return
  }
  form.anticipo_required = 1
  
  if (editingAnticipoIndex.value > -1) {
    // Modo edición: actualizamos el objeto en la lista, conservando el 'name' si lo tuviera
    form.anticipos[editingAnticipoIndex.value] = { ...form.anticipos[editingAnticipoIndex.value], ...anticipoForm }
  } else {
    // Modo nuevo: lo añadimos al final
    form.anticipos.push({ ...anticipoForm })
  }
  
  showAnticipoModal.value = false
}

const removeAnticipoRow = (index) => {
  form.anticipos.splice(index, 1)
  if (form.anticipos.length === 0) {
    form.anticipo_required = 0
  }
}

// === LÓGICA DE NUEVO CLIENTE ===
const showNewClienteModal = ref(false)
const savingCliente = ref(false)
const newClienteForm = reactive({
  name1: '',
  lastname: '',
  phone: ''
})

const openNewClienteModal = () => {
  const parts = clienteSearch.value.trim().split(' ')
  newClienteForm.name1 = parts[0] || ''
  newClienteForm.lastname = parts.slice(1).join(' ') || ''
  newClienteForm.phone = ''
  showNewClienteModal.value = true
  showClienteDropdown.value = false
}

const saveNewCliente = async () => {
  if (!newClienteForm.name1) {
    showToast("Requerido", "Ingresa al menos el nombre del cliente.", "warning")
    return
  }
  savingCliente.value = true
  try {
    const result = await call('frappe.client.insert', {
      doc: {
        doctype: 'Cliente Intimar',
        name1: newClienteForm.name1,
        lastname: newClienteForm.lastname,
        phone: newClienteForm.fullPhone || newClienteForm.phone.replace(/\s/g, '')
      }
    })
    
    // Frappe a veces no devuelve el doc completo tras insert, o el computado no viene.
    // Nos aseguramos de armar el nombre para el dropdown y la selección local.
    const nombreCompleto = `${result.name1 || newClienteForm.name1} ${result.lastname || newClienteForm.lastname}`.trim()
    result.nombre_y_apellido_completo = nombreCompleto
    
    showToast("¡Cliente Creado!", "Se añadió a la base de datos.", "success")
    
    // Añadir a la caché local de listado para el dropdown
    if (clientesList.value) {
      clientesList.value.push(result)
    }
    
    // Auto-select in form
    selectCliente(result)
    
    showNewClienteModal.value = false
  } catch (error) {
    console.error("Error creando cliente:", error)
    const msg = extractErrorMessage(error)
    showToast("Error", msg || "No se pudo crear el cliente.", "error")
  } finally {
    savingCliente.value = false
  }
}

// === LÓGICA NUEVO MOZO ===
const showNewMozoModal = ref(false)
const savingMozo = ref(false)
const newMozoForm = reactive({ nombre: '', apellido: '', telefono: '' })

const onMozoChange = (e) => {
  if (e.target.value === 'CREAR_NUEVO') {
    form.mozo = ''
    newMozoForm.nombre = ''
    newMozoForm.apellido = ''
    newMozoForm.telefono = ''
    showNewMozoModal.value = true
  }
}

const saveNewMozo = async () => {
  if (!newMozoForm.nombre || !newMozoForm.apellido) {
    showToast("Requerido", "Ingresa nombre y apellido del mozo.", "warning")
    return
  }
  savingMozo.value = true
  try {
    const result = await call('frappe.client.insert', {
      doc: {
        doctype: 'Mozo Intimar',
        nombre: newMozoForm.nombre,
        apellido: newMozoForm.apellido,
        telefono: newMozoForm.telefono
      }
    })
    
    showToast("¡Mozo Creado!", "El mozo se guardó correctamente.", "success")
    if (mozosList.value) {
      mozosList.value.push(result)
    }
    form.mozo = result.name // Auto-select
    showNewMozoModal.value = false
  } catch (error) {
    console.error(error)
    const msg = extractErrorMessage(error)
    showToast("Error", msg || "No se pudo crear el mozo.", "error")
  } finally {
    savingMozo.value = false
  }
}

// === LÓGICA NUEVA MESA ===
const showNewMesaModal = ref(false)
const savingMesa = ref(false)
const activeMesaRowIndex = ref(-1)
const newMesaForm = reactive({ numero_mesa: '', ubicacion_mesa: '' })
const ubicacionesList = ref([])

const fetchUbicaciones = async () => {
  try {
    const res = await call('frappe.client.get_list', {
      doctype: 'Ubicacion Mesa Intimar',
      fields: ['name']
    })
    ubicacionesList.value = res || []
  } catch(e) {}
}

const onMesaChange = (e, idx) => {
  if (e.target.value === 'CREAR_NUEVO') {
    form.mesas[idx].mesa = ''
    newMesaForm.numero_mesa = ''
    newMesaForm.ubicacion_mesa = ''
    activeMesaRowIndex.value = idx
    showNewMesaModal.value = true
    if (ubicacionesList.value.length === 0) {
      fetchUbicaciones()
    }
  }
}

const saveNewMesa = async () => {
  if (!newMesaForm.numero_mesa || !newMesaForm.ubicacion_mesa) {
    showToast("Requerido", "Ingresa número y ubicación de mesa.", "warning")
    return
  }
  savingMesa.value = true
  try {
    const result = await call('frappe.client.insert', {
      doc: {
        doctype: 'Mesa Intimar',
        numero_mesa: newMesaForm.numero_mesa,
        ubicacion_mesa: newMesaForm.ubicacion_mesa,
        estado_mesa: 1 // Disponible
      }
    })
    showToast("¡Mesa Creada!", "Se añadió a la base de datos.", "success")
    if (mesasList.value) {
      mesasList.value.push(result)
    }
    if (activeMesaRowIndex.value > -1) {
      form.mesas[activeMesaRowIndex.value].mesa = result.name
    }
    showNewMesaModal.value = false
  } catch (error) {
    console.error(error)
    const msg = extractErrorMessage(error)
    showToast("Error", msg || "No se pudo crear la mesa.", "error")
  } finally {
    savingMesa.value = false
  }
}

// === LOAD/SAVE API ===
const fetchReservaData = async (id) => {
  try {
    const doc = await call('frappe.client.get', {
      doctype: 'Reserva Intimar',
      name: id
    })
    if (doc) {
      originalDoc.value = doc 

      form.cliente = doc.cliente || ''
      form.nombre = doc.nombre || ''
      form.celular = doc.celular || ''
      
      // Si hay un cliente enlazado, forzamos traer su nombre completo real
      if (form.cliente) {
        try {
          const clienteDoc = await call('frappe.client.get_value', {
            doctype: 'Cliente Intimar',
            filters: { name: form.cliente },
            fieldname: ['name1', 'lastname', 'nombre_y_apellido_completo', 'phone']
          })
          if (clienteDoc) {
            const nombreCalculado = `${clienteDoc.name1 || ''} ${clienteDoc.lastname || ''}`.trim()
            form.nombre = clienteDoc.nombre_y_apellido_completo || nombreCalculado || form.nombre
            form.celular = clienteDoc.phone || form.celular
          }
        } catch (e) { console.error("Error al traer datos reales del cliente", e) }
      }

      form.cant_adultos = doc.cant_adultos || 0
      form.cant_ninos = doc.cant_ninos || 0
      form.fecha_reserva = doc.fecha_reserva || today
      form.hora_reserva = doc.hora_reserva || '19:00:00'
      form.estado_reserva = doc.estado_reserva || 'Solicitud de reserva'
      form.mozo = doc.mozo || ''
      form.anticipo_required = doc.anticipo_required || 0
      form.hora_llegada = doc.hora_llegada || null
      form.hora_salida = doc.hora_salida || null
      form.requerimientos = doc.requerimientos || ''
      form.necesidades = doc.necesidades || ''
      form.alergias = doc.alergias || ''
      form.modified = doc.modified || null
      
      clienteSearch.value = form.nombre
      
      // Mapeo de tablas hijas
      form.mesas = (doc.mesas || []).map(m => ({ mesa: m.mesa }))
      form.anticipos = (doc.anticipos || []).map(a => ({ 
        ...a,
        comprobante: a.comprobante || ''
      }))
    }
  } catch (error) {
    console.error("Error al obtener doc:", error)
    showToast("Error", "No se encontró la reserva en el sistema.", "error")
  }
}

const openWhatsApp = () => {
  if (!form.celular) return
  
  const cleanPhone = form.celular.replace(/\D/g, '')
  const totalPersonas = (form.cant_adultos || 0) + (form.cant_ninos || 0)
  
  // Formatear fecha de YYYY-MM-DD a DD-MM-YYYY
  let displayDate = form.fecha_reserva
  if (form.fecha_reserva) {
    const [y, m, d] = form.fecha_reserva.split('-')
    displayDate = `${d}-${m}-${y}`
  }

  // Mensaje más limpio y compatible
  const message = encodeURIComponent(
    `*INTIMAR - Info Reserva*\n\n` +
    `Hola *${form.nombre}*, te escribimos sobre tu reserva *${form.name || ''}*.\n\n` +
    `> Fecha: ${displayDate}\n` +
    `> Hora: ${form.hora_reserva}\n` +
    `> Personas: ${totalPersonas}\n` +
    `> Estado: ${form.estado_reserva}`
  )
  
  window.open(`https://wa.me/${cleanPhone}?text=${message}`, '_blank')
}

const saveReserva = async () => {
  if (!form.cliente) {
    showToast("Requerido", "Debes seleccionar un cliente.", "warning")
    return
  }
  if (!form.fecha_reserva || !form.hora_reserva) {
    showToast("Requerido", "Debes especificar fecha y hora.", "warning")
    return
  }
  
  // Validación de Anticipo Obligatorio (REFORZADA)
  if (requireAnticipoAlert.value && form.anticipos.length === 0) {
    showToast(
      "Anticipo Obligatorio", 
      `Para grupos de ${configuracion.value.anticipo_persona} o más personas es OBLIGATORIO registrar el anticipo antes de guardar.`, 
      "error"
    )
    // Aseguramos que el checkbox esté marcado para que el usuario vea la sección
    form.anticipo_required = 1
    return
  }

  // Validación de Horario (NUEVO CANDADO)
  if (!isTimeInRange(form.hora_reserva)) {
    showToast(
      "Horario No Permitido", 
      `La hora ${form.hora_reserva.substring(0, 5)} está fuera del rango de atención (${configuracion.value.hora_minima.substring(0, 5)} - ${configuracion.value.hora_maxima.substring(0, 5)}).`, 
      "error"
    )
    return
  }

  saving.value = true

  let payload = {}

  if (isEditing.value && originalDoc.value) {
    // Modo Edición: Clonamos el doc original completo y sobrescribimos solo lo necesario
    payload = {
      ...originalDoc.value,
      cliente: form.cliente,
      cant_adultos: form.cant_adultos,
      cant_ninos: form.cant_ninos,
      fecha_reserva: form.fecha_reserva,
      hora_reserva: form.hora_reserva,
      estado_reserva: form.estado_reserva,
      mozo: form.mozo,
      anticipo_required: form.anticipo_required,
      requerimientos: form.requerimientos || '',
      necesidades: form.necesidades || '',
      alergias: form.alergias || '',
    }
    // Para tablas hijas, conservamos el ID 'name' si ya existía para que Frappe lo actualice en lugar de recrearlo
    payload.mesas = form.mesas.filter(m => m.mesa).map((m, idx) => {
      const originalRow = (originalDoc.value.mesas || [])[idx]
      return { ...m, name: originalRow ? originalRow.name : undefined }
    })
    payload.anticipos = form.anticipos.map((a, idx) => {
      const originalRow = (originalDoc.value.anticipos || [])[idx]
      return { ...a, name: originalRow ? originalRow.name : undefined }
    })
  } else {
    // Modo Creación: Objeto desde cero
    payload = {
      doctype: 'Reserva Intimar',
      cliente: form.cliente,
      cant_adultos: form.cant_adultos,
      cant_ninos: form.cant_ninos,
      fecha_reserva: form.fecha_reserva,
      hora_reserva: form.hora_reserva,
      estado_reserva: form.estado_reserva,
      mozo: form.mozo,
      anticipo_required: form.anticipo_required,
      requerimientos: form.requerimientos || '',
      necesidades: form.necesidades || '',
      alergias: form.alergias || '',
      mesas: form.mesas.filter(m => m.mesa),
      anticipos: form.anticipos.map(a => ({
        monto_anticipo: a.monto_anticipo,
        banco: a.banco,
        moneda: a.moneda,
        estado_anticipo: a.estado_anticipo,
        fecha_pago: a.fecha_pago,
        comprobante: a.comprobante
      }))
    }
  }

  try {
    let result = null
    
    if (isEditing.value) {
      // Pasamos payload completo
      result = await call('frappe.client.save', { doc: payload })
      // Actualizamos originalDoc por si guardan de nuevo
      if (result) {
        originalDoc.value = { ...result }
        form.modified = result.modified
      }
      showToast("¡Actualizada!", "La reserva se actualizó correctamente.", "success")
    } else {
      // Para crear
      result = await call('frappe.client.insert', {
        doc: payload
      })
      showToast("¡Creada!", "La nueva reserva se guardó con éxito.", "success")
      
      // Si se guardó con éxito y era nueva, cambiamos la URL a edición suavemente
      if (result && result.name) {
        setTimeout(() => {
          router.replace(`/reservas/${result.name}`)
        }, 1500)
      }
    }
    
  } catch (error) {
    console.error("Error guardando:", error)
    
    // Manejo específico del error de concurrencia de Frappe
    if (error && error.exc_type === "TimestampMismatchError" || (error.message && error.message.includes('modificado después de haber sido abierto'))) {
      showToast(
        "Conflicto de Edición", 
        "Alguien más modificó esta reserva mientras la tenías abierta, o se actualizó en otra pestaña. Por favor, recarga la página.", 
        "error"
      )
    } else {
      const msg = extractErrorMessage(error)
      showToast("Error al guardar", msg || "Verifica tu conexión y permisos.", "error")
    }
  } finally {
    saving.value = false
  }
}

/**
 * Extrae el mensaje de error real enviado por el servidor Frappe
 */
const extractErrorMessage = (error) => {
  if (!error) return null

  // 1. Si frappe-ui ya procesó los mensajes
  if (error.messages && error.messages.length > 0) {
    return error.messages.join('\n')
  }

  // 2. Intentar buscar en _server_messages (formato JSON de Frappe)
  if (error._server_messages) {
    try {
      const messages = JSON.parse(error._server_messages)
      return messages
        .map(m => {
          try {
            const inner = JSON.parse(m)
            return inner.message || m
          } catch (e) {
            return m
          }
        })
        .join('\n')
    } catch (e) {}
  }

  // 3. Fallback al mensaje directo si no es el genérico de ValidationError
  if (error.message && !error.message.includes('ValidationError') && !error.message.includes('frappe.client')) {
    return error.message
  }

  // 4. Si el mensaje es un string que parece JSON
  if (typeof error.message === 'string' && (error.message.startsWith('[') || error.message.startsWith('{'))) {
    try {
      const parsed = JSON.parse(error.message)
      if (Array.isArray(parsed)) return parsed.join('\n')
      if (parsed.message) return parsed.message
    } catch (e) {}
  }

  return null
}
</script>

<style scoped>
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.toast-slide-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.95);
}
.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.95);
}

.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}
</style>
