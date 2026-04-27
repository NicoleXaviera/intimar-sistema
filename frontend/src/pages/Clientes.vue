<template>
  <div class="min-h-screen bg-gray-50 flex">
    <Sidebar />

    <div class="flex-1 p-6 md:p-12 pb-32 md:pb-12 overflow-y-auto font-sans">
      <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
          <div class="flex items-center gap-4">
            <img :src="'/files/intimar-logo.png'" alt="Logo" class="h-10 w-auto" />
            <div>
              <h1 class="text-3xl font-black text-gray-900 tracking-tight italic">Directorio de Clientes</h1>
              <p class="text-gray-500 font-bold uppercase tracking-widest text-[10px] mt-1">Gestión de Comensales</p>
            </div>
          </div>
          <Button 
            variant="solid" 
            class="bg-intimar-primary hover:bg-[#007a77] text-white px-8 py-6 rounded-2xl shadow-xl shadow-intimar-primary/20 font-black uppercase tracking-widest text-xs transition-all transform hover:scale-[1.03] flex items-center gap-3"
            @click="showCreateModal = true"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            NUEVO CLIENTE
          </Button>
        </div>

        <!-- Controles de Vista y Búsqueda -->
        <div class="flex flex-col md:flex-row gap-6 mb-8 items-end">
          <div class="flex-1 w-full">
            <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block">Búsqueda de Comensales</label>
            <div class="relative group">
              <svg class="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-intimar-primary transition-colors" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Nombre, DNI, Teléfono o Alergia..." 
                class="w-full pl-14 pr-6 py-5 bg-white border border-gray-100 rounded-[1.5rem] shadow-sm focus:ring-4 focus:ring-intimar-primary/5 focus:border-intimar-primary outline-none transition-all font-bold text-sm"
              >
            </div>
          </div>
          
          <div class="flex bg-white p-1.5 rounded-[1.5rem] border border-gray-100 shadow-sm h-[68px] items-center">
            <button 
              @click="viewType = 'cards'"
              :class="[
                'px-6 py-3 rounded-xl flex items-center gap-3 transition-all font-black text-[10px] uppercase tracking-[0.2em]',
                viewType === 'cards' ? 'bg-intimar-primary text-white shadow-lg shadow-intimar-primary/20' : 'text-gray-400 hover:text-gray-600'
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>
              Tarjetas
            </button>
            <button 
              @click="viewType = 'table'"
              :class="[
                'px-6 py-3 rounded-xl flex items-center gap-3 transition-all font-black text-[10px] uppercase tracking-[0.2em]',
                viewType === 'table' ? 'bg-intimar-primary text-white shadow-lg shadow-intimar-primary/20' : 'text-gray-400 hover:text-gray-600'
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
              Tabla Pro
            </button>
          </div>
        </div>

        <!-- Lista de Clientes -->
        <div v-if="clientes.loading" class="py-20 flex justify-center"><LoadingIndicator class="w-10 h-10 text-intimar-primary" /></div>
        
        <div v-else>
          <!-- Vista de Tabla (PRO) -->
          <div v-if="viewType === 'table'" class="bg-white rounded-[2.5rem] shadow-xl border border-gray-100 overflow-hidden animate-in fade-in duration-500">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-gray-50/50 border-b border-gray-100">
                    <th class="p-6 text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Comensal</th>
                    <th class="p-6 text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Contacto</th>
                    <th class="p-6 text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Acciones</th>
                  </tr>
                  <!-- Fila de Filtros por Columna -->
                  <tr class="bg-white border-b border-gray-50">
                    <td class="px-6 py-2">
                      <input v-model="colFilters.name" type="text" placeholder="Filtrar nombre..." class="w-full bg-gray-50 border-none rounded-lg px-3 py-2 text-[10px] font-bold focus:ring-1 focus:ring-intimar-primary outline-none">
                    </td>
                    <td class="px-6 py-2">
                      <input v-model="colFilters.phone" type="text" placeholder="Filtrar contacto..." class="w-full bg-gray-50 border-none rounded-lg px-3 py-2 text-[10px] font-bold focus:ring-1 focus:ring-intimar-primary outline-none">
                    </td>
                    <td class="px-6 py-2 text-center text-gray-300">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="mx-auto"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="2" y1="14" x2="6" y2="14"/><line x1="10" y1="12" x2="14" y2="12"/><line x1="18" y1="16" x2="22" y2="16"/></svg>
                    </td>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                  <tr v-for="cliente in filteredClientes" :key="cliente.name" class="hover:bg-intimar-primary/[0.02] transition-colors group">
                    <td class="p-6">
                      <div class="flex items-center gap-4">
                        <div class="w-12 h-12 bg-gray-100 text-gray-400 rounded-2xl flex items-center justify-center font-black text-xs group-hover:bg-intimar-primary group-hover:text-white transition-all">
                          {{ cliente.name1?.[0] }}{{ cliente.lastname?.[0] }}
                        </div>
                        <div>
                          <p class="font-black text-gray-900 uppercase tracking-tighter text-sm italic">{{ cliente.nombre_y_apellido_completo }}</p>
                          <p class="text-[9px] font-bold text-gray-400 uppercase tracking-widest mt-0.5">Cliente Frecuente</p>
                        </div>
                      </div>
                    </td>
                    <td class="p-6">
                      <div class="flex flex-col gap-1">
                        <p class="text-xs font-bold text-gray-900">{{ cliente.phone || '---' }}</p>
                        <p class="text-[10px] font-medium text-gray-400">{{ cliente.email || '---' }}</p>
                      </div>
                    </td>
                    <td class="p-6">
                      <div class="flex items-center gap-2">
                        <router-link 
                          :to="`/clientes/${cliente.name}`"
                          title="Ver Perfil"
                          class="p-3 bg-gray-50 text-gray-400 hover:text-intimar-primary hover:bg-white rounded-xl border border-transparent hover:border-intimar-primary/20 transition-all shadow-sm"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                        </router-link>
                        <button 
                          @click="editCliente(cliente)"
                          title="Editar"
                          class="p-3 bg-gray-50 text-gray-400 hover:text-intimar-gold hover:bg-white rounded-xl border border-transparent hover:border-intimar-gold/20 transition-all shadow-sm"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>
                        </button>
                        <button 
                          @click="deleteCliente(cliente)"
                          title="Eliminar"
                          class="p-3 bg-gray-50 text-gray-400 hover:text-red-500 hover:bg-white rounded-xl border border-transparent hover:border-red-500/20 transition-all shadow-sm"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Vista de Tarjetas -->
          <div v-else-if="viewType === 'cards'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in fade-in duration-500">
            <div v-for="cliente in filteredClientes" :key="cliente.name" class="bg-white p-6 rounded-[2.5rem] shadow-sm border border-gray-100 hover:shadow-xl hover:border-intimar-gold/30 transition-all group relative overflow-hidden">
              <!-- Decoración -->
              <div class="absolute top-0 right-0 w-24 h-24 bg-gray-50 rounded-bl-[4rem] -mr-8 -mt-8 group-hover:bg-intimar-gold/5 transition-colors"></div>
              
              <div class="relative z-10">
                <div class="flex items-center gap-4 mb-6">
                  <div class="w-14 h-14 bg-intimar-primary/10 rounded-2xl flex items-center justify-center text-intimar-primary font-black text-xl uppercase">
                    {{ cliente.name1?.[0] }}{{ cliente.lastname?.[0] }}
                  </div>
                  <div>
                    <h3 class="font-black text-gray-900 leading-tight uppercase tracking-tighter">{{ cliente.nombre_y_apellido_completo }}</h3>
                    <div class="flex items-center gap-2 mt-1">
                      <p class="text-[10px] font-black text-intimar-gold uppercase tracking-widest">ID: {{ cliente.dni_ruc || '---' }}</p>
                      <span class="w-1 h-1 bg-gray-300 rounded-full"></span>
                      <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest italic">Cliente Frecuente</p>
                    </div>
                  </div>
                </div>

                <div class="flex flex-wrap gap-2 mb-6">
                  <div v-if="cliente.alergias" class="bg-red-50 text-red-600 px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest flex items-center gap-2 border border-red-100 mb-2 w-full">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
                    ALERGIAS: {{ cliente.alergias }}
                  </div>
                  <div class="flex items-center gap-3 text-gray-500 w-full">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    <span class="text-xs font-bold">{{ cliente.phone || 'Sin teléfono' }}</span>
                  </div>
                  <div class="flex items-center gap-3 text-gray-500 w-full">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                    <span class="text-xs font-bold truncate max-w-[180px]">{{ cliente.email || 'Sin correo' }}</span>
                  </div>
                </div>

                <div class="flex gap-2">
                  <router-link 
                    :to="`/clientes/${cliente.name}`"
                    class="flex-1 py-4 rounded-xl border border-gray-100 bg-gray-50 text-center text-gray-500 hover:border-intimar-primary hover:text-intimar-primary hover:bg-white transition-all font-black uppercase text-[10px] tracking-widest flex items-center justify-center"
                  >
                    VER PERFIL
                  </router-link>
                  <Button 
                    variant="outline" 
                    class="w-12 h-12 p-0 flex items-center justify-center rounded-xl border-gray-100 hover:border-red-500 hover:text-red-500 transition-all"
                    @click="deleteCliente(cliente)"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Paginación Compacta -->
        <div v-if="!clientes.loading && filteredClientes && filteredClientes.length > 0" class="mt-4 flex flex-col sm:flex-row justify-between items-center gap-4 px-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
            Mostrando {{ filteredClientes.length }} registros
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
              :disabled="!filteredClientes || filteredClientes.length < pageSize"
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

    <!-- Modal de Crear/Editar (REFORZADO) -->
    <Teleport to="body">
      <div v-if="showCreateModal" class="fixed inset-0 z-[999] flex items-center justify-center p-4">
        <!-- Backdrop con Desenfoque -->
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-md" @click="showCreateModal = false"></div>
        
        <!-- Contenedor del Modal -->
        <div class="bg-white w-full max-w-lg rounded-[3rem] shadow-2xl relative z-10 overflow-hidden border border-gray-100 animate-in fade-in zoom-in duration-300">
          <!-- Header del Modal -->
          <div class="p-8 pb-4 border-b border-gray-50 flex justify-between items-center bg-gray-50/50">
            <h3 class="text-xl font-black text-gray-900 uppercase tracking-tighter">{{ editingCliente ? 'Editar Cliente' : 'Nuevo Cliente' }}</h3>
            <button @click="showCreateModal = false" class="text-gray-400 hover:text-gray-900 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <!-- Cuerpo del Modal -->
          <div class="p-8 space-y-6 max-h-[60vh] overflow-y-auto custom-scrollbar">
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block font-black">DNI / RUC / Pasaporte</label>
              <input v-model="form.dni_ruc" type="text" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold" placeholder="Número de documento">
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block font-black">Nombre</label>
                <input v-model="form.name1" type="text" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
              </div>
              <div>
                <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block font-black">Apellido</label>
                <input v-model="form.lastname" type="text" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold">
              </div>
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block font-black">Teléfono</label>
              <div class="flex gap-2">
                <select v-model="form.country_code" class="w-24 px-2 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-black text-sm appearance-none text-center">
                  <option value="+51">🇵🇪 +51</option>
                  <option value="+1">🇺🇸 +1</option>
                  <option value="+52">🇲🇽 +52</option>
                  <option value="+54">🇦🇷 +54</option>
                  <option value="+55">🇧🇷 +55</option>
                  <option value="+56">🇨🇱 +56</option>
                  <option value="+57">🇨🇴 +57</option>
                  <option value="+58">🇻🇪 +58</option>
                  <option value="+591">🇧🇴 +591</option>
                  <option value="+593">🇪🇨 +593</option>
                  <option value="+595">🇵🇾 +595</option>
                  <option value="+598">🇺🇾 +598</option>
                  <option value="+502">🇬🇹 +502</option>
                  <option value="+503">🇸🇻 +503</option>
                  <option value="+504">🇭🇳 +504</option>
                  <option value="+505">🇳🇮 +505</option>
                  <option value="+506">🇨🇷 +506</option>
                  <option value="+507">🇵🇦 +507</option>
                  <option value="+34">🇪🇸 +34</option>
                  <option value="+39">🇮🇹 +39</option>
                  <option value="+33">🇫🇷 +33</option>
                  <option value="+44">🇬🇧 +44</option>
                  <option value="+49">🇩🇪 +49</option>
                </select>
                <input v-model="form.phone" type="text" class="flex-1 px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold text-lg" placeholder="999 999 999">
              </div>
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block font-black">Correo Electrónico</label>
              <input v-model="form.email" type="email" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold" placeholder="cliente@correo.com">
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block font-black">Dirección</label>
              <textarea v-model="form.direccion" rows="2" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold text-sm resize-none" placeholder="Dirección completa..."></textarea>
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block font-black text-red-500">⚠️ Alergias Críticas</label>
              <input v-model="form.alergias" type="text" class="w-full px-6 py-4 bg-red-50/30 border-2 border-transparent rounded-2xl focus:bg-white focus:border-red-500 outline-none transition-all font-bold text-red-700" placeholder="Ej: Mariscos, Maní, Gluten...">
            </div>
            <div>
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 ml-2 mb-2 block font-black font-black text-gray-400 uppercase tracking-[0.2em]">Observaciones / Notas</label>
              <textarea v-model="form.observaciones" rows="3" class="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-intimar-primary outline-none transition-all font-bold text-sm resize-none" placeholder="Notas sobre el cliente..."></textarea>
            </div>
          </div>

          <!-- Acciones del Modal -->
          <div class="p-8 pt-4 bg-gray-50/50 border-t border-gray-50 flex gap-4">
            <Button variant="outline" class="flex-1 py-6 rounded-2xl font-black uppercase tracking-widest text-xs border-gray-200 hover:bg-white" @click="showCreateModal = false">Cancelar</Button>
            <Button 
              variant="solid" 
              class="flex-1 bg-intimar-primary hover:bg-[#007a77] text-white py-6 rounded-2xl font-black uppercase tracking-widest text-xs shadow-lg shadow-intimar-primary/20" 
              @click="saveCliente"
              :loading="saving"
            >
              {{ editingCliente ? 'GUARDAR CAMBIOS' : 'CREAR CLIENTE' }}
            </Button>
          </div>
        </div>
      </div>
    </Teleport>
    <!-- Modal de Eliminación (BONITO) -->
    <!-- Modal de Eliminación Personalizado -->
    <Teleport to="body">
      <div v-if="showDeleteDialog" class="fixed inset-0 z-[999] flex items-center justify-center p-4">
        <!-- Backdrop con Desenfoque -->
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-md transition-opacity" @click="!deleting && (showDeleteDialog = false)"></div>
        
        <!-- Contenedor del Modal -->
        <div class="bg-white w-full max-w-sm rounded-[3rem] shadow-2xl relative z-10 overflow-hidden border border-gray-100 animate-in fade-in zoom-in duration-300 text-center p-8">
          <div class="w-20 h-20 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
          </div>
          
          <h3 class="text-2xl font-black text-gray-900 mb-2 tracking-tight">¿Eliminar Cliente?</h3>
          <p class="text-gray-500 font-bold leading-relaxed mb-8">
            Estás a punto de eliminar a <span class="text-gray-900 font-black">{{ clienteToDelete?.nombre_y_apellido_completo }}</span>. 
            Esta acción no se puede deshacer.
          </p>
          
          <div class="flex flex-col gap-3">
            <Button 
              variant="solid" 
              class="w-full bg-red-500 hover:bg-red-600 text-white font-black uppercase tracking-widest text-[11px] py-6 rounded-2xl shadow-xl shadow-red-500/20 transition-all flex items-center justify-center gap-2"
              :loading="deleting"
              @click="confirmDelete"
            >
              ELIMINAR DEFINITIVAMENTE
            </Button>
            <button 
              class="w-full bg-gray-50 hover:bg-gray-100 text-gray-500 font-black uppercase tracking-widest text-[11px] py-5 rounded-2xl transition-all border border-gray-100"
              @click="showDeleteDialog = false"
              :disabled="deleting"
            >
              CANCELAR
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Notificación Toast Personalizada -->
    <Teleport to="body">
      <transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="transform translate-y-4 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform translate-y-4 opacity-0"
      >
        <div v-if="notification.show" 
             class="fixed bottom-6 right-6 z-[1000] px-6 py-4 rounded-2xl shadow-2xl font-bold flex items-center gap-3"
             :class="notification.type === 'success' ? 'bg-intimar-primary text-white' : 'bg-red-500 text-white'">
          
          <svg v-if="notification.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          
          {{ notification.message }}
        </div>
      </transition>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { Button, LoadingIndicator, createResource, call, Dialog } from 'frappe-ui'
