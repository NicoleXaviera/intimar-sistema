<template>
  <div class="bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden relative z-10">
    <div class="overflow-x-auto scrollbar-hide">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50/50 border-b border-gray-100 select-none">
            <th @click="toggleSort('name')" class="py-3 px-2 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] w-1 text-center cursor-pointer hover:bg-gray-50/80 hover:text-gray-600 transition-colors group">
              <div class="flex items-center justify-center gap-1">
                ID
                <span class="inline-flex align-middle text-gray-400">
                  <svg v-if="getSortDir('name') === 'asc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/></svg>
                  <svg v-else-if="getSortDir('name') === 'desc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/></svg>
                  <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/></svg>
                </span>
              </div>
            </th>
            <th v-if="columns.creacion" @click="toggleSort('creation')" class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] cursor-pointer hover:bg-gray-50/80 hover:text-gray-600 transition-colors group">
              <div class="flex items-center gap-1">
                Creación
                <span class="inline-flex align-middle text-gray-400">
                  <svg v-if="getSortDir('creation') === 'asc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/></svg>
                  <svg v-else-if="getSortDir('creation') === 'desc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/></svg>
                  <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/></svg>
                </span>
              </div>
            </th>
            <th v-if="columns.cliente" @click="toggleSort('nombre')" class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] cursor-pointer hover:bg-gray-50/80 hover:text-gray-600 transition-colors group">
              <div class="flex items-center gap-1">
                Cliente
                <span class="inline-flex align-middle text-gray-400">
                  <svg v-if="getSortDir('nombre') === 'asc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/></svg>
                  <svg v-else-if="getSortDir('nombre') === 'desc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/></svg>
                  <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/></svg>
                </span>
              </div>
            </th>
            <th v-if="columns.detalles" @click="toggleSort('fecha_reserva')" class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] cursor-pointer hover:bg-gray-50/80 hover:text-gray-600 transition-colors group">
              <div class="flex items-center gap-1">
                Detalles
                <span class="inline-flex align-middle text-gray-400">
                  <svg v-if="getSortDir('fecha_reserva') === 'asc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/></svg>
                  <svg v-else-if="getSortDir('fecha_reserva') === 'desc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/></svg>
                  <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/></svg>
                </span>
              </div>
            </th>
            <th v-if="columns.llegada" @click="toggleSort('hora_llegada')" class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] cursor-pointer hover:bg-gray-50/80 hover:text-gray-600 transition-colors group">
              <div class="flex items-center gap-1">
                Llegada
                <span class="inline-flex align-middle text-gray-400">
                  <svg v-if="getSortDir('hora_llegada') === 'asc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/></svg>
                  <svg v-else-if="getSortDir('hora_llegada') === 'desc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/></svg>
                  <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/></svg>
                </span>
              </div>
            </th>
            <th v-if="columns.salida" @click="toggleSort('hora_salida')" class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] cursor-pointer hover:bg-gray-50/80 hover:text-gray-600 transition-colors group">
              <div class="flex items-center gap-1">
                Salida
                <span class="inline-flex align-middle text-gray-400">
                  <svg v-if="getSortDir('hora_salida') === 'asc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/></svg>
                  <svg v-else-if="getSortDir('hora_salida') === 'desc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/></svg>
                  <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/></svg>
                </span>
              </div>
            </th>
            <th v-if="columns.pago" class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em]">Anticipo</th>
            <th v-if="columns.mesas" @click="toggleSort('mozo')" class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] cursor-pointer hover:bg-gray-50/80 hover:text-gray-600 transition-colors group">
              <div class="flex items-center gap-1">
                Asignación
                <span class="inline-flex align-middle text-gray-400">
                  <svg v-if="getSortDir('mozo') === 'asc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/></svg>
                  <svg v-else-if="getSortDir('mozo') === 'desc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/></svg>
                  <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/></svg>
                </span>
              </div>
            </th>
            <th v-if="columns.creacion" @click="toggleSort('creation')" class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] cursor-pointer hover:bg-gray-50/80 hover:text-gray-600 transition-colors group">
              <div class="flex items-center gap-1">
                Creación
                <span class="inline-flex align-middle text-gray-400">
                  <svg v-if="getSortDir('creation') === 'asc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/></svg>
                  <svg v-else-if="getSortDir('creation') === 'desc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/></svg>
                  <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/></svg>
                </span>
              </div>
            </th>
            <th v-if="columns.estado" @click="toggleSort('estado_reserva')" class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] cursor-pointer hover:bg-gray-50/80 hover:text-gray-600 transition-colors group">
              <div class="flex items-center gap-1">
                Estado
                <span class="inline-flex align-middle text-gray-400">
                  <svg v-if="getSortDir('estado_reserva') === 'asc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/></svg>
                  <svg v-else-if="getSortDir('estado_reserva') === 'desc'" class="w-3 h-3 text-intimar-gold" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/></svg>
                  <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/></svg>
                </span>
              </div>
            </th>
            <th class="py-3 px-4 font-black text-gray-400 text-[10px] uppercase tracking-[0.2em] text-right">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="loading" class="animate-pulse">
            <td colspan="8" class="p-8 text-center text-gray-400 font-bold">Cargando reservaciones...</td>
          </tr>
          <tr v-else-if="reservas.length === 0">
            <td colspan="8" class="p-12 text-center text-gray-400 font-bold">No hay reservaciones que coincidan con los filtros.</td>
          </tr>
          
          <tr 
            v-for="reserva in reservas" 
            :key="reserva.name"
            class="hover:bg-gray-50/50 transition-colors group"
          >
            <!-- ID -->
            <td class="px-2 py-2">
              <div class="bg-gray-100 text-gray-500 font-black text-[10px] py-1 px-2 rounded-md text-center tracking-tight inline-block w-full whitespace-nowrap">
                {{ reserva.name }}
              </div>
            </td>

            <!-- Fecha de Creación (OPCIONAL) -->
            <td v-if="columns.creacion" class="px-4 py-2">
              <div v-if="reserva.creation" class="flex flex-col gap-0.5">
                <span class="text-[11px] font-black text-gray-700 tracking-tight">{{ formatDate(reserva.creation) }}</span>
                <span class="text-[9px] font-bold text-gray-400 uppercase tracking-widest">{{ formatTime(reserva.creation.split(' ')[1]) }}</span>
              </div>
              <div v-else class="text-[10px] font-bold text-gray-300 italic">---</div>
            </td>

            <!-- Cliente -->
            <td v-if="columns.cliente" class="px-4 py-2">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-intimar-primary/10 rounded-lg flex items-center justify-center text-intimar-primary font-black text-xs uppercase">
                  {{ getInitials(reserva.nombre, reserva.apellido) }}
                </div>
                <div>
                  <h4 class="font-black text-gray-900 text-[13px] mb-0.5 flex items-center gap-2">
                    {{ reserva.nombre }} {{ reserva.apellido || '' }}
                    <span v-if="reserva.motivo_reserva?.includes('[WEB]')" class="bg-blue-100 text-blue-600 text-[8px] px-1.5 py-0.5 rounded-full tracking-tighter uppercase font-black">WEB</span>
                    <span v-else-if="reserva.motivo_reserva?.includes('[RÁPIDA]')" class="bg-amber-100 text-amber-700 text-[8px] px-1.5 py-0.5 rounded-full tracking-tighter uppercase font-black">RÁPIDA</span>
                    <span v-else class="bg-gray-100 text-gray-500 text-[8px] px-1.5 py-0.5 rounded-full tracking-tighter uppercase font-bold">INTERNA</span>
                  </h4>
                  <p v-if="columns.celular" class="text-[10px] font-bold text-gray-400 flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    {{ (session.hasRole(['Anfitriona', 'Vigilante']) && !session.isAdmin) ? '********' : (reserva.celular || 'Sin teléfono') }}
                  </p>
                </div>
              </div>
            </td>

            <!-- Detalles -->
            <td v-if="columns.detalles" class="px-4 py-2">
              <div class="flex flex-col gap-1">
                <div class="flex items-center gap-2">
                  <span class="bg-gray-100 text-gray-700 font-bold text-[11px] py-0.5 px-2 rounded flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                    {{ formatDate(reserva.fecha_reserva) }}
                  </span>
                  <span class="bg-intimar-gold/10 text-intimar-gold font-black text-[11px] py-0.5 px-2 rounded flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    {{ formatTime(reserva.hora_reserva) }}
                  </span>
                </div>
                <div class="text-[10px] font-bold text-gray-500 flex items-center gap-2 ml-0.5">
                  <span class="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    {{ reserva.cant_adultos || 0 }} Adul.
                  </span>
                  <span class="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
                    {{ reserva.cant_ninos || 0 }} Niñ.
                  </span>
                </div>
              </div>
            </td>

            <!-- Hora Llegada (OPCIONAL) -->
            <td v-if="columns.llegada" class="px-4 py-2">
              <div v-if="reserva.hora_llegada" class="flex flex-col gap-0.5">
                <span class="text-xs font-black text-gray-900 tracking-tight">{{ formatTime(reserva.hora_llegada) }}</span>
              </div>
              <div v-else class="text-[10px] font-bold text-gray-300 italic">Pendiente</div>
            </td>

            <!-- Hora Salida (OPCIONAL) -->
            <td v-if="columns.salida" class="px-4 py-2">
              <div v-if="reserva.hora_salida" class="flex flex-col gap-0.5">
                <span class="text-xs font-black text-gray-900 tracking-tight">{{ formatTime(reserva.hora_salida) }}</span>
              </div>
              <div v-else class="text-[10px] font-bold text-gray-300 italic">Pendiente</div>
            </td>

            <!-- Medio de Pago (OPCIONAL) -->
            <td v-if="columns.pago" class="px-4 py-2">
              <div v-if="reserva.anticipos?.length" class="flex flex-col gap-1.5">
                <div v-for="a in reserva.anticipos" :key="a.name" class="flex flex-col items-start leading-none">
                  <!-- Monto en texto elegante y bold -->
                  <span class="text-xs font-black text-gray-900 tracking-tight">
                    {{ a.moneda === 'PEN' ? 'S/' : (a.moneda === 'USD' ? '$' : a.moneda) }} {{ parseFloat(a.monto_anticipo).toFixed(2) }}
                  </span>
                  <!-- Pill de Banco y Operación abajo (muy compactos) -->
                  <div class="mt-1 flex items-center gap-1.5 leading-none">
                    <span :class="[getAnticipoBadgeClasses(a.banco), 'text-[8px] font-black py-0.25 px-1.5 rounded uppercase tracking-wider border leading-none']">
                      {{ a.banco || 'Pago' }}
                    </span>
                    <span v-if="a.nro_operacion" class="text-[8px] text-gray-400 font-bold tracking-tight">
                      #{{ a.nro_operacion }}
                    </span>
                  </div>
                </div>
              </div>
              <div v-else-if="reserva.anticipo_required" class="inline-flex items-center gap-1 bg-amber-50 text-amber-700 text-[9px] font-black py-0.5 px-2 rounded border border-amber-200 uppercase tracking-wider">
                <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                Sin registrar
              </div>
              <div v-else class="inline-flex items-center text-gray-300 text-[9px] font-bold uppercase tracking-wider">
                No requiere
              </div>
            </td>

            <!-- Asignación (OPCIONAL) -->
            <td v-if="columns.mesas" class="px-4 py-2">
              <!-- Mesas Asignadas (Badge/Texto arriba) -->
              <div v-if="reserva.mesas?.length" class="flex flex-wrap gap-1">
                <span v-for="m in reserva.mesas" :key="m.name" class="bg-intimar-primary/10 text-intimar-primary text-[10px] font-black py-0.5 px-2 rounded-lg border border-intimar-primary/20 uppercase tracking-wider flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M16 4l-4-4-4 4"/><path d="M12 0v16"/></svg>
                  {{ m.mesa }}
                </span>
              </div>
              <div v-else class="text-[10px] font-bold text-gray-400 italic">
                Sin mesa
              </div>
              
              <!-- Mozo (Chiquito abajo) -->
              <div class="mt-1 flex items-center gap-1 text-[10px] text-gray-500 font-bold">
                <svg xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                <span v-if="reserva.mozo" class="truncate max-w-[120px]">{{ reserva.mozo }}</span>
                <span v-else class="text-gray-300 italic">Sin mozo</span>
              </div>
            </td>

            <!-- Estado -->
            <td v-if="columns.estado" class="px-4 py-2">
              <span :class="getStatusClass(reserva.estado_reserva)" class="inline-flex items-center gap-1.5 py-1 px-2 rounded-lg text-[10px] font-black uppercase tracking-wider">
                <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotClass(reserva.estado_reserva)"></span>
                {{ reserva.estado_reserva }}
              </span>
            </td>

            <!-- Acciones -->
            <td class="px-4 py-2 text-right">
              <div class="flex justify-end gap-2">
                <!-- WhatsApp -->
                <button 
                  v-if="session.isAdmin"
                  @click="openWhatsApp(reserva)"
                  class="p-2 bg-white text-emerald-500 hover:text-emerald-600 border border-gray-100 hover:border-emerald-200 rounded-lg shadow-sm hover:shadow-md transition-all"
                  title="Enviar WhatsApp"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                </button>

                <!-- Asignar Mesa -->
                <button 
                  v-if="!reserva.mesas?.length && (session.isAdmin || session.hasRole('Anfitriona'))" 
                  @click="$emit('asignar', reserva)"
                  class="p-2 bg-white text-gray-400 hover:text-intimar-primary border border-gray-100 hover:border-intimar-primary/30 rounded-lg shadow-sm hover:shadow-md transition-all"
                  title="Asignar Mesa"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M16 4l-4-4-4 4"/><path d="M12 0v16"/></svg>
                </button>
                
                <!-- Editar -->
                <router-link 
                  v-if="session.isAdmin"
                  :to="`/reservas/${reserva.name}`"
                  class="p-2 bg-white text-gray-400 hover:text-intimar-gold border border-gray-100 hover:border-intimar-gold/30 rounded-lg shadow-sm hover:shadow-md transition-all"
                  title="Gestionar"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                </router-link>

                <!-- Eliminar -->
                <button 
                  v-if="session.isAdmin"
                  @click="$emit('delete', reserva)"
                  class="p-2 bg-white text-gray-400 hover:text-red-500 border border-gray-100 hover:border-red-200 rounded-lg shadow-sm hover:shadow-md transition-all"
                  title="Eliminar Reserva"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { session } from '@/data/session'

