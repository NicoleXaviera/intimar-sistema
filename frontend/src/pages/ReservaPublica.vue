<template>
  <div class="min-h-screen bg-white flex flex-col md:flex-row font-sans selection:bg-intimar-primary selection:text-white md:h-screen md:overflow-hidden relative">
    
    <!-- LATERAL IZQUIERDO: VISUAL (46%) -->
    <div class="h-[15vh] md:h-full md:w-[46%] relative overflow-hidden bg-intimar-dark shrink-0">
      <div class="absolute inset-0 z-0">
        <TransitionGroup name="fade">
          <img v-for="(img, idx) in heroImages" :key="img" v-show="currentHeroIdx === idx" :src="img" class="absolute inset-0 w-full h-full object-cover transition-all duration-[3000ms]"/>
        </TransitionGroup>
        <div class="absolute inset-0 bg-gradient-to-t from-intimar-dark/60 via-transparent to-transparent"></div>
      </div>
      <div class="absolute bottom-2 left-4 z-10 md:hidden"><p class="text-[7px] font-bold uppercase tracking-[0.4em] text-intimar-gold">Inti-Mar Paracas</p></div>
      <div class="absolute inset-x-0 bottom-0 z-10 p-12 text-white animate-fade-in hidden md:block text-shadow">
        <p class="text-[10px] font-bold uppercase tracking-[0.6em] text-intimar-gold mb-3">Desde 1995</p>
        <p class="text-xl font-light italic opacity-90 leading-relaxed serif-font max-w-sm mb-8">«{{ t.welcomeQuote }}»</p>
      </div>
    </div>

    <!-- LATERAL DERECHO: PORTAL (54%) -->
    <div class="flex-1 md:w-[54%] flex flex-col bg-white overflow-y-auto scrollbar-hide relative">
      
      <!-- Top Bar -->
      <div class="sticky top-0 z-30 bg-white/95 backdrop-blur-md px-5 py-4 md:px-10 md:py-6 border-b border-gray-50 flex items-center justify-between shrink-0">
        <img :src="'/files/intimar-logo.png'" class="h-8 md:h-10 w-auto" />
        <div class="flex items-center gap-4">
            <div class="flex gap-2">
                <button @click="lang = 'es'" :class="['text-[10px] font-bold tracking-widest px-2 py-1 rounded transition-all', lang === 'es' ? 'text-intimar-primary bg-intimar-primary/5' : 'text-gray-300 hover:text-gray-400']">ES</button>
                <button @click="lang = 'en'" :class="['text-[10px] font-bold tracking-widest px-2 py-1 rounded transition-all', lang === 'en' ? 'text-intimar-primary bg-intimar-primary/5' : 'text-gray-300 hover:text-gray-400']">EN</button>
            </div>
            <button v-if="step > 1 && step < 5" @click="step--" class="ml-1 text-gray-400 flex items-center gap-1 text-[9px] font-bold uppercase tracking-widest hover:text-intimar-primary border border-gray-100 px-2 py-1 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
                {{ t.btnBack }}
            </button>
        </div>
      </div>

      <!-- Flow Content -->
      <div :class="['flex-1 flex flex-col', step === 4 ? 'p-5 md:p-8' : 'p-6 md:p-12 lg:p-20']">
        <div :class="['w-full mx-auto space-y-8', step === 4 ? 'max-w-4xl' : 'max-w-md']">
          
          <div v-if="step < 5" class="flex items-center gap-4">
            <div class="flex-1 flex gap-1"><div v-for="i in 4" :key="i" :class="['h-1 flex-1 rounded-full transition-all duration-500', step >= i ? 'bg-intimar-primary' : 'bg-gray-100']"></div></div>
            <span class="text-[8px] font-bold text-gray-400 uppercase tracking-widest shrink-0">{{ step }} / 4</span>
          </div>

          <!-- PASO 1, 2, 3 (Sin cambios) -->
          <div v-if="step === 1" class="space-y-8 animate-fade-in">
            <div class="space-y-1.5"><h2 class="text-3xl md:text-5xl font-light tracking-tighter text-gray-900 leading-none uppercase">{{ t.title1 }}</h2><p class="text-gray-400 text-[9px] font-bold uppercase tracking-[0.2em]">{{ t.subtitle1 }}</p></div>
            <div class="flex flex-wrap gap-2.5">
                <button v-for="p in [1,2,3,4,5,6,7,8]" :key="p" @click="form.adultos = p; showManualPax = false" :class="['h-10 w-10 rounded-full font-medium text-xs transition-all border', form.adultos === p && !showManualPax ? 'bg-intimar-primary border-intimar-primary text-white shadow-md' : 'bg-white border-gray-100 text-gray-400']">{{ p }}</button>
                <button @click="showManualPax = !showManualPax" :class="['h-10 w-10 rounded-full font-medium text-xs transition-all border', showManualPax ? 'bg-intimar-primary border-intimar-primary text-white' : 'bg-white border-gray-100 text-gray-400']">8+</button>
            </div>
            <div class="space-y-5 pt-6 border-t border-gray-50">
                <div class="flex items-center justify-between"><h3 class="text-[10px] font-bold uppercase tracking-[0.3em] text-gray-900">{{ t.labelDate }}</h3><div class="flex gap-4"><button @click="prevMonth" :disabled="currentMonthOffset <= 0" class="text-gray-200 disabled:opacity-0 transition-all"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg></button><button @click="nextMonth" class="text-gray-200 transition-all"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg></button></div></div>
                <div v-for="cal in [calendarData[0]]" :key="cal.month + cal.year" class="space-y-4"><p class="text-[11px] font-bold tracking-[0.2em] uppercase text-intimar-primary text-center py-2 bg-gray-50/80 rounded-xl">{{ getMonthName(cal.month) }} {{ cal.year }}</p><div class="grid grid-cols-7 gap-y-1"><div v-for="day in ['M','T','W','T','F','S','S']" :key="day" class="text-[8px] font-bold text-gray-300 uppercase text-center mb-2">{{ day }}</div><div v-for="n in cal.padding" :key="'p'+n"></div><button v-for="d in cal.days" :key="d.dateStr" @click="selectDate(d.dateStr)" :disabled="d.disabled" :class="['h-9 w-9 rounded-full font-medium text-[11px] mx-auto flex items-center justify-center transition-all', d.disabled ? 'opacity-10' : form.fecha === d.dateStr ? 'bg-intimar-primary text-white shadow-md' : 'text-gray-700 hover:bg-gray-50']">{{ d.day }}</button></div></div>
            </div>
            <button @click="nextStep" :disabled="!form.fecha" class="w-full py-5 bg-intimar-primary text-white rounded-full font-medium uppercase tracking-[0.5em] text-[10px] shadow-xl shadow-intimar-primary/10 transition-all active:scale-95 disabled:opacity-20">{{ t.btnSearch }}</button>
          </div>

          <div v-if="step === 2" class="space-y-10 animate-fade-in">
            <div class="space-y-1.5"><h2 class="text-3xl md:text-5xl font-light tracking-tighter text-gray-900 leading-none uppercase">{{ t.title2 }}</h2><p class="text-gray-400 text-[9px] font-bold uppercase tracking-[0.3em]">{{ t.subtitle2 }}</p></div>
            <div class="grid grid-cols-3 gap-3"><button v-for="slot in availableSlots" :key="slot" @click="form.hora = slot; nextStep()" class="py-5 rounded-2xl font-light text-2xl transition-all border border-gray-50 text-gray-300 hover:border-intimar-primary hover:text-intimar-primary active:scale-95">{{ slot }}</button></div>
            <div class="p-6 bg-gray-50 rounded-3xl flex gap-5 items-start border border-orange-50">
               <div class="text-orange-400 shrink-0 mt-0.5"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="10"/></svg></div>
               <div class="space-y-2"><div class="space-y-1"><p class="text-[9px] font-bold uppercase tracking-[0.2em] text-orange-600">{{ t.policyTitle }}</p><p class="text-[11px] font-medium text-gray-500 leading-snug uppercase">{{ t.policyDesc }}</p></div><p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest pt-2 border-t border-gray-100">{{ t.assignmentNote }}</p></div>
            </div>
          </div>

          <div v-if="step === 3" class="space-y-10 animate-fade-in">
            <div class="space-y-1.5"><h2 class="text-3xl md:text-5xl font-light tracking-tighter text-gray-900 leading-none uppercase">{{ t.title4 }}</h2><p class="text-gray-400 text-[9px] font-bold uppercase tracking-[0.3em] italic">{{ t.subtitle4 }}</p></div>
            <div class="space-y-8">
                <div v-for="f in [{k:'requerimientos',l:'labelSpecialReq',p:'placeholderReq'},{k:'necesidades',l:'labelNeeds',p:'placeholderNeeds'},{k:'alergias',l:'labelAllergies',p:'placeholderAllergies'}]" :key="f.k" class="space-y-2"><label class="text-[11px] font-bold uppercase tracking-[0.2em] text-gray-700 block ml-0.5">{{ t[f.l] }} <span class="text-gray-400 font-normal normal-case italic text-[10px]">({{ t.optional }})</span></label><textarea v-model="form[f.k]" rows="1" class="w-full bg-white border-b border-gray-200 focus:border-intimar-primary outline-none transition-all font-medium text-gray-900 py-2 text-sm" :placeholder="t[f.p]"></textarea></div>
            </div>
            <button @click="nextStep" class="w-full py-5 bg-intimar-primary text-white rounded-full font-medium uppercase tracking-[0.5em] text-[10px] shadow-xl shadow-intimar-primary/10 transition-all active:scale-95">{{ t.btnGoLast }}</button>
          </div>

          <!-- PASO 4 -->
          <div v-if="step === 4" class="animate-fade-in pb-8">
            <div class="flex flex-col lg:flex-row gap-8 lg:gap-10">
              <div class="flex-1 space-y-8">
                <div class="space-y-1.5"><h2 class="text-3xl font-light tracking-tighter text-gray-900 leading-none uppercase">{{ t.title3 }}</h2><p class="text-gray-400 text-[9px] font-bold uppercase tracking-[0.3em]">{{ t.subtitle3 }}</p></div>
                <div class="space-y-5">
                  <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-1.5"><label class="text-[9px] font-bold uppercase tracking-widest text-gray-700 ml-0.5">{{ t.labelName }} *</label><input v-model="form.nombre" type="text" :class="['w-full border-b outline-none py-1 text-sm font-medium uppercase transition-all', errors.nombre ? 'border-red-400' : 'border-gray-200 focus:border-intimar-primary']"></div>
                    <div class="space-y-1.5"><label class="text-[9px] font-bold uppercase tracking-widest text-gray-700 ml-0.5">{{ t.labelLastname }} *</label><input v-model="form.apellido" type="text" :class="['w-full border-b outline-none py-1 text-sm font-medium uppercase transition-all', errors.apellido ? 'border-red-400' : 'border-gray-200 focus:border-intimar-primary']"></div>
                  </div>
                  <div class="space-y-1.5"><label class="text-[9px] font-bold uppercase tracking-widest text-gray-700 ml-0.5">Email *</label><input v-model="form.email" type="email" :class="['w-full border-b outline-none py-1 text-sm font-medium transition-all', errors.email ? 'border-red-400' : 'border-gray-200 focus:border-intimar-primary']"></div>
                  <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-1.5"><label class="text-[9px] font-bold uppercase tracking-widest text-gray-700 ml-0.5">DNI / Passport</label><input v-model="form.dni" type="text" class="w-full border-b border-gray-200 focus:border-intimar-primary outline-none py-1 text-sm font-medium uppercase"></div>
                    <div class="space-y-1.5">
                      <label class="text-[9px] font-bold uppercase tracking-widest text-gray-700 ml-0.5">{{ t.labelPhone }} *</label>
                      <vue-tel-input 
                        v-model="form.celular" 
                        @on-input="onPhoneInput"
                        v-bind="telInputOptions"
                        :class="['border-b transition-all', errors.celular ? 'border-red-400' : 'border-gray-200 focus-within:border-intimar-primary']"
                      ></vue-tel-input>
                    </div>
                  </div>
                </div>
                <div class="space-y-3 pt-6 border-t border-gray-50">
                    <label class="flex gap-3 cursor-pointer group"><input type="checkbox" v-model="form.acepta_legal1" class="mt-0.5 w-4 h-4 rounded border-gray-300 text-intimar-primary transition-all"><span class="text-[9px] font-bold text-gray-500 uppercase tracking-tight leading-snug">{{ t.legal1 }}</span></label>
                    <label class="flex gap-3 cursor-pointer group"><input type="checkbox" v-model="form.acepta_legal3" class="mt-0.5 w-4 h-4 rounded border-gray-300 text-intimar-primary transition-all"><span :class="['text-[9px] font-bold uppercase tracking-tight leading-snug transition-all', errors.acepta_legal3 ? 'text-red-500' : 'text-gray-500']">{{ t.legal3 }} *</span></label>
                </div>
                <div class="space-y-4">
                    <!-- Mensaje de Error del Servidor -->
                    <div v-if="apiError" class="p-4 bg-red-50 border border-red-100 rounded-2xl animate-in fade-in zoom-in duration-300">
                        <p class="text-[10px] font-black text-red-600 uppercase tracking-widest leading-relaxed text-center">
                           {{ apiError }}
                        </p>
                    </div>

                    <p v-if="Object.keys(errors).length > 0" class="text-[10px] font-bold text-red-500 uppercase tracking-widest text-center animate-pulse">{{ t.errorRequired }}</p>
                    <button @click="submitReserva" :disabled="submitting" class="w-full py-5 bg-intimar-primary text-white rounded-full font-medium uppercase tracking-[0.5em] text-[10px] shadow-xl shadow-intimar-primary/20 active:translate-y-1 transition-all flex items-center justify-center gap-4 disabled:opacity-50">{{ submitting ? t.btnProcessing : t.btnConfirm }}</button>
                </div>
              </div>
              <!-- DERECHA -->
              <div class="lg:w-64 space-y-4 shrink-0">
                <div class="bg-intimar-dark rounded-3xl p-5 text-white space-y-5 shadow-xl border border-white/5">
                    <div class="space-y-1"><h3 class="text-base font-light serif-font italic text-white/90 leading-tight">Inti-Mar Paracas</h3><p class="text-[6px] font-bold uppercase tracking-[0.4em] text-intimar-gold">{{ t.summaryTitle }}</p></div>
                    <div class="space-y-3 pt-3 border-t border-white/5">
                        <div class="flex items-center gap-3"><div class="text-intimar-gold/80"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div><span class="text-[9px] font-medium tracking-widest uppercase">{{ form.adultos }} {{ t.summaryPax }}</span></div>
                        <div class="flex items-center gap-3"><div class="text-intimar-gold/80"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg></div><span class="text-[9px] font-medium tracking-widest uppercase">{{ formatDate(form.fecha) }}</span></div>
                        <div class="flex items-center gap-3"><div class="text-intimar-gold/80"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div><span class="text-[9px] font-medium tracking-widest uppercase">{{ form.hora }}</span></div>
                    </div>
                </div>
                <div class="bg-gray-50 rounded-3xl p-5 space-y-4 text-[9px] border border-gray-100">
                    <div class="space-y-1.5 border-b border-gray-100/50 pb-3"><div class="flex gap-2 items-center text-intimar-primary"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg><span class="font-bold uppercase tracking-widest text-gray-400 text-[7px]">Info & Contacto</span></div><p class="font-bold text-gray-900 uppercase leading-tight text-[8px]">Km 38 Carr. Pisco – Pto San Martín, Paracas</p><p class="font-bold text-intimar-primary tracking-widest">+51 981 318 866</p></div>
                    <div class="space-y-3 border-b border-gray-100/50 pb-3"><div class="flex justify-between items-center"><span class="font-bold uppercase tracking-widest text-gray-400 text-[7px]">Horarios</span><span class="text-[5px] bg-red-100 text-red-600 px-1 py-0.5 rounded-full font-bold">CERRADO MIÉ</span></div><div class="flex justify-between uppercase text-[7px]"><div class="space-y-0.5"><p class="text-gray-400 font-bold">ALM.</p><p class="font-bold text-gray-900">11 AM–4 PM</p></div><div class="space-y-0.5 text-right"><p class="text-gray-400 font-bold">CENA</p><p class="font-bold text-gray-900">7–8:30 PM</p></div></div></div>
                    <p class="text-gray-400 leading-snug uppercase italic text-[7px] font-medium">{{ t.infoText }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- ÉXITO CON ID DE RESERVA -->
          <div v-if="step === 5" class="text-center space-y-10 animate-fade-in py-12 md:py-20">
            <div class="w-16 h-16 bg-emerald-500 text-white rounded-full flex items-center justify-center mx-auto shadow-xl animate-bounce text-2xl font-bold">✓</div>
            
            <div class="space-y-4">
              <h2 class="text-4xl font-light tracking-tighter uppercase text-gray-900 leading-none">{{ t.successTitle }}</h2>
              <p class="text-gray-600 font-medium text-base max-w-[280px] mx-auto leading-relaxed">{{ t.successDesc.replace('{name}', form.nombre) }}</p>
            </div>

            <div class="max-w-[300px] mx-auto p-6 bg-intimar-primary/5 rounded-[2rem] border border-intimar-primary/10 space-y-3">
                <p class="text-[9px] font-bold text-intimar-primary uppercase tracking-[0.4em]">{{ t.idLabel }}</p>
                <p class="text-3xl font-light tracking-tight text-gray-900 uppercase serif-font">{{ reservationId }}</p>
                <p class="text-[8px] text-gray-400 uppercase font-bold tracking-widest pt-2">{{ t.idHint }}</p>
            </div>

            <button @click="resetForm" class="text-[9px] font-bold uppercase tracking-[0.4em] text-intimar-primary border-b border-intimar-primary/20 pb-1 transition-all hover:border-intimar-primary">{{ t.btnBackHome }}</button>
          </div>

        </div>
      </div>
    </div>

    <!-- MODAL DE AFORO / LISTA DE ESPERA -->
    <div v-if="showWaitlistModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-intimar-dark/40 backdrop-blur-md animate-fade-in">
        <div class="bg-white w-full max-w-sm rounded-[2.5rem] p-10 shadow-2xl space-y-8 text-center border border-gray-100">
            <div class="w-14 h-14 bg-orange-100 text-orange-500 rounded-full flex items-center justify-center mx-auto">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="m12.8 2.8 8.1 13.5c.6 1 .6 2.2 0 3.2s-1.7 1.5-2.8 1.5H3.9c-1.1 0-2.2-.5-2.8-1.5s-.6-2.2 0-3.2l8.1-13.5c.6-1 1.7-1.5 2.8-1.5s2.2.5 2.8 1.5Z"/></svg>
            </div>
            <div class="space-y-3">
                <h3 class="text-2xl font-light tracking-tight uppercase text-gray-900">{{ t.waitlistTitle }}</h3>
                <p class="text-gray-500 text-xs font-medium leading-relaxed">{{ t.waitlistDesc }}</p>
            </div>
            <div class="space-y-3 pt-4">
                <button @click="joinWaitlist" class="w-full py-4 bg-intimar-primary text-white rounded-full font-bold uppercase tracking-[0.3em] text-[9px] shadow-lg transition-all active:scale-95 hover:bg-intimar-dark">
                    {{ t.btnWaitlist }}
                </button>
                <button @click="changeTime" class="w-full py-4 bg-gray-50 text-gray-400 rounded-full font-bold uppercase tracking-[0.3em] text-[9px] transition-all hover:text-gray-600 active:scale-95">
                    {{ t.btnChangeTime }}
                </button>
            </div>
        </div>
    </div>

    <!-- BOTÓN WHATSAPP -->
    <a href="https://wa.me/51981318866?text=Hola%20Intimar,%20tengo%20una%20consulta%20sobre%20mi%20reserva." target="_blank" class="fixed bottom-6 right-6 z-50 w-14 h-14 bg-[#25D366] text-white rounded-full flex items-center justify-center shadow-2xl hover:scale-110 transition-all active:scale-95 group">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 1 1-7.6-7.6 8.38 8.38 0 0 1 3.8.9L22 2l-1.5 5.5Z"/></svg>
      <span class="absolute right-16 bg-white text-gray-900 text-[10px] font-bold px-3 py-2 rounded-xl shadow-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none uppercase tracking-widest border border-gray-100">{{ lang === 'es' ? '¿Consultas?' : 'Questions?' }}</span>
    </a>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { call } from 'frappe-ui'
import { VueTelInput } from 'vue-tel-input'
import 'vue-tel-input/vue-tel-input.css'

const step = ref(1); const submitting = ref(false); const lang = ref('es'); const showManualPax = ref(false); const currentMonthOffset = ref(0); const currentHeroIdx = ref(0); let heroTimer = null;
const reservationId = ref(''); const showWaitlistModal = ref(false); const apiError = ref('');
const heroImages = ['/files/intimar-1.webp','/files/intimar-2.webp','/files/intimar-3.webp']
const form = reactive({ fecha: '', adultos: 2, ninos: 0, hora: '', nombre: '', apellido: '', celular: '', codigoPais: '+51', email: '', dni: '', requerimientos: '', necesidades: '', alergias: '', acepta_legal1: false, acepta_legal3: false, aceptar_lista_espera: 0 })
const errors = reactive({})

const telInputOptions = {
  mode: 'international',
  dropdownOptions: { showFlags: true, showDialCodeInSelection: true },
  inputOptions: { placeholder: '987 654 321', showDialCode: false },
  autoDefaultCountry: true
}

const onPhoneInput = (phone, phoneObject) => {
  if (phoneObject) {
    // Guardamos el código de país por separado por si acaso
    if (phoneObject.countryCallingCode) {
      form.codigoPais = '+' + phoneObject.countryCallingCode
    }
    // Si el número es válido o tiene formato, lo usamos completo
    if (phoneObject.number) {
      form.fullPhone = phoneObject.number // Este ya incluye el + y prefijo
    }
  }
}

const translations = {
  es: {
    welcomeQuote: 'Bienvenidos a este lugar de respeto por la naturaleza, gusto por la buena mesa y Pasión por el mar.',
    summaryTitle: 'Resumen de Reserva', summaryPax: 'Personas',
    title1: 'Experiencia', subtitle1: '¿Cuántas personas nos visitan?',
    labelDate: 'Selecciona una Fecha', btnSearch: 'Buscar Disponibilidad',
    title2: 'Horarios Disponibles', subtitle2: 'Sujeto a disponibilidad del día',
    policyTitle: 'Tolerancia', policyDesc: '15 minutos. Pasado este tiempo, su mesa podría ser reasignada.',
    assignmentNote: 'Las mesas se asignan según disponibilidad por orden de llegada.',
    title3: 'Confirma tus Datos', subtitle3: 'Solo falta un paso para asegurar tu mesa',
    labelName: 'Nombre', labelLastname: 'Apellido', labelPhone: 'Teléfono',
    title4: 'Personalizar', subtitle4: 'Ayúdanos a que tu visita sea única',
    labelSpecialReq: '¿Algún requerimiento especial?', placeholderReq: 'Ej: Mesa cerca al mar...',
    labelNeeds: '¿Alguna necesidad especial?', placeholderNeeds: 'Ej: Silla de bebé...',
    labelAllergies: '¿Alguna alergia o intolerancia?', placeholderAllergies: 'Ej: Mariscos, gluten...',
    optional: 'Opcional',
    btnGoLast: 'Ir al último paso',
    infoText: 'NOTA: Todos los visitantes abonan el ingreso a la Reserva Nacional de Paracas en el control.',
    btnConfirm: 'Confirmar Reserva', btnProcessing: 'Procesando...', btnNext: 'Siguiente Paso', btnBack: 'Volver',
    successTitle: '¡Reserva Lista!', successDesc: 'Gracias {name}, recibimos tu solicitud. Nos contactaremos pronto.',
    btnBackHome: 'Volver al Inicio',
    idLabel: 'Código de Reserva', idHint: 'Guarda este código para tu visita',
    legal1: 'Acepto la Política de Privacidad.',
    legal3: 'Autorizo comunicaciones comerciales (WhatsApp/Email/SMS).',
    errorRequired: 'Por favor, completa todos los campos obligatorios (*)',
    waitlistTitle: 'Sin Disponibilidad',
    waitlistDesc: 'Lo sentimos, ya no tenemos mesas libres para este horario. ¿Deseas ingresar a nuestra lista de espera o prefieres buscar otro horario?',
    btnWaitlist: 'Pasar a lista de espera',
    btnChangeTime: 'Elegir otro horario'
  },
  en: {
    welcomeQuote: 'Welcome to this place of respect for nature, taste for good food, and Passion for the sea.',
    summaryTitle: 'Booking Summary', summaryPax: 'People',
    title1: 'Experience', subtitle1: 'How many people will visit us?',
    labelDate: 'Select a Date', btnSearch: 'Search Availability',
    title2: 'Available Slots', subtitle2: 'Times subject to availability',
    policyTitle: 'Grace Period', policyDesc: '15-minute tolerance. After this time, your table may be reassigned.',
    assignmentNote: 'Tables are assigned based on availability upon arrival.',
    title3: 'Confirm Your Details', subtitle3: 'Just one step left to secure your table',
    labelName: 'First Name', labelLastname: 'Last Name', labelPhone: 'Phone',
    title4: 'Personalize', subtitle4: 'Help us make your visit unique',
    labelSpecialReq: 'Any special requests?', placeholderReq: 'E.g. Table near the ocean...',
    labelNeeds: 'Any special needs?', placeholderNeeds: 'E.g. Baby chair...',
    labelAllergies: 'Any allergies or intolerances?', placeholderAllergies: 'E.g. Seafood...',
    optional: 'Optional',
    btnGoLast: 'Go to the last step',
    infoText: 'NOTE: All visitors pay the entry fee to the Paracas National Reserve at the control point.',
    btnConfirm: 'Confirm Reservation', btnProcessing: 'Processing...', btnNext: 'Next Step', btnBack: 'Back',
    successTitle: 'Done!', successDesc: 'Thank you {name}, we received your request. We will contact you shortly.',
    btnBackHome: 'Back to Start',
    idLabel: 'Booking Code', idHint: 'Keep this code for your visit',
    legal1: 'I accept the Privacy Policy.',
    legal3: 'I authorize commercial communications.',
    errorRequired: 'Please complete all required fields (*)',
    waitlistTitle: 'No Availability',
    waitlistDesc: 'Sorry, we are fully booked for this time. Would you like to join our waitlist or choose a different time?',
    btnWaitlist: 'Join waitlist',
    btnChangeTime: 'Choose another time'
  }
}

const t = computed(() => translations[lang.value])
const formatDate = (dateStr) => { if (!dateStr) return ''; const date = new Date(dateStr + 'T12:00:00'); return date.toLocaleDateString(lang.value === 'es' ? 'es-ES' : 'en-US', { weekday: 'short', day: 'numeric', month: 'short' }).toUpperCase(); }
const calendarData = computed(() => { const months = []; let curr = new Date(); curr.setMonth(curr.getMonth() + currentMonthOffset.value); curr.setDate(1); for (let i = 0; i < 2; i++) { const month = curr.getMonth(); const year = curr.getFullYear(); let firstDay = new Date(year, month, 1).getDay(); let padding = firstDay === 0 ? 6 : firstDay - 1; const daysInMonth = new Date(year, month + 1, 0).getDate(); const days = []; for (let d = 1; d <= daysInMonth; d++) { const date = new Date(year, month, d); const dateStr = date.toISOString().split('T')[0]; const today = new Date(); today.setHours(0,0,0,0); days.push({ day: d, dateStr, disabled: date < today }) } months.push({ month, year, padding, days }); curr.setMonth(curr.getMonth() + 1); } return months })
const nextMonth = () => currentMonthOffset.value++; const prevMonth = () => { if (currentMonthOffset.value > 0) currentMonthOffset.value-- };
const getMonthName = (m) => { const names = lang.value === 'es' ? ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'] : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']; return names[m]; }
const selectDate = (dateStr) => form.fecha = dateStr; const availableSlots = ['12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'];
const nextStep = () => { step.value++; window.scrollTo({ top: 0, behavior: 'smooth' }) }

