<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />

    <div class="flex-1 p-6 md:p-12 pb-32 md:pb-12 overflow-y-auto">
      <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
          <div>
            <h2 class="text-5xl font-black text-gray-900 tracking-tighter italic flex items-center gap-4">
              Configuración
              <button @click="openGuide('general')" class="w-10 h-10 bg-white shadow-sm border border-gray-100 text-intimar-bordeaux rounded-2xl flex items-center justify-center hover:scale-110 transition-all active:scale-95" title="Ver Guía Completa">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
              </button>
            </h2>
            <p class="text-gray-400 font-bold uppercase tracking-widest text-[10px] mt-2 ml-1">Motor de Aforo e Inteligencia de Reservas</p>
          </div>
          <Button 
            variant="solid" 
            class="bg-intimar-primary hover:bg-[#007a77] text-white px-10 py-6 rounded-2xl shadow-xl shadow-intimar-primary/20 font-black uppercase tracking-widest text-xs transition-all transform hover:scale-[1.03]"
            @click="saveConfig"
            :loading="saving"
          >
            GUARDAR CAMBIOS
          </Button>
        </div>

        <div v-if="loading" class="py-20 flex justify-center"><LoadingIndicator class="w-10 h-10 text-intimar-primary" /></div>
        
        <div v-else class="space-y-8">
          <!-- Alerta de Error -->
          <div v-if="errorMessage" class="bg-red-50 border-2 border-red-100 p-6 rounded-[2rem] flex items-center gap-4 animate-shake">
            <div class="w-10 h-10 bg-red-500 rounded-full flex items-center justify-center text-white shrink-0 shadow-lg shadow-red-200">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            </div>
            <p class="text-red-600 font-black uppercase tracking-tight text-xs">{{ errorMessage }}</p>
          </div>

          <!-- Alerta de Éxito -->
          <div v-if="successMessage" class="bg-green-50 border-2 border-green-100 p-6 rounded-[2rem] flex items-center gap-4 animate-bounce-subtle">
            <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white shrink-0 shadow-lg shadow-green-200">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            </div>
            <p class="text-green-600 font-black uppercase tracking-tight text-xs">{{ successMessage }}</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Card: Operación (AHORA PRIMERO Y ANCHO COMPLETO) -->
            <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 md:col-span-2">
              <h3 class="text-lg font-black text-gray-900 uppercase tracking-tighter mb-6 flex items-center gap-3">
                <span class="w-2 h-8 bg-intimar-bordeaux rounded-full"></span>
                Operación
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-1 flex items-center gap-1.5">
                    Aforo Máximo (Sillas)
                    <button @click="openGuide('aforo')" class="w-4 h-4 bg-gray-100 text-gray-400 rounded-full flex items-center justify-center hover:bg-intimar-primary hover:text-white transition-all">
                      <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                    </button>
                  </label>
                  <p class="text-[8px] text-gray-400 ml-2 mb-2 italic">Capacidad total de comensales sentados simultáneamente.</p>
                  <input v-model="formData.aforo_maximo" type="number" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-1 flex items-center gap-1.5">
                    Duración Estándar (Horas)
                    <button @click="openGuide('duracion')" class="w-4 h-4 bg-gray-100 text-gray-400 rounded-full flex items-center justify-center hover:bg-intimar-primary hover:text-white transition-all">
                      <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                    </button>
                  </label>
                  <input v-model="formData.duracion_reserva" type="number" step="0.5" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-1 flex items-center gap-1.5">
                    Duración Grupos >8 (Horas)
                    <button @click="openGuide('grupos')" class="w-4 h-4 bg-gray-100 text-gray-400 rounded-full flex items-center justify-center hover:bg-intimar-primary hover:text-white transition-all">
                      <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                    </button>
                  </label>
                  <input v-model="formData.duracion_reserva_grande" type="number" step="0.5" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-1 flex items-center gap-1.5">
                    Margen de Seguridad (Minutos)
                    <button @click="openGuide('margen')" class="w-4 h-4 bg-gray-100 text-gray-400 rounded-full flex items-center justify-center hover:bg-intimar-primary hover:text-white transition-all">
                      <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                    </button>
                  </label>
                  <input v-model="formData.margen_limpieza" type="number" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
                <div class="md:col-span-2 bg-amber-50/50 p-6 rounded-3xl border border-amber-100/50">
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-amber-600 ml-2 mb-2 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M6 13.87A4 4 0 0 1 7.41 6a5.11 5.11 0 0 1 1.05-1.54 5 5 0 0 1 7.08 0A5.11 5.11 0 0 1 16.59 6 4 4 0 0 1 18 13.87V21H6Z"/><line x1="6" x2="18" y1="17" y2="17"/></svg>
                    Capacidad de Cocina (Personas / 30 min)
                  </label>
                  <div class="flex flex-col md:flex-row gap-6 items-center">
                    <div class="flex gap-2">
                      <div class="w-24">
                        <label class="text-[8px] font-bold text-amber-600/50 uppercase mb-1 block">Pax (Límite)</label>
                        <input v-model="formData.capacidad_cocina_30min" type="number" class="w-full px-4 py-3 bg-white border-2 border-amber-200 rounded-xl focus:border-amber-500 outline-none transition-all font-black text-lg text-amber-700 shadow-sm" placeholder="Pax">
                      </div>
                      <div class="w-32">
                        <label class="text-[8px] font-bold text-amber-600/50 uppercase mb-1 block">Cada (Bloque)</label>
                        <input v-model="formData.intervalo_flujo_cocina" type="number" class="w-full px-4 py-3 bg-white border-2 border-amber-200 rounded-xl focus:border-amber-500 outline-none transition-all font-black text-lg text-amber-700 shadow-sm" placeholder="Min">
                      </div>
                    </div>
                    <div class="flex-1">
                      <p class="text-[11px] text-amber-800 leading-tight font-black uppercase italic mb-1 flex items-center justify-between">
                        <span class="flex items-center gap-1.5">
                          <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                          Protección de Cocina
                        </span>
                        <button @click="openGuide('cocina')" class="w-4 h-4 bg-amber-200 text-amber-700 rounded-full flex items-center justify-center hover:bg-amber-500 hover:text-white transition-all">
                          <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                        </button>
                      </p>
                      <p class="text-[10px] text-amber-800/80 leading-relaxed font-medium">
                        Define el ritmo máximo. Por ejemplo: <b>30 personas cada 30 minutos</b>. Esto evita que lleguen demasiadas comandas al mismo tiempo aunque el salón esté vacío.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

    <!-- MODAL: GUÍA DE AFORO (POPUP) -->
    <Teleport to="body">
      <transition name="modal-fade">
        <div v-if="showAforoGuide" class="fixed inset-0 z-[10000] flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-gray-900/80 backdrop-blur-md" @click="showAforoGuide = false"></div>
          <div class="relative bg-gray-900 text-white w-full max-w-3xl max-h-[90vh] md:max-h-none rounded-[2rem] md:rounded-[3rem] shadow-2xl overflow-y-auto md:overflow-hidden border border-white/10 animate-scaleIn">
            <button @click="showAforoGuide = false" class="absolute top-8 right-8 w-10 h-10 bg-white/5 rounded-full flex items-center justify-center text-white/40 hover:text-white hover:bg-white/10 transition-all z-20">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>

            <div class="p-6 md:p-14 relative z-10">
              <div class="flex items-center gap-4 md:gap-5 mb-8 md:mb-10">
                <div class="w-12 h-12 md:w-16 md:h-16 bg-intimar-primary/20 text-intimar-primary rounded-2xl md:rounded-[1.5rem] flex items-center justify-center shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="md:w-8 md:h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                </div>
                <div>
                  <h3 class="text-xl md:text-3xl font-black italic tracking-tight text-white leading-tight">Lógica de Aforo</h3>
                  <p class="text-[8px] md:text-[10px] font-bold uppercase tracking-[0.2em] md:tracking-[0.4em] text-intimar-primary mt-0.5 md:mt-1">Guía para el Administrador</p>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12">
                <!-- SECCIÓN: AFORO -->
                <div v-if="helpSection === 'general' || helpSection === 'aforo'" class="flex gap-5">
                  <span class="text-4xl font-black text-intimar-primary opacity-30 mt-1">01</span>
                  <div class="space-y-2">
                    <p class="font-black uppercase tracking-widest text-xs text-white">Aforo Máximo</p>
                    <p class="text-sm text-gray-400 leading-relaxed">
                      Representa el límite físico de <b class="text-white">162 personas</b>. El sistema bloquea nuevas reservas cuando la suma de clientes sentados y próximos a llegar alcanza este número.
                    </p>
                  </div>
                </div>

                <!-- SECCIÓN: DURACIÓN -->
                <div v-if="helpSection === 'general' || helpSection === 'duracion'" class="flex gap-5">
                  <span class="text-4xl font-black text-intimar-primary opacity-30 mt-1">02</span>
                  <div class="space-y-2">
                    <p class="font-black uppercase tracking-widest text-xs text-white">Duración Estándar</p>
                    <p class="text-sm text-gray-400 leading-relaxed">
                      Es el tiempo base (ej. 1.5h) que se le asigna a una mesa pequeña. Sirve para calcular cuándo se desocuparán las sillas para el siguiente grupo.
                    </p>
                  </div>
                </div>

                <!-- SECCIÓN: GRUPOS -->
                <div v-if="helpSection === 'general' || helpSection === 'grupos'" class="flex gap-5">
                  <span class="text-4xl font-black text-intimar-primary opacity-30 mt-1">03</span>
                  <div class="space-y-2">
                    <p class="font-black uppercase tracking-widest text-xs text-white">Duración Grupos >8</p>
                    <p class="text-sm text-gray-400 leading-relaxed">
                      Los grupos grandes demoran más en comer. Este ajuste les da un tiempo extendido (ej. 2.5h) automáticamente al momento de reservar.
                    </p>
                  </div>
                </div>

                <!-- SECCIÓN: MARGEN -->
                <div v-if="helpSection === 'general' || helpSection === 'margen'" class="flex gap-5">
                  <span class="text-4xl font-black text-intimar-primary opacity-30 mt-1">04</span>
                  <div class="space-y-2">
                    <p class="font-black uppercase tracking-widest text-xs text-white">Margen de Seguridad</p>
                    <p class="text-sm text-gray-400 leading-relaxed">
                       <b>Garantía de Turno:</b> Protege al cliente que llega. Si la mesa anterior se demora un poco en salir, este colchón evita que los clientes se amontonen en la recepción.
                    </p>
                  </div>
                </div>

                <!-- SECCIÓN: COCINA -->
                <div v-if="helpSection === 'general' || helpSection === 'cocina'" class="flex gap-5 md:col-span-2">
                  <span class="text-4xl font-black text-amber-500 opacity-40 mt-1">05</span>
                  <div class="space-y-2">
                    <p class="font-black uppercase tracking-widest text-xs text-amber-500">Protección de Cocina</p>
                    <p class="text-sm text-gray-400 leading-relaxed">
                      Controla cuántas personas pueden <b>llegar</b> en cada bloque de tiempo. Si el límite es 30 pax cada 30 min, el sistema bloqueará ese horario aunque haya mesas vacías, para proteger la calidad de los platos.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>

            <!-- Card: Horarios -->
            <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
              <h3 class="text-lg font-black text-gray-900 uppercase tracking-tighter mb-6 flex items-center gap-3">
                <span class="w-2 h-8 bg-intimar-orange rounded-full"></span>
                Horarios
              </h3>
              <div class="space-y-6">
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Hora de Apertura</label>
                  <input v-model="formData.hora_minima" type="time" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Hora de Cierre</label>
                  <input v-model="formData.hora_maxima" type="time" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
              </div>
            </div>

            <!-- Card: Anticipos -->
            <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
              <h3 class="text-lg font-black text-gray-900 uppercase tracking-tighter mb-6 flex items-center gap-3">
                <span class="w-2 h-8 bg-intimar-gold rounded-full"></span>
                Anticipos
              </h3>
              <div class="space-y-6">
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Límite de Personas</label>
                  <input v-model="formData.anticipo_persona" type="number" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Monto por Persona (S/)</label>
                  <input v-model="formData.monto_anticipo_persona" type="number" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
              </div>
            </div>

            <!-- Card: Cierres Especiales -->
            <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 md:col-span-2">
              <h3 class="text-lg font-black text-gray-900 uppercase tracking-tighter mb-6 flex items-center gap-3">
                <span class="w-2 h-8 bg-red-600 rounded-full"></span>
                Cierres Especiales (Días, Fechas y Horas)
              </h3>
              <div class="space-y-4">
                <p class="text-[10px] text-gray-400 ml-2 mb-3 italic">
                  Defina días recurrentes o fechas del calendario específicas que deban permanecer cerradas total o parcialmente.
                </p>
                <div class="overflow-x-auto border border-gray-100 rounded-3xl">
                  <table class="w-full text-left border-collapse">
                    <thead>
                      <tr class="bg-gray-50 border-b border-gray-100">
                        <th class="p-4 text-[9px] font-black uppercase tracking-widest text-gray-400">Tipo de Cierre</th>
                        <th class="p-4 text-[9px] font-black uppercase tracking-widest text-gray-400">Día / Fecha</th>
                        <th class="p-4 text-[9px] font-black uppercase tracking-widest text-gray-400">Cobertura</th>
                        <th class="p-4 text-[9px] font-black uppercase tracking-widest text-gray-400">Horas (Separadas por coma)</th>
                        <th class="p-4 text-[9px] font-black uppercase tracking-widest text-gray-400 text-center w-16">Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(row, idx) in cierresList" :key="idx" class="border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
                        <td class="p-3">
                          <select v-model="row.tipo" class="px-3 py-2 bg-gray-50 border border-gray-100 rounded-xl outline-none font-bold text-xs focus:border-intimar-primary">
                            <option value="dia_semana">Día de la Semana</option>
                            <option value="fecha">Fecha Específica</option>
                          </select>
                        </td>
                        <td class="p-3">
                          <select v-if="row.tipo === 'dia_semana'" v-model="row.valor" class="px-3 py-2 bg-gray-50 border border-gray-100 rounded-xl outline-none font-bold text-xs focus:border-intimar-primary w-full max-w-[150px]">
                            <option value="lunes">Lunes</option>
                            <option value="martes">Martes</option>
                            <option value="miercoles">Miércoles</option>
                            <option value="jueves">Jueves</option>
                            <option value="viernes">Viernes</option>
                            <option value="sabado">Sábado</option>
                            <option value="domingo">Domingo</option>
                          </select>
                          <input v-else v-model="row.valor" type="date" class="px-3 py-2 bg-gray-50 border border-gray-100 rounded-xl outline-none font-bold text-xs focus:border-intimar-primary w-full max-w-[150px]">
                        </td>
                        <td class="p-3">
                          <select v-model="row.cobertura" class="px-3 py-2 bg-gray-50 border border-gray-100 rounded-xl outline-none font-bold text-xs focus:border-intimar-primary">
                            <option value="todo">Todo el día</option>
                            <option value="horas">Horas Específicas</option>
                          </select>
                        </td>
                        <td class="p-3">
                          <input v-if="row.cobertura === 'horas'" v-model="row.horasInput" type="text" class="w-full px-3 py-2 bg-gray-50 border border-gray-100 rounded-xl outline-none font-bold text-xs focus:border-intimar-primary placeholder-gray-300" placeholder="Ej: 12:00-14:30 o 12:00, 12:30">
                          <span v-else class="text-[10px] text-gray-300 font-bold uppercase tracking-wider ml-3">Día Completo</span>
                        </td>
                        <td class="p-3 text-center">
                          <button @click="removeCierreRow(idx)" class="w-8 h-8 rounded-full bg-red-50 text-red-500 hover:bg-red-500 hover:text-white transition-all flex items-center justify-center mx-auto active:scale-90" title="Eliminar fila">
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                          </button>
                        </td>
                      </tr>
                      <tr v-if="cierresList.length === 0">
                        <td colspan="5" class="p-8 text-center text-gray-300 font-bold uppercase tracking-widest text-[10px]">No hay cierres configurados</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <button @click="addCierreRow" class="mt-4 px-6 py-3 bg-gray-900 hover:bg-gray-800 text-white rounded-2xl font-black uppercase tracking-widest text-[9px] transition-all flex items-center gap-2 active:scale-95">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                  AGREGAR CIERRE
                </button>
              </div>
            </div>
          </div>
        </div>
    </div>
  </div>