const props = defineProps({
  reservas: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  columns: {
    type: Object,
    default: () => ({ pago: false, llegada: false, salida: false, mesas: true, creacion: false })
  },
  currentSort: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['refresh', 'asignar', 'delete', 'sort'])

const isSorted = (field) => {
  return props.currentSort.startsWith(field)
}

const getSortDir = (field) => {
  if (!isSorted(field)) return ''
  return props.currentSort.includes('desc') ? 'desc' : 'asc'
}

const toggleSort = (field) => {
  let newSort = ''
  if (field === 'fecha_reserva') {
    if (props.currentSort.startsWith('fecha_reserva')) {
      newSort = props.currentSort.includes('asc') ? 'fecha_reserva desc, hora_reserva desc' : 'fecha_reserva asc, hora_reserva asc'
    } else {
      newSort = 'fecha_reserva asc, hora_reserva asc'
    }
  } else {
    if (props.currentSort.startsWith(field)) {
      newSort = props.currentSort.includes('asc') ? `${field} desc` : `${field} asc`
    } else {
      newSort = `${field} asc`
    }
  }
  emit('sort', newSort)
}

const openWhatsApp = (reserva) => {
  if (!reserva.celular) return
  
  const nombre = reserva.nombre
  const fecha = formatDate(reserva.fecha_reserva)
  const hora = formatTime(reserva.hora_reserva)
  const personas = (reserva.cant_adultos || 0) + (reserva.cant_ninos || 0)
  
  const mensaje = `Hola ${nombre}, te confirmamos tu reserva en Intimar para el ${fecha} a las ${hora} para ${personas} personas. ¡Te esperamos!`
  let phone = reserva.celular.replace(/\D/g, '')
  if (phone.length === 9) phone = '51' + phone
  
  const url = `https://wa.me/${phone}?text=${encodeURIComponent(mensaje)}`
  
  window.open(url, '_blank')
}

// Utilidades
const getAnticipoBadgeClasses = (banco) => {
  const b = (banco || '').toUpperCase().trim()
  if (b.includes('YAPE')) {
    return 'bg-fuchsia-50 text-fuchsia-700 border-fuchsia-200/50'
  }
  if (b.includes('PLIN')) {
    return 'bg-cyan-50 text-cyan-700 border-cyan-200/50'
  }
  if (b.includes('BCP')) {
    return 'bg-blue-50/80 text-blue-700 border-blue-200/50'
  }
  if (b.includes('BBVA')) {
    return 'bg-indigo-50/80 text-indigo-700 border-indigo-200/50'
  }
  if (b.includes('INTERBANK')) {
    return 'bg-emerald-50 text-emerald-700 border-emerald-200/50'
  }
  if (b.includes('SCOTIABANK')) {
    return 'bg-rose-50 text-rose-700 border-rose-200/50'
  }
  return 'bg-green-50 text-green-700 border-green-200/60'
}

const getInitials = (nombre, apellido) => {
  const n = (nombre || '').split(' ')[0] || ''
  const a = (apellido || '').split(' ')[0] || ''
  return (n.charAt(0) + a.charAt(0)).toUpperCase() || '?'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const [year, month, day] = dateString.substring(0, 10).split('-')
  const date = new Date(year, month - 1, day)
  return new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: 'short' }).format(date)
}

