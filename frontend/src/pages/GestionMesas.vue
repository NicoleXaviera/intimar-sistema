<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />

    <div class="flex-1 p-6 md:p-12 pb-32 md:pb-12 overflow-y-auto">
      <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-10 gap-6">
          <div class="flex items-center gap-4">
            <img :src="'/files/intimar-logo.png'" alt="Logo" class="h-10 w-auto" />
            <div>
              <h1 class="text-3xl font-black text-gray-900 tracking-tight italic">Gestión de Mesas</h1>
              <p class="text-gray-500 font-bold uppercase tracking-widest text-[10px] mt-1">Configuración del Salón</p>
            </div>
          </div>

          <Button 
            variant="solid" 
            class="bg-intimar-primary hover:bg-[#007a77] text-white px-8 py-6 rounded-2xl shadow-xl shadow-intimar-primary/20 font-black uppercase tracking-widest text-xs transition-all transform hover:scale-[1.03] active:scale-95"
            @click="openCreateModal"
          >
            + AÑADIR NUEVA MESA
          </Button>
        </div>

        <!-- FILTROS -->
        <div class="flex flex-col md:flex-row gap-4 mb-8 bg-white p-4 rounded-[2rem] shadow-sm border border-gray-100">
          <div class="flex-1 relative group">
            <svg class="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-intimar-primary transition-colors" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            <input 
              v-model="filterQuery"
              type="text" 
              placeholder="BUSCAR POR NÚMERO DE MESA..."
              class="w-full pl-14 pr-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary focus:ring-0 outline-none transition-all font-bold text-xs uppercase tracking-widest"
            >
          </div>
          <div class="md:w-64 relative group">
             <select 
              v-model="filterUbicacion"
              class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary focus:ring-0 outline-none transition-all font-bold text-xs uppercase tracking-widest appearance-none"
            >
              <option value="">TODAS LAS UBICACIONES</option>
              <option v-for="zona in zonas.data" :key="zona.name" :value="zona.name">{{ zona.name }}</option>
            </select>
            <svg class="absolute right-5 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
          </div>
        </div>

        <!-- Tabla de Mesas -->
        <div class="bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden">

          <div v-if="mesas.loading" class="py-20 flex justify-center"><LoadingIndicator class="w-10 h-10 text-intimar-primary" /></div>
          
          <table v-else class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-gray-50/50 border-b border-gray-100">
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 italic">Mesa</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 italic">Ubicación</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 italic text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="mesa in filteredMesas" :key="mesa.name" class="hover:bg-gray-50/50 transition-colors group">
                <td class="px-8 py-6">
                  <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-2xl bg-intimar-primary/5 flex items-center justify-center text-intimar-primary font-black italic text-xl group-hover:bg-intimar-primary group-hover:text-white transition-all shadow-sm">
                      {{ mesa.numero_mesa }}
                    </div>
                    <span class="font-black text-gray-900 tracking-tight">{{ mesa.name }}</span>
                  </div>
                </td>
                <td class="px-8 py-6">
                  <span class="inline-flex items-center px-4 py-1.5 rounded-full bg-gray-100 text-[10px] font-black uppercase tracking-widest text-gray-500">
                    {{ mesa.ubicacion_mesa }}
                  </span>
                </td>
                <td class="px-8 py-6 text-right">
                  <div class="flex justify-end gap-3">
                    <button 
                      @click="openEditModal(mesa)" 
                      class="p-3 text-gray-400 hover:text-intimar-primary hover:bg-intimar-primary/5 rounded-xl transition-all"
                      title="Editar"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
                    </button>
                    <button 
                      @click="confirmDelete(mesa)" 
                      class="p-3 text-gray-400 hover:text-intimar-red hover:bg-intimar-red/5 rounded-xl transition-all"
                      title="Eliminar"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación Compacta -->
        <div v-if="!mesas.loading && totalRecords > 0" class="mt-4 flex flex-col sm:flex-row justify-between items-center gap-4 px-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
            Mostrando {{ filteredMesas.length }} de {{ totalRecords }} registros
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
              PÁGINA {{ currentPage }} DE {{ totalPages }}
            </span>
            <button 
              :disabled="currentPage === totalPages"
              @click="currentPage++"
              class="text-gray-400 hover:text-intimar-primary disabled:opacity-30 disabled:hover:text-gray-400 transition-colors flex items-center p-1"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: CREAR/EDITAR MESA -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-[9999] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="showModal = false"></div>
        <div class="relative bg-white w-full max-w-md rounded-[2.5rem] shadow-2xl overflow-hidden animate-scaleIn">
          <div class="p-8">
            <h3 class="text-3xl font-black text-gray-900 italic tracking-tighter mb-8">
              {{ editingMesa ? 'Editar' : 'Nueva' }} <span class="text-intimar-primary">Mesa</span>
            </h3>

            <div class="space-y-6">
              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Número de Mesa</label>
                <input 
                  v-model="formData.numero_mesa"
                  type="number" 
                  class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary focus:ring-0 outline-none transition-all font-bold"
                >
              </div>

              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Ubicación</label>
                <select 
                  v-model="formData.ubicacion_mesa"
                  class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary focus:ring-0 outline-none transition-all font-bold appearance-none"
                >
                  <option value="" disabled>Seleccionar zona...</option>
                  <option v-for="zona in zonas.data" :key="zona.name" :value="zona.name">{{ zona.name }}</option>
                </select>
              </div>
            </div>
          </div>

          <div class="p-6 bg-gray-50 border-t border-gray-100 flex gap-4">
            <Button 
              class="flex-1 py-7 bg-intimar-primary hover:bg-[#007a77] text-white font-black rounded-2xl shadow-xl uppercase tracking-widest text-xs transition-all"
              @click="saveMesa" 
              :loading="saving"
            >
              {{ editingMesa ? 'GUARDAR CAMBIOS' : 'CREAR MESA' }}
            </Button>
            <Button 
              variant="ghost" 
              class="py-7 px-8 text-gray-400 font-black uppercase tracking-widest text-[10px] hover:text-gray-900" 
              @click="showModal = false"
            >
              CANCELAR
            </Button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { Button, LoadingIndicator, createResource } from 'frappe-ui'
