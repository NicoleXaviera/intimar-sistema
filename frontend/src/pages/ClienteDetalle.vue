<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />

    <div class="flex-1 p-6 md:p-12 pb-32 md:pb-12 overflow-y-auto font-sans">
      <div class="max-w-5xl mx-auto">
        <!-- Botón Volver -->
        <router-link to="/clientes" class="inline-flex items-center gap-2 text-gray-500 hover:text-intimar-primary font-black uppercase tracking-widest text-[10px] mb-8 transition-colors group">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="transform group-hover:-translate-x-1 transition-transform"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          Volver al Directorio
        </router-link>

        <div v-if="cliente.loading" class="py-20 flex justify-center"><LoadingIndicator class="w-12 h-12 text-intimar-primary" /></div>
        
        <div v-else-if="cliente.data" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
          <!-- Cabecera de Perfil -->
          <div class="bg-white p-8 md:p-12 rounded-[3rem] shadow-xl shadow-gray-200/50 border border-gray-100 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-64 h-64 bg-intimar-primary/5 rounded-bl-full -mr-20 -mt-20"></div>
            
            <div class="relative z-10 flex flex-col md:flex-row items-center md:items-start gap-8">
              <div class="w-32 h-32 bg-intimar-primary text-white rounded-[2.5rem] flex items-center justify-center text-4xl font-black shadow-2xl shadow-intimar-primary/30">
                {{ cliente.data.name1?.[0] }}{{ cliente.data.lastname?.[0] }}
              </div>
              
              <div class="flex-1 text-center md:text-left">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                  <div class="flex items-center gap-4">
                    <h1 class="text-4xl font-black text-gray-900 tracking-tighter uppercase italic">{{ cliente.data.nombre_y_apellido_completo }}</h1>
                    <span class="px-4 py-1 bg-intimar-gold/10 text-intimar-gold rounded-full text-[10px] font-black uppercase tracking-widest border border-intimar-gold/20">Cliente VIP</span>
                  </div>
                  
                  <Button 
                    variant="outline" 
                    class="rounded-xl border-gray-100 hover:border-intimar-primary hover:text-intimar-primary font-black uppercase text-[10px] tracking-widest px-6 py-4 flex items-center gap-2"
                    @click="openEditModal"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>
                    Editar Datos
                  </Button>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                  <div class="flex items-center gap-3 text-gray-500">
                    <div class="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center text-gray-400">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    </div>
                    <div>
                      <p class="text-[9px] font-black uppercase tracking-widest text-gray-400">Teléfono</p>
                      <p class="font-bold text-gray-900">{{ cliente.data.phone || 'No registrado' }}</p>
                    </div>
                  </div>
                  
                  <div class="flex items-center gap-3 text-gray-500">
                    <div class="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center text-gray-400">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                    </div>
                    <div>
                      <p class="text-[9px] font-black uppercase tracking-widest text-gray-400">Email</p>
                      <p class="font-bold text-gray-900 truncate max-w-[200px]">{{ cliente.data.email || 'No registrado' }}</p>
                    </div>
                  </div>

                  <div class="flex items-center gap-3 text-gray-500">
                    <div class="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center text-gray-400">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                    </div>
                    <div>
                      <p class="text-[9px] font-black uppercase tracking-widest text-gray-400">DNI / RUC</p>
                      <p class="font-bold text-gray-900">{{ cliente.data.dni_ruc || '---' }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Alergias en Cabecera (SI TIENE) -->
            <div v-if="cliente.data.alergias" class="mt-8 p-4 bg-red-50 border-2 border-red-100 rounded-2xl flex items-center gap-4 animate-pulse">
              <div class="w-12 h-12 bg-red-500 text-white rounded-xl flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
              </div>
              <div>
                <p class="text-[10px] font-black uppercase tracking-[0.2em] text-red-600">Alerta de Alergias</p>
                <p class="text-lg font-black text-red-700 uppercase tracking-tight">{{ cliente.data.alergias }}</p>
              </div>
            </div>
          </div>

          <!-- Estadísticas y Dashboard -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="bg-white p-6 rounded-[2rem] border border-gray-100 shadow-sm flex flex-col items-center justify-center text-center group hover:border-intimar-primary transition-all">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">Total Reservas</p>
              <p class="text-4xl font-black text-gray-900 group-hover:scale-110 transition-transform">{{ reservas.data?.length || 0 }}</p>
            </div>
            <div class="bg-white p-6 rounded-[2rem] border border-gray-100 shadow-sm flex flex-col items-center justify-center text-center">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">Asistencias</p>
              <p class="text-4xl font-black text-green-600">{{ attendanceStats.attended }}</p>
            </div>
            <div class="bg-white p-6 rounded-[2rem] border border-gray-100 shadow-sm flex flex-col items-center justify-center text-center">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">Inasistencias</p>
              <p class="text-4xl font-black text-red-600">{{ attendanceStats.noShows }}</p>
            </div>
            <div class="bg-white p-6 rounded-[2rem] border border-gray-100 shadow-sm flex flex-col items-center justify-center text-center relative overflow-hidden group">
              <div class="absolute inset-0 bg-intimar-primary/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 relative z-10">Nivel de Confianza</p>
              <p class="text-xl font-black uppercase tracking-tighter relative z-10" :class="getConfidenceClass(attendanceStats.rate)">
                {{ attendanceStats.level }}
              </p>
              <div class="flex gap-1 mt-2 relative z-10">
                <div v-for="i in 5" :key="i" class="w-2.5 h-1 rounded-full" :class="i <= (attendanceStats.rate / 20) ? getConfidenceBg(attendanceStats.rate) : 'bg-gray-100'"></div>
              </div>
            </div>
          </div>

          <!-- Contenido Principal (Tabs) -->
          <div class="bg-white rounded-[3rem] shadow-xl border border-gray-100 overflow-hidden">
            <div class="flex border-b border-gray-50">
              <button 
                v-for="tab in ['Historial', 'Preferencias']" 
                :key="tab"
                @click="activeTab = tab"
                :class="[
                  'flex-1 py-6 text-[10px] font-black uppercase tracking-[0.3em] transition-all',
                  activeTab === tab ? 'text-intimar-primary bg-gray-50 border-b-4 border-intimar-primary' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                {{ tab }}
              </button>
            </div>

            <div class="p-8 md:p-12">
              <!-- Tab: Historial -->
              <div v-if="activeTab === 'Historial'" class="space-y-6">
                <div v-if="reservas.loading" class="py-10 flex justify-center"><LoadingIndicator class="w-8 h-8 text-intimar-primary" /></div>
                <div v-else-if="!reservas.data?.length" class="py-12 text-center">
                  <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto mb-4 text-gray-300">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/></svg>
                  </div>
                  <p class="text-gray-400 font-bold uppercase tracking-widest text-[10px]">Sin historial de reservas registrado</p>
                </div>
                
                <div v-else class="space-y-4">
                  <router-link 
                    v-for="res in reservas.data" 
                    :key="res.name" 
                    :to="{ name: 'EditarReserva', params: { name: res.name } }"
                    class="flex flex-col md:flex-row md:items-center justify-between p-6 bg-gray-50 rounded-3xl border border-transparent hover:border-intimar-primary/20 hover:bg-white hover:shadow-lg transition-all group cursor-pointer"
                  >
                    <div class="flex items-center gap-6">
                      <div class="w-14 h-14 bg-white rounded-2xl flex flex-col items-center justify-center shadow-sm">
                        <span class="text-[8px] font-black text-gray-400 uppercase tracking-tighter">{{ formatMonth(res.fecha_reserva) }}</span>
                        <span class="text-xl font-black text-gray-900">{{ formatDay(res.fecha_reserva) }}</span>
                      </div>
                      <div>
                        <div class="flex items-center gap-3 mb-1">
                          <p class="font-black text-gray-900 uppercase tracking-tighter text-lg">{{ res.hora_reserva.substring(0,5) }}</p>
                          <span :class="getStatusClass(res.estado_reserva)" class="px-3 py-0.5 rounded-full text-[8px] font-black uppercase tracking-widest border">
                            {{ res.estado_reserva }}
                          </span>
                        </div>
                        <div class="flex items-center gap-4 text-[10px] font-bold text-gray-500 uppercase tracking-widest">
                          <span class="flex items-center gap-1.5">
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                            {{ res.cant_adultos + res.cant_ninos }} PERS.
                          </span>
                          <span v-if="res.mozo_nombre" class="flex items-center gap-1.5">
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="5"/><path d="M3 21v-2a7 7 0 0 1 7-7h4a7 7 0 0 1 7 7v2"/></svg>
                            MOZO: {{ res.mozo_nombre }}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="mt-4 md:mt-0 flex items-center gap-4">
                      <div class="text-right">
                        <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest">Mesa(s)</p>
                        <p v-if="res.mesas_asignadas" class="font-black text-intimar-primary text-xs uppercase tracking-tighter">{{ res.mesas_asignadas }}</p>
                        <p v-else class="font-black text-gray-300 italic text-sm">Pendiente</p>
                      </div>
                      <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center text-gray-300 group-hover:text-intimar-primary transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
                      </div>
                    </div>
                  </router-link>
                </div>
              </div>

              <!-- Tab: Preferencias -->
              <div v-if="activeTab === 'Preferencias'" class="space-y-10">
                <div>
                  <h4 class="text-[10px] font-black uppercase tracking-[0.3em] text-intimar-gold mb-6 flex items-center gap-2">
                    <span class="w-8 h-[2px] bg-intimar-gold/30"></span>
                    Salud y Restricciones
                  </h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="bg-red-50/30 p-6 rounded-3xl border border-red-100/50">
                      <p class="text-[9px] font-black uppercase tracking-widest text-red-400 mb-3">Alergias Conocidas</p>
                      <p class="text-xl font-black text-red-700 uppercase tracking-tight">{{ cliente.data.alergias || 'Sin alergias registradas' }}</p>
                    </div>
                    <div class="bg-gray-50 p-6 rounded-3xl border border-gray-100">
                      <p class="text-[9px] font-black uppercase tracking-widest text-gray-400 mb-3">Fecha de Nacimiento</p>
                      <p class="text-xl font-black text-gray-900 uppercase tracking-tight">{{ cliente.data.fecha_nacimiento || 'No registrada' }}</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 class="text-[10px] font-black uppercase tracking-[0.3em] text-intimar-primary mb-6 flex items-center gap-2">
                    <span class="w-8 h-[2px] bg-intimar-primary/30"></span>
                    Notas Internas
                  </h4>
                  <div class="bg-gray-50 p-8 rounded-3xl border border-gray-100 italic text-gray-600 font-medium leading-relaxed">
                    {{ cliente.data.observaciones || 'No hay notas u observaciones adicionales para este cliente.' }}
                  </div>
                </div>

                <div>
                  <h4 class="text-[10px] font-black uppercase tracking-[0.3em] text-gray-400 mb-6 flex items-center gap-2">
                    <span class="w-8 h-[2px] bg-gray-200"></span>
                    Información de Envío / Ubicación
                  </h4>
                  <div class="flex items-start gap-4">
                    <div class="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-sm text-gray-400 border border-gray-100">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                    </div>
                    <p class="text-gray-900 font-bold text-lg leading-tight">{{ cliente.data.direccion || 'Dirección no especificada' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="py-20 text-center">
          <p class="text-gray-500 font-black uppercase tracking-widest">No se encontró la información del cliente.</p>
        </div>
      </div>
    </div>

    <!-- Modal de Edición -->
    <Teleport to="body">
      <div v-if="showEditModal" class="fixed inset-0 z-[999] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-md" @click="showEditModal = false"></div>
        <div class="bg-white w-full max-w-lg rounded-[3rem] shadow-2xl relative z-10 overflow-hidden border border-gray-100 animate-in fade-in zoom-in duration-300">
          <div class="p-8 pb-4 border-b border-gray-50 flex justify-between items-center bg-gray-50/50">
            <h3 class="text-xl font-black text-gray-900 uppercase tracking-tighter">Editar Perfil</h3>
            <button @click="showEditModal = false" class="text-gray-400 hover:text-gray-900 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <div class="p-8 space-y-6 max-h-[60vh] overflow-y-auto custom-scrollbar">
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">DNI / RUC</label>
              <input v-model="form.dni_ruc" type="text" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Nombre</label>
                <input v-model="form.name1" type="text" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
              </div>
              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Apellido</label>
                <input v-model="form.lastname" type="text" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
              </div>
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Teléfono</label>
              <vue-tel-input 
                v-model="form.phone" 
                @on-input="onPhoneInput"
                v-bind="telInputOptions"
                class="bg-gray-50 border-2 border-transparent rounded-2xl focus-within:bg-white focus-within:border-intimar-primary transition-all font-bold"
              ></vue-tel-input>
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Email</label>
              <input v-model="form.email" type="email" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold" placeholder="cliente@correo.com">
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Dirección</label>
              <textarea v-model="form.direccion" rows="2" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold text-sm resize-none"></textarea>
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block text-red-500">⚠️ Alergias Críticas</label>
              <input v-model="form.alergias" type="text" class="w-full px-6 py-4 bg-red-50/30 border-2 border-transparent rounded-2xl focus:bg-white focus:border-red-500 outline-none transition-all font-bold text-red-700">
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Observaciones / Notas</label>
              <textarea v-model="form.observaciones" rows="3" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold text-sm resize-none"></textarea>
            </div>
          </div>

          <div class="p-8 pt-4 bg-gray-50/50 border-t border-gray-50 flex gap-4">
            <Button variant="outline" class="flex-1 py-6 rounded-2xl font-black uppercase tracking-widest text-xs" @click="showEditModal = false">Cancelar</Button>
            <Button variant="solid" class="flex-1 bg-intimar-primary text-white py-6 rounded-2xl font-black uppercase tracking-widest text-xs shadow-lg shadow-intimar-primary/20" @click="saveChanges" :loading="saving">Guardar Cambios</Button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import { createResource, LoadingIndicator, Button, call } from 'frappe-ui'
import Sidebar from '@/components/Sidebar.vue'
import { VueTelInput } from 'vue-tel-input'
import 'vue-tel-input/vue-tel-input.css'

const route = useRoute()
const activeTab = ref('Historial')
const showEditModal = ref(false)
const saving = ref(false)

const form = reactive({
  name1: '',
  lastname: '',
  dni_ruc: '',
  country_code: '+51',
  phone: '',
  direccion: '',
  alergias: '',
  observaciones: '',
  email: '',
  fullPhone: ''
})

const telInputOptions = {
  mode: 'international',
  dropdownOptions: { showFlags: true, showDialCodeInSelection: true },
  inputOptions: { placeholder: '987 654 321', showDialCode: false },
  autoDefaultCountry: true
}

const onPhoneInput = (phone, phoneObject) => {
  if (phoneObject && phoneObject.number) {
    form.fullPhone = phoneObject.number
  }
}

// Obtener datos del Cliente
const cliente = createResource({
  url: 'frappe.client.get',
  params: {
    doctype: 'Cliente Intimar',
    name: route.params.name
  },
  auto: true
})

// Obtener historial de Reservas
const reservas = createResource({
  url: 'intimar_erp.api.get_reservas_list',
  params: {
    filters: { cliente: route.params.name },
    limit_page_length: 50
  },
  auto: true
})

const openEditModal = () => {
  if (!cliente.data) return
  form.name1 = cliente.data.name1
  form.lastname = cliente.data.lastname
  form.dni_ruc = cliente.data.dni_ruc
  form.direccion = cliente.data.direccion
  form.alergias = cliente.data.alergias
  form.observaciones = cliente.data.observaciones
  form.email = cliente.data.email
  
  form.phone = cliente.data.phone || ''
  form.fullPhone = cliente.data.phone || ''
  showEditModal.value = true
}

const saveChanges = async () => {
  saving.value = true
  try {
    const finalPhone = form.fullPhone || form.phone.replace(/\s/g, '')
    await call('frappe.client.set_value', {
      doctype: 'Cliente Intimar',
      name: route.params.name,
      fieldname: {
        name1: form.name1,
        lastname: form.lastname,
        dni_ruc: form.dni_ruc,
        phone: finalPhone,
        direccion: form.direccion,
        alergias: form.alergias,
        observaciones: form.observaciones,
        email: form.email
      }
    })
    await cliente.reload()
    showEditModal.value = false
  } catch (e) {
    console.error(e)
    alert('Error al actualizar datos')
  } finally {
    saving.value = false
  }
}

// Estadísticas de Asistencia con Lógica Automática
const attendanceStats = computed(() => {
  if (!reservas.data || reservas.data.length === 0) return { attended: 0, noShows: 0, rate: 0, level: 'Sin Datos' }
  
  const today = new Date().toISOString().split('T')[0]
  const total = reservas.data.length
  
  // Asistencias: Solo cuando realmente vinieron
  const attended = reservas.data.filter(r => ['Finalizada', 'En proceso'].includes(r.estado_reserva)).length
  
  // Inasistencias: Cancelaciones manuales + Reservas pasadas no atendidas
  const noShows = reservas.data.filter(r => {
    const isCancelled = r.estado_reserva === 'Cancelada'
    const isPast = r.fecha_reserva < today
    const wasNotAttended = ['Solicitud de reserva', 'Confirmada', 'Lista de espera', 'Atrasada'].includes(r.estado_reserva)
    return isCancelled || (isPast && wasNotAttended)
  }).length
  
  // Ratio de cumplimiento
  const rate = (attended + noShows) > 0 ? Math.round((attended / (attended + noShows)) * 100) : 100
  
  let level = 'Estándar'
  if (rate >= 90 && total >= 3) level = 'Premium VIP'
  else if (rate >= 80) level = 'Muy Confiable'
  else if (rate < 50) level = 'Riesgoso'
  else if (total < 2) level = 'Cliente Nuevo'

  return { attended, noShows, rate, level }
})

const getConfidenceClass = (rate) => {
  if (rate >= 90) return 'text-emerald-600'
  if (rate >= 70) return 'text-intimar-primary'
  if (rate >= 50) return 'text-intimar-gold'
  return 'text-red-600'
}

const getConfidenceBg = (rate) => {
  if (rate >= 90) return 'bg-emerald-500'
  if (rate >= 70) return 'bg-intimar-primary'
  if (rate >= 50) return 'bg-intimar-gold'
  return 'bg-red-500'
}

// Formateadores de fecha
const formatMonth = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr + 'T12:00:00')
  return date.toLocaleString('es-ES', { month: 'short' }).toUpperCase().replace('.', '')
}

const formatDay = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.split('-')[2]
}

const getStatusClass = (status) => {
  const map = {
    'Solicitud de reserva': 'bg-blue-50 text-blue-600 border-blue-100',
    'Confirmada': 'bg-green-50 text-green-600 border-green-100',
    'En proceso': 'bg-orange-50 text-orange-600 border-orange-100',
    'Finalizada': 'bg-gray-50 text-gray-600 border-gray-100',
    'Cancelada': 'bg-red-50 text-red-600 border-red-100',
    'Atrasada': 'bg-rose-50 text-rose-600 border-rose-100',
    'Lista de espera': 'bg-purple-50 text-purple-600 border-purple-100'
  }
  return map[status] || 'bg-gray-50 text-gray-400 border-gray-100'
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}
.italic { font-style: italic; }
</style>
