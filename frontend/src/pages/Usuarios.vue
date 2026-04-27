<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />
    
    <div class="flex-1 p-4 pb-28 md:p-8 md:pb-8 flex flex-col h-screen overflow-hidden">
      <!-- Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <div>
          <div class="inline-flex items-center gap-2 bg-intimar-primary/10 text-intimar-primary px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest mb-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            Gestión Administrativa
          </div>
          <h1 class="text-4xl font-black text-gray-900 tracking-tight italic">Usuarios del Sistema</h1>
        </div>
        
        <button @click="showAddModal = true" class="bg-intimar-primary text-white px-8 py-4 rounded-[2rem] text-xs font-black uppercase tracking-[0.2em] shadow-xl shadow-intimar-primary/20 hover:scale-105 transition-all flex items-center gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Nuevo Usuario
        </button>
      </div>

      <!-- Tabla de Usuarios -->
      <div class="bg-white rounded-[3rem] shadow-sm border border-gray-100 flex-1 overflow-hidden flex flex-col">
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="border-b border-gray-50">
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Usuario</th>
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Roles</th>
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Estado</th>
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Última Conexión</th>
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="user in users" :key="user.name" class="group hover:bg-gray-50/50 transition-colors">
                <td class="px-8 py-6">
                  <div class="flex items-center gap-4">
                    <div class="w-12 h-12 bg-gray-100 rounded-2xl flex items-center justify-center text-gray-400 font-black overflow-hidden border-2 border-white shadow-sm">
                      <img v-if="user.user_image" :src="user.user_image" class="w-full h-full object-cover" />
                      <span v-else>{{ user.full_name ? user.full_name[0] : 'U' }}</span>
                    </div>
                    <div>
                      <div class="font-black text-gray-900 text-sm italic">{{ user.full_name }}</div>
                      <div class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{{ user.name }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-8 py-6">
                  <div class="flex flex-wrap gap-2">
                    <span v-for="role in (user.roles || '').split(',')" :key="role" class="bg-gray-100 text-gray-600 text-[9px] font-black uppercase tracking-widest px-2 py-1 rounded-lg">
                      {{ role }}
                    </span>
                    <span v-if="!user.roles" class="text-gray-300 italic text-[10px]">Sin roles</span>
                  </div>
                </td>
                <td class="px-8 py-6">
                  <div :class="[user.enabled ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600']" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
                    <span class="w-1.5 h-1.5 rounded-full" :class="[user.enabled ? 'bg-green-600' : 'bg-red-600']"></span>
                    {{ user.enabled ? 'Activo' : 'Inactivo' }}
                  </div>
                </td>
                <td class="px-8 py-6 text-xs font-bold text-gray-500 uppercase tracking-tighter">
                  {{ user.last_login ? formatDate(user.last_login) : 'Nunca' }}
                </td>
                <td class="px-8 py-6 text-right">
                  <div class="flex justify-end gap-2">
                    <button @click="editUser(user)" class="w-10 h-10 bg-gray-50 hover:bg-intimar-primary hover:text-white rounded-xl flex items-center justify-center text-gray-400 transition-all shadow-sm">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal: Nuevo/Editar Usuario -->
    <Teleport to="body">
      <div v-if="showAddModal" class="fixed inset-0 z-[200] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-md" @click="showAddModal = false"></div>
        
        <div class="relative bg-white w-full max-w-xl rounded-[3rem] shadow-2xl overflow-hidden animate-in zoom-in-95 duration-300">
          <div class="bg-intimar-primary p-8 text-white relative">
            <div class="absolute right-0 top-0 w-32 h-32 bg-white/10 rounded-full -mr-10 -mt-10 blur-2xl"></div>
            <h2 class="text-2xl font-black italic tracking-tight">{{ editingUser ? 'Editar Usuario' : 'Nuevo Usuario' }}</h2>
            <p class="text-[10px] font-black uppercase tracking-[0.2em] opacity-60">Configuración de acceso al sistema</p>
          </div>
          
          <form @submit.prevent="saveUser" class="p-8 space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Nombre Completo</label>
                <input v-model="form.full_name" type="text" required class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-gray-700 focus:ring-2 ring-intimar-primary transition-all" placeholder="Ej: Juan Perez" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Correo (ID)</label>
                <input v-model="form.email" type="email" required :disabled="editingUser" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-gray-700 focus:ring-2 ring-intimar-primary transition-all" placeholder="usuario@intimar.com" />
              </div>
              <div v-if="!editingUser" class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Contraseña Inicial</label>
                <input v-model="form.new_password" type="password" required class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-gray-700 focus:ring-2 ring-intimar-primary transition-all" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Estado</label>
                <select v-model="form.enabled" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-gray-700 focus:ring-2 ring-intimar-primary transition-all">
                  <option :value="1">Activo</option>
                  <option :value="0">Inactivo</option>
                </select>
              </div>
            </div>

            <div class="space-y-3">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Roles Asignados</label>
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
                <label v-for="role in availableRoles" :key="role" class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors">
                  <input type="checkbox" :value="role" v-model="form.selectedRoles" class="w-4 h-4 text-intimar-primary rounded focus:ring-intimar-primary border-none bg-white shadow-sm" />
                  <span class="text-[10px] font-black text-gray-600 uppercase tracking-tighter">{{ role }}</span>
                </label>
              </div>
            </div>

            <div class="pt-6 flex gap-4">
              <button type="button" @click="showAddModal = false" class="flex-1 px-8 py-4 bg-gray-50 text-gray-400 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-gray-100 transition-all">
                Cancelar
              </button>
              <button type="submit" :disabled="loading" class="flex-[2] px-8 py-4 bg-intimar-primary text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-intimar-dark transition-all shadow-xl shadow-intimar-primary/20 disabled:opacity-50">
                {{ loading ? 'Guardando...' : (editingUser ? 'Guardar Cambios' : 'Crear Usuario') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { call } from 'frappe-ui'
import Sidebar from '@/components/Sidebar.vue'

const users = ref([])
const showAddModal = ref(false)
const editingUser = ref(null)
const loading = ref(false)
const availableRoles = ['Administrator', 'System Manager', 'Reserva Manager', 'Mozo', 'Cajero']

const form = ref({
  full_name: '',
  email: '',
  new_password: '',
  enabled: 1,
  selectedRoles: []
})

const fetchUsers = async () => {
  try {
    // Obtenemos lista de usuarios con sus roles básicos
    const data = await call('frappe.client.get_list', {
      doctype: 'User',
      fields: ['name', 'full_name', 'user_image', 'enabled', 'last_login', 'creation'],
      order_by: 'creation desc'
    })
    
    // Para cada usuario, intentamos obtener sus roles de manera más detallada si es necesario
    // Pero por simplicidad en este MVP, usaremos get_doc para los roles al editar
    users.value = data
  } catch (e) {
    console.error(e)
  }
}

const saveUser = async () => {
  loading.value = true
  try {
    if (editingUser.value) {
      await call('intimar_erp.api.update_user_details', {
        user_id: form.value.email,
        full_name: form.value.full_name,
        enabled: form.value.enabled,
        roles: JSON.stringify(form.value.selectedRoles)
      })
    } else {
      await call('intimar_erp.api.create_new_user', {
        email: form.value.email,
        full_name: form.value.full_name,
        password: form.value.new_password,
        roles: JSON.stringify(form.value.selectedRoles)
      })
    }
    
    showAddModal.value = false
    await fetchUsers()
    resetForm()
  } catch (e) {
    alert('Error: ' + (e.message || 'No tienes permisos suficientes'))
  } finally {
    loading.value = false
  }
}

const editUser = async (user) => {
  editingUser.value = user
  try {
    const data = await call('intimar_erp.api.get_user_details', {
      user_id: user.name
    })
    form.value = {
      full_name: data.full_name || '',
      email: data.email || data.name,
      enabled: data.enabled,
      selectedRoles: data.roles || []
    }
    showAddModal.value = true
  } catch (e) {
    console.error('Error al cargar usuario:', e)
    alert('No se pudo cargar la información del usuario. Verifica tus permisos de Administrador.')
  }
}

const resetForm = () => {
  editingUser.value = null
  form.value = {
    full_name: '',
    email: '',
    new_password: '',
    enabled: 1,
    selectedRoles: []
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('es-ES', { 
    day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' 
  })
}

onMounted(() => {
  fetchUsers()
})
</script>