const validateForm = () => {
    Object.keys(errors).forEach(key => delete errors[key])
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!form.nombre) errors.nombre = true
    if (!form.apellido) errors.apellido = true
    if (!form.email || !emailRegex.test(form.email)) errors.email = true
    if (!form.celular) errors.celular = true
    if (!form.acepta_legal3) errors.acepta_legal3 = true
    return Object.keys(errors).length === 0
}

const submitReserva = async () => {
  if (!validateForm()) { window.scrollTo({ top: 0, behavior: 'smooth' }); return }
  submitting.value = true
  try {
    const finalPhone = form.fullPhone || form.celular.replace(/\s/g, '')

    const res = await call('intimar_erp.api.crear_reserva_publica', { 
      cliente_nombre: form.nombre, 
      apellido: form.apellido, 
      cliente_celular: finalPhone, 
      codigo_pais: form.codigoPais,
      fecha: form.fecha, hora: form.hora, adultos: form.adultos, ninos: form.ninos || 0, email: form.email, dni: form.dni, alergias: form.alergias, requerimientos: form.requerimientos, necesidades: form.necesidades, acepta_politicas: form.acepta_legal1 ? 1 : 0, acepta_promociones: form.acepta_legal3 ? 1 : 0, aceptar_lista_espera: form.aceptar_lista_espera })
    
    if (res && res.status === 'success') {
        reservationId.value = res.reserva_name;
        step.value = 5; showWaitlistModal.value = false; window.scrollTo({ top: 0, behavior: 'smooth' })
    } else if (res && res.status === 'error') {
        if (res.message && res.message.includes('Aforo excedido')) {
            showWaitlistModal.value = true
        } else {
            apiError.value = res.message || 'Error al procesar la reserva.'
        }
    }
  } catch (e) { 
    console.error(e); 
    apiError.value = 'Ocurrió un problema de conexión. Intente nuevamente.'
  } finally { submitting.value = false }
}

