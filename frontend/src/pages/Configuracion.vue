<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />

    <div class="flex-1 p-6 md:p-12 pb-32 md:pb-12 overflow-y-auto">
      <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="flex items-center justify-between mb-10">
          <div class="flex items-center gap-4">
            <img :src="'/files/intimar-logo.png'" alt="Logo" class="h-10 w-auto" />
            <div>
              <h1 class="text-3xl font-black text-gray-900 tracking-tight italic">Configuración General</h1>
              <p class="text-gray-500 font-bold uppercase tracking-widest text-[10px] mt-1">Parámetros del Sistema</p>
            </div>
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
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 flex items-center gap-2">
                    Aforo Máximo
                    <button @click="showAforoGuide = true" class="w-5 h-5 bg-intimar-primary/10 text-intimar-primary rounded-full flex items-center justify-center hover:bg-intimar-primary hover:text-white transition-all transform active:scale-90">
                      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                    </button>
                  </label>
                  <input v-model="formData.aforo_maximo" type="number" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Duración Estándar (Horas)</label>
                  <input v-model="formData.duracion_reserva" type="number" step="0.5" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Duración Grupos >8 (Horas)</label>
                  <input v-model="formData.duracion_reserva_grande" type="number" step="0.5" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
                <div>
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Margen de Limpieza (Minutos)</label>
                  <input v-model="formData.margen_limpieza" type="number" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
                </div>
              </div>
            </div>

    <!-- MODAL: GUÍA DE AFORO (POPUP) -->
    <Teleport to="body">
      <transition name="modal-fade">
        <div v-if="showAforoGuide" class="fixed inset-0 z-[10000] flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-gray-900/80 backdrop-blur-md" @click="showAforoGuide = false"></div>
          <div class="relative bg-gray-900 text-white w-full max-w-3xl rounded-[3rem] shadow-2xl overflow-hidden border border-white/10 animate-scaleIn">
            <button @click="showAforoGuide = false" class="absolute top-8 right-8 w-10 h-10 bg-white/5 rounded-full flex items-center justify-center text-white/40 hover:text-white hover:bg-white/10 transition-all z-20">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>

            <div class="p-10 md:p-14 relative z-10">
              <div class="flex items-center gap-5 mb-10">
                <div class="w-16 h-16 bg-intimar-primary/20 text-intimar-primary rounded-[1.5rem] flex items-center justify-center shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                </div>
                <div>
                  <h3 class="text-3xl font-black italic tracking-tight text-white leading-tight">Lógica de Aforo</h3>
                  <p class="text-[10px] font-bold uppercase tracking-[0.4em] text-intimar-primary mt-1">Guía para el Administrador</p>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div class="space-y-8">
                  <div class="flex gap-5">
                    <span class="text-4xl font-black text-intimar-primary opacity-30 mt-1">01</span>
                    <div class="space-y-2">
                      <p class="font-black uppercase tracking-widest text-xs text-white">Tiempos Inteligentes</p>
                      <p class="text-sm text-gray-400 leading-relaxed">
                        El sistema distingue entre grupos: las mesas de <b class="text-white">más de 8 personas</b> tienen una duración mayor, ya que su estancia suele ser más larga.
                      </p>
                    </div>
                  </div>
                  <div class="flex gap-5">
                    <span class="text-4xl font-black text-intimar-primary opacity-30 mt-1">02</span>
                    <div class="space-y-2">
                      <p class="font-black uppercase tracking-widest text-xs text-white">Solapamiento Real</p>
                      <p class="text-sm text-gray-400 leading-relaxed">
                        Para saber el espacio libre a la 1 PM, el sistema suma a los que <b class="text-white">siguen comiendo</b> y a los que <b class="text-white">están por llegar</b> en ese instante exacto.
                      </p>
                    </div>
                  </div>
                </div>

                <div class="space-y-8">
                  <div class="flex gap-5">
                    <span class="text-4xl font-black text-intimar-primary opacity-30 mt-1">03</span>
                    <div class="space-y-2">
                      <p class="font-black uppercase tracking-widest text-xs text-white">Margen de Limpieza</p>
                      <p class="text-sm text-gray-400 leading-relaxed">
                         Cada reserva reserva automáticamente un <b class="text-white">tiempo de limpieza</b> al final, evitando que se junten clientes al entrar y salir.
                      </p>
                    </div>
                  </div>
                  <div class="flex gap-5">
                    <span class="text-4xl font-black text-intimar-primary opacity-30 mt-1">04</span>
                    <div class="space-y-2">
                      <p class="font-black uppercase tracking-widest text-xs text-white">Autoliberación</p>
                      <p class="text-sm text-gray-400 leading-relaxed">
                        A los <b class="text-white">20 min de retraso</b>, si no se marcó llegada ("En proceso"), el sistema libera el espacio para permitir nuevos registros.
                      </p>
                    </div>
                  </div>
                  <div class="bg-white/5 p-8 rounded-[2rem] border border-white/10 relative overflow-hidden group/card">
                    <div class="absolute top-0 right-0 p-4 opacity-10"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="m9 12 2 2 4-4"/></svg></div>
                    <p class="text-[10px] font-black uppercase tracking-widest text-intimar-gold mb-3">Consejo Operativo</p>
                    <p class="text-[13px] text-gray-300 italic leading-relaxed font-medium">
                      "Marcar <b>Finalizada</b> cuando un grupo se retira es clave para que el sistema libere la mesa de inmediato."
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
const formData = reactive({
  anticipo_persona: 0,
  monto_anticipo_persona: 0,
  duracion_reserva: 2,
  duracion_reserva_grande: 2.5,
  margen_limpieza: 15,
  aforo_maximo: 100,
  hora_minima: '09:00:00',
  hora_maxima: '22:00:00'
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
      formData.aforo_maximo = data.aforo_maximo || 100
      formData.hora_minima = data.hora_minima || '09:00:00'
      formData.hora_maxima = data.hora_maxima || '22:00:00'
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
        hora_minima: formData.hora_minima,
        hora_maxima: formData.hora_maxima
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