import Sidebar from '@/components/Sidebar.vue'

const showCreateModal = ref(false)
const showDeleteDialog = ref(false)
const viewType = ref('table') // 'table' or 'cards'
const clienteToDelete = ref(null)
const editingCliente = ref(null)
const saving = ref(false)
const deleting = ref(false)
const notification = ref({ show: false, message: '', type: 'success' })

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}
const searchQuery = ref('')

const colFilters = reactive({
  name: '',
  dni: '',
  phone: '',
  alergias: ''
})

const form = reactive({
  name1: '',
  lastname: '',
  dni_ruc: '',
  country_code: '+51',
  phone: '',
  email: '',
  direccion: '',
  fecha_nacimiento: '',
  alergias: '',
  observaciones: ''
})

const currentPage = ref(1)
const pageSize = ref(20)

const buildFilters = () => {
  let f = {}
  if (colFilters.name) f['nombre_y_apellido_completo'] = ['like', `%${colFilters.name}%`]
  if (colFilters.dni) f['dni_ruc'] = ['like', `%${colFilters.dni}%`]
  if (colFilters.phone) f['phone'] = ['like', `%${colFilters.phone}%`]
  if (colFilters.alergias) f['alergias'] = ['like', `%${colFilters.alergias}%`]
  return f
}