const joinWaitlist = () => { form.aceptar_lista_espera = 1; submitReserva(); }
const changeTime = () => { showWaitlistModal.value = false; step.value = 2; window.scrollTo({ top: 0, behavior: 'smooth' }) }

const resetForm = () => { step.value = 1; showManualPax.value = false; reservationId.value = ''; showWaitlistModal.value = false; Object.assign(form, { fecha: '', adultos: 2, ninos: 0, hora: '', nombre: '', apellido: '', celular: '', codigoPais: '+51', email: '', dni: '', requerimientos: '', necesidades: '', alergias: '', acepta_legal1: false, acepta_legal3: false, aceptar_lista_espera: 0 }); Object.keys(errors).forEach(key => delete errors[key]) }

onMounted(() => { const userLang = navigator.language || navigator.userLanguage; if (userLang.startsWith('en')) lang.value = 'en'; else lang.value = 'es'; heroTimer = setInterval(() => { currentHeroIdx.value = (currentHeroIdx.value + 1) % heroImages.length }, 6000) })
onUnmounted(() => { if (heroTimer) clearInterval(heroTimer) })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:italic,wght@400;700&display=swap');
.serif-font { font-family: 'Playfair Display', serif; }
.fade-enter-active, .fade-leave-active { transition: opacity 3s ease-in-out; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
@keyframes fade-in { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fade-in 0.3s ease-out forwards; }
.scrollbar-hide::-webkit-scrollbar { display: none; }
input::-webkit-outer-spin-button, input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
@media (max-width: 768px) { .h-screen { height: auto !important; overflow: visible !important; } }
.text-shadow { text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
</style>