import Sidebar from '@/components/Sidebar.vue'

const showModal = ref(false)
const editingMesa = ref(null)
const saving = ref(false)
const filterQuery = ref('')
const filterUbicacion = ref('')

// Pagination state
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize.value))

const formData = reactive({
  numero_mesa: '',
  ubicacion_mesa: ''
})

// RECURSOS
const mesas = createResource({
  url: 'intimar_erp.api.get_mesas_with_reserva',
  auto: false,
  onSuccess(data) {
    if (data && data.total_count !== undefined) {
      totalCount.value = data.total_count
    }
  }
})

const fetchMesas = () => {
  mesas.fetch({
    limit_start: (currentPage.value - 1) * pageSize.value,
    limit_page_length: pageSize.value,
    with_pagination: 1,
    search_query: filterQuery.value,
    ubicacion_mesa: filterUbicacion.value
  })
}

// Watchers for filters and pagination
import { watch, onMounted } from 'vue'

watch([filterQuery, filterUbicacion], () => {
  currentPage.value = 1 // Reset to page 1 when filters change
  fetchMesas()
})

watch(currentPage, () => {
  fetchMesas()
})

onMounted(() => {
  fetchMesas()
})


const zonas = createResource({
  url: 'intimar_erp.api.get_ubicaciones_mesas',
  auto: true
})

const filteredMesas = computed(() => {
  if (!mesas.data) return []
  return mesas.data.data || mesas.data
})

// ACCIONES
const openCreateModal = () => {
  editingMesa.value = null
  formData.numero_mesa = ''
  formData.ubicacion_mesa = ''
  showModal.value = true
}

const openEditModal = (mesa) => {
  editingMesa.value = mesa
  formData.numero_mesa = mesa.numero_mesa
  formData.ubicacion_mesa = mesa.ubicacion_mesa
  showModal.value = true
}

const saveMesa = async () => {
  saving.value = true
  try {
    if (editingMesa.value) {
      await createResource({
        url: 'frappe.client.set_value',
        params: {
          doctype: 'Mesa Intimar',
          name: editingMesa.value.name,
          fieldname: {
            numero_mesa: formData.numero_mesa,
            ubicacion_mesa: formData.ubicacion_mesa
          }
        }
      }).submit()
    } else {
      await createResource({
        url: 'frappe.client.insert',
        params: {
          doc: {
            doctype: 'Mesa Intimar',
            numero_mesa: formData.numero_mesa,
            ubicacion_mesa: formData.ubicacion_mesa
          }
        }
      }).submit()
    }
    await fetchMesas()
    showModal.value = false
  } finally {
    saving.value = false
  }
}

const confirmDelete = async (mesa) => {
  if (confirm(`¿Estás seguro de eliminar la mesa ${mesa.numero_mesa}?`)) {
    await createResource({
      url: 'frappe.client.delete',
      params: {
        doctype: 'Mesa Intimar',
        name: mesa.name
      }
    }).submit()
    await fetchMesas()
  }
}
</script>