const buildOrFilters = () => {
  let o_f = []
  if (searchQuery.value) {
     const q = `%${searchQuery.value}%`
     o_f.push(['nombre_y_apellido_completo', 'like', q])
     o_f.push(['email', 'like', q])
     o_f.push(['phone', 'like', q])
     o_f.push(['dni_ruc', 'like', q])
     o_f.push(['alergias', 'like', q])
  }
  return o_f.length ? o_f : undefined
}

const clientes = createResource({
  url: 'frappe.client.get_list',
  auto: false
})

const fetchClientes = () => {
  clientes.fetch({
    doctype: 'Cliente Intimar',
    fields: ['name', 'name1', 'lastname', 'phone', 'email', 'nombre_y_apellido_completo', 'dni_ruc', 'direccion', 'fecha_nacimiento', 'alergias', 'observaciones'],
    order_by: 'creation desc',
    limit_start: (currentPage.value - 1) * pageSize.value,
    limit_page_length: pageSize.value,
    filters: buildFilters(),
    or_filters: buildOrFilters()
  })
}

onMounted(() => fetchClientes())

watch([searchQuery, colFilters], () => {
  currentPage.value = 1
  fetchClientes()
}, { deep: true })

watch(currentPage, () => {
  fetchClientes()
})

const filteredClientes = computed(() => {
  return clientes.data || []
})

