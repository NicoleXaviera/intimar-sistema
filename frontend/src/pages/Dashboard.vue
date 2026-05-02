<template>
  <div class="min-h-screen bg-gray-50 flex overflow-hidden">
    <Sidebar />
    
    <div class="flex-1 flex flex-col h-screen overflow-hidden relative">
      <main class="flex-1 w-full h-full p-4 md:p-8 overflow-y-auto">
        <!-- Título de la sección -->
        <div class="flex justify-between items-center mb-10">
          <div>
            <h1 class="text-4xl font-black text-intimar-dark italic tracking-tighter drop-shadow-sm">
              GRÁFICAS <span class="text-intimar-gold">ESTADÍSTICAS</span>
            </h1>
            <p class="text-gray-500 font-bold text-[10px] uppercase tracking-[0.3em] mt-1">
              Control Operativo en Tiempo Real
            </p>
          </div>

          <div class="flex gap-3">
            <button 
              @click="refreshAll"
              class="bg-white p-3 rounded-2xl shadow-sm border border-gray-100 hover:bg-gray-50 transition-all group"
              title="Refrescar Todo"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" :class="{'animate-spin': loading}"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            </button>
          </div>
        </div>
        <!-- Panel de Aforo en Tiempo Real -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <!-- Aforo Total -->
          <div class="bg-white p-6 rounded-[2.5rem] border border-gray-100 shadow-sm relative overflow-hidden group">
            <div class="absolute right-6 top-6 text-gray-100 group-hover:text-intimar-gold/20 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9Z"/><path d="M3 9V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4"/></svg>
            </div>
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">General</p>
            <h3 class="text-xs font-black text-gray-400 mb-2 italic uppercase">Aforo total</h3>
            <h2 class="text-5xl font-black text-intimar-dark tracking-tighter">{{ stats?.kpis?.aforo_total || 0 }}</h2>
          </div>

          <!-- Aforo Actual (Personas en Sala) -->
          <div class="bg-intimar-primary p-6 rounded-[2.5rem] shadow-xl shadow-intimar-primary/20 relative overflow-hidden group">
             <div class="absolute right-6 top-6 text-white/10 group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            </div>
            <p class="text-[10px] font-black text-white/50 uppercase tracking-widest mb-1">En Intimar</p>
            <h3 class="text-xs font-black text-intimar-gold mb-2 italic uppercase">Aforo actual</h3>
            <h2 class="text-5xl font-black text-white leading-none tracking-tighter mb-2">{{ stats?.kpis?.personas_en_restaurante || 0 }}</h2>
            <p class="text-[10px] font-black text-white/40 uppercase tracking-widest">de {{ stats?.kpis?.reservas_en_proceso || 0 }} reservas</p>
          </div>

          <!-- Lista de Espera -->
          <div class="bg-white p-6 rounded-[2.5rem] border border-gray-100 shadow-sm relative group">
             <div class="absolute right-6 top-6 text-amber-500/10">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
            </div>
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Por entrar</p>
            <h3 class="text-xs font-black text-amber-500 mb-2 italic uppercase">Lista de espera</h3>
            <h2 class="text-5xl font-black text-intimar-dark tracking-tighter mb-2">{{ stats?.kpis?.personas_en_espera || 0 }}</h2>
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">de {{ stats?.kpis?.reservas_en_espera || 0 }} reservas</p>
          </div>

          <!-- Mesas Disponibles -->
          <div class="bg-white p-6 rounded-[2.5rem] border-2 border-emerald-500/20 shadow-sm relative group overflow-hidden">
             <div class="absolute right-6 top-6 text-emerald-500/10">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
            </div>
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Disponibilidad</p>
            <h3 class="text-xs font-black text-emerald-500 mb-2 italic uppercase">Mesas libres</h3>
            <h2 class="text-5xl font-black text-intimar-dark tracking-tighter">{{ stats?.kpis?.mesas_disponibles || 0 }}</h2>
          </div>
        </div>

        <!-- Dashboard de Insights (Iframe) -->
        <div class="w-full h-[800px] bg-white rounded-[3rem] shadow-2xl shadow-gray-200/50 border border-gray-100 overflow-hidden relative">
          <iframe 
            :key="dashboardKey"
            :src="dashboardUrl" 
            class="w-full h-full border-none"
            allowfullscreen
          ></iframe>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { call } from 'frappe-ui'
import Sidebar from '@/components/Sidebar.vue'

const stats = ref(null)
const dashboardKey = ref(0)
const loading = ref(true)

const occupancyPercent = computed(() => {
  if (!stats.value?.kpis?.aforo_total) return 0
  return (stats.value.kpis.personas_en_restaurante / stats.value.kpis.aforo_total) * 100
})

const dashboardUrl = computed(() => {
  return window.location.origin + '/insights/shared/dashboard/4329ndoq8f'
})

const fetchRealtimeStats = async () => {
  try {
    const data = await call('intimar_erp.api.get_dashboard_stats')
    stats.value = data
  } catch (e) {
    console.error("Error cargando aforo:", e)
  }
}

const refreshAll = async () => {
  loading.value = true
  dashboardKey.value++
  await fetchRealtimeStats()
  setTimeout(() => { loading.value = false }, 1000)
}

onMounted(() => {
  refreshAll()
  // Auto-refrescar aforo cada 30 segundos sin recargar el iframe
  setInterval(fetchRealtimeStats, 30000)
})
</script>

<style scoped>
/* Estilos para el scroll interno suave */
main::-webkit-scrollbar {
  width: 6px;
}
main::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}

iframe {
  filter: contrast(1.02);
}
</style>
