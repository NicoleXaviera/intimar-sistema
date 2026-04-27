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

          <!-- Card: Reservas -->
          <div class="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 md:col-span-2">
            <h3 class="text-lg font-black text-gray-900 uppercase tracking-tighter mb-6 flex items-center gap-3">
              <span class="w-2 h-8 bg-intimar-bordeaux rounded-full"></span>
              Operación
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Aforo Máximo</label>
                <input v-model="formData.aforo_maximo" type="number" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
              </div>
              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Duración Reserva (Horas)</label>
                <input v-model="formData.duracion_reserva" type="number" step="0.5" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
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
const errorMessage = ref('')
const successMessage = ref('')
const formData = reactive({
  anticipo_persona: 0,
  monto_anticipo_persona: 0,
  duracion_reserva: 2,
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