const editCliente = (cliente) => {
  editingCliente.value = cliente
  form.name1 = cliente.name1
  form.lastname = cliente.lastname
  form.dni_ruc = cliente.dni_ruc
  form.direccion = cliente.direccion
  form.fecha_nacimiento = cliente.fecha_nacimiento
  form.alergias = cliente.alergias
  form.observaciones = cliente.observaciones
  
  // Split phone into code and number
  const fullPhone = cliente.phone || ''
  const match = fullPhone.match(/^(\+\d+)\s*(.*)$/)
  if (match) {
    form.country_code = match[1]
    form.phone = match[2]
  } else {
    form.country_code = '+51'
    form.phone = fullPhone
  }
  
  form.email = cliente.email
  showCreateModal.value = true
}

const saveCliente = async () => {
  if (!form.name1) return showNotification('El nombre es obligatorio', 'error')
  
  saving.value = true
  try {
    const fullPhone = `${form.country_code} ${form.phone}`.trim()
    const isEdit = !!editingCliente.value
    
    if (isEdit) {
      await call('frappe.client.set_value', {
        doctype: 'Cliente Intimar',
        name: editingCliente.value.name,
        fieldname: {
          name1: form.name1,
          lastname: form.lastname,
          dni_ruc: form.dni_ruc,
          phone: fullPhone,
          email: form.email,
          direccion: form.direccion,
          fecha_nacimiento: form.fecha_nacimiento,
          alergias: form.alergias,
          observaciones: form.observaciones
        }
      })
    } else {
      await call('frappe.client.insert', {
        doc: {
          doctype: 'Cliente Intimar',
          name1: form.name1,
          lastname: form.lastname,
          dni_ruc: form.dni_ruc,
          phone: fullPhone,
          email: form.email,
          direccion: form.direccion,
          fecha_nacimiento: form.fecha_nacimiento,
          alergias: form.alergias,
          observaciones: form.observaciones
        }
      })
    }
    
    await fetchClientes()
    showCreateModal.value = false
    resetForm()
    showNotification(isEdit ? 'Cliente actualizado exitosamente' : 'Cliente creado exitosamente', 'success')
  } catch (e) {
    console.error(e)
    showNotification('Ocurrió un error al guardar', 'error')
  } finally {
    saving.value = false
  }
}

const deleteCliente = (cliente) => {
  clienteToDelete.value = cliente
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  if (!clienteToDelete.value) return
  
  deleting.value = true
  try {
    await call('frappe.client.delete', {
      doctype: 'Cliente Intimar',
      name: clienteToDelete.value.name
    })
    await fetchClientes()
    showDeleteDialog.value = false
    clienteToDelete.value = null
    showNotification('Cliente eliminado correctamente', 'success')
  } catch (e) {
    console.error(e)
    showNotification('No se pudo eliminar el cliente', 'error')
  } finally {
    deleting.value = false
  }
}

const resetForm = () => {
  editingCliente.value = null
  form.name1 = ''
  form.lastname = ''
  form.dni_ruc = ''
  form.country_code = '+51'
  form.phone = ''
  form.email = ''
  form.direccion = ''
  form.fecha_nacimiento = ''
  form.alergias = ''
  form.observaciones = ''
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
</style>