</div>
</template>



<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Button, LoadingIndicator, call } from 'frappe-ui'
import Sidebar from '@/components/Sidebar.vue'

const loading = ref(true)
const saving = ref(false)
const showAforoGuide = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const helpSection = ref('general')

const cierresList = ref([])

const addCierreRow = () => {
  cierresList.value.push({
    tipo: 'dia_semana',
    valor: 'miercoles',
    cobertura: 'todo',
    horasInput: ''
  })
}

const removeCierreRow = (idx) => {
  cierresList.value.splice(idx, 1)
}

const openGuide = (section) => {
  helpSection.value = section
  showAforoGuide.value = true
}

const formData = reactive({
  anticipo_persona: 0,
  monto_anticipo_persona: 0,
  duracion_reserva: 2,
  duracion_reserva_grande: 2.5,
  margen_limpieza: 15,
  aforo_maximo: 162,
  capacidad_cocina_30min: 30,
  intervalo_flujo_cocina: 30,
  hora_minima: '09:00:00',
  hora_maxima: '22:00:00',
  cierres_especiales: ''
})

const fetchConfig = async () => {
  loading.value = true
  try {
    const data = await call('frappe.client.get', {
      doctype: 'Configuracion Intimar',
      name: 'Configuracion Intimar'
    })
    
    if (data) {
      formData.anticipo_persona = data.anticipo_persona || 0
      formData.monto_anticipo_persona = data.monto_anticipo_persona || 0
      formData.duracion_reserva = data.duracion_reserva || 2
      formData.duracion_reserva_grande = data.duracion_reserva_grande || 2.5
      formData.margen_limpieza = data.margen_limpieza || 15
      formData.aforo_maximo = data.aforo_maximo || 162
      formData.capacidad_cocina_30min = data.capacidad_cocina_30min || 30
      formData.intervalo_flujo_cocina = data.intervalo_flujo_cocina || 30
      formData.hora_minima = data.hora_minima || '09:00:00'
      formData.hora_maxima = data.hora_maxima || '22:00:00'
      formData.cierres_especiales = data.cierres_especiales || ''
      try {
        const parsed = JSON.parse(data.cierres_especiales)
        if (Array.isArray(parsed)) {
          cierresList.value = parsed.map(item => ({
            tipo: item.tipo || 'dia_semana',
            valor: item.valor || '',
            cobertura: item.cobertura || 'todo',
            horasInput: Array.isArray(item.horas) ? item.horas.join(', ') : (item.horas || '')
          }))
        } else {
          cierresList.value = []
        }
      } catch (e) {
        cierresList.value = []
        if (data.cierres_especiales) {
          const lines = data.cierres_especiales.split('\n')
          lines.forEach(line => {
            const trimmed = line.trim()
            if (!trimmed) return
            let tipo = 'dia_semana'
            let valor = trimmed
            let cobertura = 'todo'
            let horasInput = ''
            
            if (trimmed.match(/^\d{4}-\d{2}-\d{2}/)) {
              tipo = 'fecha'
            }
            
            if (trimmed.includes(':')) {
              cobertura = 'horas'
              const parts = trimmed.split(':')
              valor = parts[0].trim()
              horasInput = parts[1].trim()
            }
            
            cierresList.value.push({ tipo, valor, cobertura, horasInput })
          })
        }
      }
      
      // Asegurar que Miércoles esté siempre incluido por defecto en la lista interactiva
      const tieneMiercoles = cierresList.value.some(row => row.tipo === 'dia_semana' && row.valor === 'miercoles')
      if (!tieneMiercoles) {
        cierresList.value.unshift({
          tipo: 'dia_semana',
          valor: 'miercoles',
          cobertura: 'todo',
          horasInput: ''
        })
      }
    }
  } catch (e) {
    console.error('Error cargando config:', e)
    errorMessage.value = 'NO SE PUDO CARGAR LA CONFIGURACIÓN'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchConfig()
})