const formatTime = (timeString) => {
  if (!timeString) return ''
  return timeString.substring(0, 5)
}

// Estilos de Badges según el estado
const getStatusClass = (estado) => {
  const map = {
    'Solicitud de reserva': 'bg-red-50 text-red-600',
    'Pendiente a confirmar': 'bg-orange-50 text-orange-600',
    'Confirmada': 'bg-green-50 text-green-600',
    'En proceso': 'bg-blue-50 text-blue-600',
    'Finalizada': 'bg-gray-100 text-gray-700',
    'Cancelada': 'bg-red-100 text-red-800',
    'Lista de espera': 'bg-purple-50 text-purple-600',
    'Atrasada': 'bg-rose-50 text-rose-600',
  }
  return map[estado] || 'bg-gray-50 text-gray-500'
}

const getStatusDotClass = (estado) => {
  const map = {
    'Solicitud de reserva': 'bg-red-500',
    'Pendiente a confirmar': 'bg-orange-500',
    'Confirmada': 'bg-green-500',
    'En proceso': 'bg-blue-500',
    'Finalizada': 'bg-gray-500',
    'Cancelada': 'bg-red-500',
    'Lista de espera': 'bg-purple-500',
    'Atrasada': 'bg-rose-500',
  }
  return map[estado] || 'bg-gray-400'
}
</script>