const saveConfig = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  
  // Serializar la lista de cierres a JSON
  const serialized = cierresList.value.map(row => {
    const horas = row.cobertura === 'horas'
      ? row.horasInput.split(',').map(h => h.trim()).filter(h => h.match(/^\d{2}:\d{2}$/) || h.match(/^\d{2}:\d{2}\s*-\s*\d{2}:\d{2}$/))
      : []
    return {
      tipo: row.tipo,
      valor: row.valor,
      cobertura: row.cobertura,
      horas: horas
    }
  })
  formData.cierres_especiales = JSON.stringify(serialized)
  
  saving.value = true
  try {
    await call('frappe.client.set_value', {
      doctype: 'Configuracion Intimar',
      name: 'Configuracion Intimar',
      fieldname: {
        anticipo_persona: formData.anticipo_persona,
        monto_anticipo_persona: formData.monto_anticipo_persona,
        duracion_reserva: formData.duracion_reserva,
        duracion_reserva_grande: formData.duracion_reserva_grande,
        margen_limpieza: formData.margen_limpieza,
        aforo_maximo: formData.aforo_maximo,
        capacidad_cocina_30min: formData.capacidad_cocina_30min,
        intervalo_flujo_cocina: formData.intervalo_flujo_cocina,
        hora_minima: formData.hora_minima,
        hora_maxima: formData.hora_maxima,
        cierres_especiales: formData.cierres_especiales
      }
    })
    
    successMessage.value = '¡CONFIGURACIÓN ACTUALIZADA CON ÉXITO!'
    setTimeout(() => { successMessage.value = '' }, 3000)
    await fetchConfig()
  } catch (e) {
    errorMessage.value = 'ERROR AL GUARDAR: ' + (e.messages?.[0] || e.message || 'Error desconocido')
  } finally {
    saving.value = false
  }
}
</script>

