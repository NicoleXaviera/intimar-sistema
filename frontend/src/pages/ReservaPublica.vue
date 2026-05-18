<template>
  <div class="min-h-screen bg-white flex flex-col md:flex-row font-sans selection:bg-intimar-primary selection:text-white md:h-screen md:overflow-hidden relative">
    
    <!-- LATERAL IZQUIERDO: VISUAL (46%) -->
    <div class="h-[35vh] md:h-full md:w-[46%] relative overflow-hidden bg-intimar-dark shrink-0 shadow-2xl z-0">
      <div class="absolute inset-0 z-0">
        <TransitionGroup name="fade">
          <img v-for="(img, idx) in heroImages" :key="img" v-show="currentHeroIdx === idx" :src="img" class="absolute inset-0 w-full h-full object-cover transition-all duration-[3000ms]"/>
        </TransitionGroup>
        <div class="absolute inset-0 bg-gradient-to-t from-intimar-dark/60 via-transparent to-transparent"></div>
      </div>
      <div class="absolute inset-x-0 bottom-0 z-10 p-6 md:p-12 text-white animate-fade-in text-shadow">
        <p class="text-[8px] md:text-[10px] font-bold uppercase tracking-[0.4em] md:tracking-[0.6em] text-intimar-gold mb-1 md:mb-3">Desde 1995</p>
        <p class="text-xs md:text-xl font-light italic opacity-90 leading-relaxed serif-font max-w-[300px] md:max-w-sm mb-4 md:mb-8">«{{ t.welcomeQuote }}»</p>
      </div>
    </div>

    <!-- LATERAL DERECHO: PORTAL (54%) -->
    <div class="flex-1 md:w-[54%] flex flex-col bg-white overflow-y-auto scrollbar-hide relative">
      
      <!-- Top Bar -->
      <div class="sticky top-0 z-30 bg-white/95 backdrop-blur-md px-4 py-3 md:px-10 md:py-6 border-b border-gray-50 flex items-center justify-between shrink-0 md:rounded-none">
        <div class="flex items-center gap-2 md:gap-3">
            <img :src="'/files/intimar-logo.png'" class="h-6 md:h-10 w-auto" />
            <div class="flex gap-3 md:gap-4 ml-2 md:ml-4">
                <a href="https://www.inti-mar.com/wp-content/uploads/2023/03/CARTA_ESPANOLvsINGLES_5.pdf" target="_blank" class="text-[8px] md:text-[9px] font-black uppercase tracking-widest text-gray-400 hover:text-intimar-primary flex items-center gap-1.5">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
                    <span class="inline">{{ lang === 'es' ? 'Carta' : 'Menu' }}</span>
                </a>
                <a href="https://maps.app.goo.gl/B6V8iT3gZTCuRfxbA" target="_blank" class="text-[9px] font-black uppercase tracking-widest text-gray-400 hover:text-intimar-primary flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                    <span class="hidden sm:inline">{{ lang === 'es' ? 'Cómo llegar' : 'Directions' }}</span>
                </a>
                <a href="https://www.instagram.com/intimarparacas/" target="_blank" class="text-[9px] font-black uppercase tracking-widest text-gray-400 hover:text-pink-600 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
                    <span class="hidden sm:inline">IG</span>
                </a>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <div class="flex gap-1 md:gap-2 mr-0.5">
                <button @click="lang = 'es'" :class="['text-[9px] md:text-[10px] font-bold tracking-widest px-1.5 py-1 rounded transition-all', lang === 'es' ? 'text-intimar-primary bg-intimar-primary/5' : 'text-gray-300 hover:text-gray-400']">ES</button>
                <button @click="lang = 'en'" :class="['text-[9px] md:text-[10px] font-bold tracking-widest px-1.5 py-1 rounded transition-all', lang === 'en' ? 'text-intimar-primary bg-intimar-primary/5' : 'text-gray-300 hover:text-gray-400']">EN</button>
            </div>
            
            <button v-if="step > 1 && step < 5" @click="step--" class="text-gray-400 flex items-center justify-center h-8 w-8 hover:text-intimar-primary border border-gray-100 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
            </button>
        </div>
      </div>

      <!-- Flow Content -->
      <div :class="['flex-1 flex flex-col relative z-10 -mt-8 md:mt-0 bg-white rounded-t-[2.5rem] md:rounded-none', step === 4 ? 'p-6 md:p-8' : (step === 5 ? 'p-4 md:p-12' : 'p-8 md:p-12 lg:p-20')]">
        <div :class="['w-full mx-auto space-y-6 md:space-y-8', step === 4 ? 'max-w-4xl' : 'max-w-md']">
          
          <div v-if="step < 5" class="flex items-center gap-4 mb-2">
            <div class="flex-1 flex gap-1"><div v-for="i in 4" :key="i" :class="['h-1 flex-1 rounded-full transition-all duration-500', step >= i ? 'bg-intimar-primary' : 'bg-gray-100']"></div></div>
            <span class="text-[8px] font-black text-gray-400 uppercase tracking-widest shrink-0">{{ step }} / 4</span>
          </div>

          <!-- PASO 1 -->
          <div v-if="step === 1" class="space-y-6 md:space-y-8 animate-fade-in">
            <div class="space-y-2"><h2 class="text-4xl md:text-5xl font-light tracking-tighter text-gray-900 leading-none uppercase">{{ t.title1 }}</h2><p class="text-gray-400 text-[9px] font-bold uppercase tracking-[0.2em]">{{ t.subtitle1 }}</p></div>
            <div class="flex flex-wrap gap-2.5">
                <button v-for="p in [1,2,3,4,5,6,7,8]" :key="p" @click="form.adultos = p; showManualPax = false" :class="['h-10 w-10 rounded-full font-medium text-xs transition-all border', form.adultos === p && !showManualPax ? 'bg-intimar-primary border-intimar-primary text-white shadow-md' : 'bg-white border-gray-100 text-gray-400']">{{ p }}</button>
                <button @click="showManualPax = !showManualPax; if(showManualPax && form.adultos <= 8) form.adultos = 9" :class="['h-10 w-10 rounded-full font-medium text-xs transition-all border', showManualPax ? 'bg-intimar-primary border-intimar-primary text-white' : 'bg-white border-gray-100 text-gray-400']">8+</button>
            </div>
            <div v-if="showManualPax" class="animate-fade-in pt-2">
                <div class="space-y-1.5 max-w-[140px]">
                    <label class="text-[9px] font-bold uppercase tracking-widest text-intimar-primary ml-0.5">{{ t.labelManualPax }}</label>
                    <input 
                        v-model.number="form.adultos" 
                        type="number" 
                        min="1"
                        class="w-full border-b border-gray-200 focus:border-intimar-primary outline-none py-1 text-xl font-light tracking-tight transition-all"
                    >
                </div>
            </div>
            <div class="space-y-5 pt-6 border-t border-gray-50">
                <div class="flex items-center justify-between"><h3 class="text-[10px] font-bold uppercase tracking-[0.3em] text-gray-900">{{ t.labelDate }}</h3><div class="flex gap-4"><button @click="prevMonth" :disabled="currentMonthOffset <= 0" class="text-gray-200 disabled:opacity-0 transition-all"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg></button><button @click="nextMonth" class="text-gray-200 transition-all"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg></button></div></div>
                <div v-for="cal in [calendarData[0]]" :key="cal.month + cal.year" class="space-y-4"><p class="text-[11px] font-bold tracking-[0.2em] uppercase text-intimar-primary text-center py-2 bg-gray-50/80 rounded-xl">{{ getMonthName(cal.month) }} {{ cal.year }}</p><div class="grid grid-cols-7 gap-y-1"><div v-for="day in ['M','T','W','T','F','S','S']" :key="day" class="text-[8px] font-bold text-gray-300 uppercase text-center mb-2">{{ day }}</div><div v-for="n in cal.padding" :key="'p'+n"></div><button v-for="d in cal.days" :key="d.dateStr" @click="selectDate(d.dateStr)" :disabled="d.disabled" :class="['h-9 w-9 rounded-full font-medium text-[11px] mx-auto flex items-center justify-center transition-all', d.disabled ? 'opacity-10' : form.fecha === d.dateStr ? 'bg-intimar-primary text-white shadow-md' : 'text-gray-700 hover:bg-gray-50']">{{ d.day }}</button></div></div>
            </div>
            <button @click="nextStep" :disabled="!form.fecha" class="w-full py-5 bg-intimar-primary text-white rounded-full font-medium uppercase tracking-[0.5em] text-[10px] shadow-xl shadow-intimar-primary/10 transition-all active:scale-95 disabled:opacity-20">{{ t.btnSearch }}</button>
          </div>

          <div v-if="step === 2" class="space-y-10 animate-fade-in">
            <div class="space-y-1.5"><h2 class="text-3xl md:text-5xl font-light tracking-tighter text-gray-900 leading-none uppercase">{{ t.title2 }}</h2><p class="text-gray-400 text-[9px] font-bold uppercase tracking-[0.3em]">{{ t.subtitle2 }}</p></div>
            <div class="grid grid-cols-3 gap-3">
              <button 
                v-for="slot in availableSlots" 
                :key="slot" 
                @click="handleSlotClick(slot)" 
                class="py-5 rounded-2xl font-light text-2xl transition-all border relative overflow-hidden"
                :class="getSlotClass(slot)"
              >
                {{ slot }}
                <!-- Línea de Tachado (X) -->
                <div v-if="isSlotDisabled(slot)" class="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div class="w-full h-[1px] bg-red-400/40 -rotate-45"></div>
                </div>
              </button>
            </div>
            <div v-if="loadingSlots" class="mt-4 flex justify-center">
              <div class="animate-spin h-5 w-5 border-2 border-intimar-primary border-t-transparent rounded-full"></div>
            </div>
            <div class="p-6 bg-gray-50 rounded-3xl flex gap-5 items-start border border-orange-50">
               <div class="text-orange-400 shrink-0 mt-0.5"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="10"/></svg></div>
               <div class="space-y-2">
                 <div class="space-y-1">
                   <p class="text-[9px] font-bold uppercase tracking-[0.2em] text-orange-600">{{ t.policyTitle }}</p>
                   <p class="text-[11px] font-medium text-gray-500 leading-snug uppercase">{{ t.policyDesc }}</p>
                 </div>
                 <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest pt-2 border-t border-gray-100">{{ t.assignmentNote }}</p>
               </div>
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
                <div class="p-5 bg-gray-50 rounded-3xl border border-gray-100 space-y-3">
                    <div class="flex items-center gap-2 text-intimar-gold">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                        <span class="text-[9px] font-black uppercase tracking-widest">{{ lang === 'es' ? 'Políticas de Reserva' : 'Booking Policies' }}</span>
                    </div>
                    <p class="text-[10px] font-medium text-gray-500 leading-relaxed uppercase">
                        {{ t.generalPolicy }}
                    </p>
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
                    <div class="space-y-1.5 border-b border-gray-100/50 pb-3">
                        <div class="flex gap-2 items-center text-intimar-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                            <span class="font-bold uppercase tracking-widest text-gray-400 text-[7px]">Info & Contacto</span>
                        </div>
                        <a href="https://maps.app.goo.gl/B6V8iT3gZTCuRfxbA" target="_blank" class="block font-bold text-gray-900 uppercase leading-tight text-[8px] hover:text-intimar-primary transition-colors">Km 38 Carr. Pisco – Pto San Martín, Paracas</a>
                        <a href="tel:+51981318866" class="block font-bold text-intimar-primary tracking-widest hover:underline">+51 981 318 866</a>
                    </div>
                    <div class="space-y-3 border-b border-gray-100/50 pb-3">
                        <div class="flex justify-between items-center"><span class="font-bold uppercase tracking-widest text-gray-400 text-[7px]">Horarios</span><span class="text-[5px] bg-red-100 text-red-600 px-1 py-0.5 rounded-full font-bold">CERRADO MIÉ</span></div>
                        <div class="flex justify-between uppercase text-[7px]"><div class="space-y-0.5"><p class="text-gray-400 font-bold">ALM.</p><p class="font-bold text-gray-900">11 AM–4 PM</p></div><div class="space-y-0.5 text-right"><p class="text-gray-400 font-bold">CENA</p><p class="font-bold text-gray-900">7–8:30 PM</p></div></div>
                    </div>
                    <div class="grid grid-cols-2 gap-2 pt-2">
                        <a href="https://www.inti-mar.com/wp-content/uploads/2023/03/CARTA_ESPANOLvsINGLES_5.pdf" target="_blank" class="bg-white border border-gray-100 py-2 rounded-xl text-[7px] font-black uppercase text-center text-gray-400 hover:text-intimar-primary transition-all">Ver Carta</a>
                        <a href="https://maps.app.goo.gl/B6V8iT3gZTCuRfxbA" target="_blank" class="bg-white border border-gray-100 py-2 rounded-xl text-[7px] font-black uppercase text-center text-gray-400 hover:text-intimar-primary transition-all">Ubicación</a>
                    </div>
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

            <!-- CARD DE CONFIRMACIÓN PREMIUM -->
            <div class="w-full max-w-md mx-auto bg-white rounded-[2rem] md:rounded-[3rem] border border-gray-100 shadow-2xl shadow-gray-200/50 overflow-hidden relative group animate-in zoom-in-95 duration-700">
                <div class="absolute top-0 right-0 w-40 h-40 bg-intimar-gold/5 rounded-full -mr-20 -mt-20 blur-3xl group-hover:bg-intimar-gold/10 transition-all duration-1000"></div>
                
                <div class="p-6 md:p-12 relative z-10 space-y-8 md:space-y-10">
                    <!-- Código de Reserva -->
                    <div class="text-center space-y-2 md:space-y-3">
                        <p class="text-[8px] md:text-[9px] font-black text-gray-400 uppercase tracking-[0.4em]">{{ t.idLabel }}</p>
                        <h3 class="text-4xl md:text-5xl font-light tracking-tighter text-intimar-dark uppercase serif-font">{{ reservationId }}</h3>
                        <p class="text-[7px] md:text-[8px] text-gray-300 uppercase font-bold tracking-[0.2em]">{{ t.idHint }}</p>
                    </div>

                    <!-- Sección Anticipo (Si aplica) -->
                    <div v-if="requiresAnticipo" class="pt-8 md:pt-10 border-t border-gray-50 space-y-6 md:space-y-8">
                        <div class="text-center space-y-4">
                            <span class="inline-block px-4 py-1.5 bg-intimar-gold/10 text-intimar-gold text-[8px] md:text-[9px] font-black uppercase tracking-[0.2em] rounded-full">{{ t.anticipoTitle }}</span>
                            <p class="text-[11px] md:text-xs font-medium text-gray-500 leading-relaxed max-w-[280px] mx-auto italic">{{ t.anticipoNotice }}</p>
                            <div class="py-2 md:py-4">
                                <span class="block text-[7px] md:text-[8px] font-bold text-gray-300 uppercase tracking-widest mb-1">{{ lang === 'es' ? 'Total a depositar' : 'Total to deposit' }}</span>
                                <div class="text-4xl md:text-5xl font-black text-intimar-primary tracking-tighter serif-font">S/ {{ totalAnticipo }}</div>
                            </div>
                        </div>

                        <!-- Condiciones Elegantes -->
                        <div class="bg-gray-50/50 rounded-[1.5rem] md:rounded-[2rem] p-6 md:p-8 space-y-4 md:space-y-5">
                            <p class="text-[7px] md:text-[8px] font-black text-gray-400 uppercase tracking-[0.3em] text-center mb-1 md:mb-2">{{ t.anticipoConditions }}</p>
                            <div class="space-y-3 md:space-y-4">
                                <div v-for="item in [t.anticipoItem1, t.anticipoItem2, t.anticipoItem3]" :key="item" class="flex gap-3 md:gap-4 items-start">
                                    <div class="w-1.5 h-1.5 rounded-full bg-intimar-gold/30 mt-1.5 shrink-0"></div>
                                    <p class="text-[9px] md:text-[10px] font-medium text-gray-500 leading-relaxed">{{ item }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Aviso de Correo y Botón de Verificación WhatsApp -->
            <div class="space-y-6 pt-4">
                <div class="p-4 bg-red-50 border border-red-100 rounded-2xl">
                    <p class="text-[10px] font-black text-red-600 uppercase tracking-widest leading-relaxed">
                        {{ t.emailCheck1 }}<br/>
                        <span class="text-[8px] opacity-70">{{ t.emailCheck2 }}</span>
                    </p>
                </div>

                <div class="space-y-3">
                    <p class="text-[9px] font-bold text-gray-400 uppercase tracking-[0.2em]">{{ t.verifyText }}</p>
                    <a 
                        :href="whatsappUrl" 
                        target="_blank"
                        class="inline-flex items-center gap-3 px-8 py-5 bg-[#25D366] text-white rounded-full font-black uppercase tracking-[0.2em] text-[10px] shadow-xl shadow-green-500/20 transition-all hover:scale-[1.03] active:scale-95"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 448 512" fill="currentColor"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-5.5-2.8-23.2-8.5-44.2-27.1-16.4-14.6-27.4-32.7-30.6-38.2-3.2-5.6-.3-8.6 2.5-11.3 2.5-2.5 5.6-6.5 8.3-9.7 2.8-3.3 3.7-5.6 5.6-9.3 1.9-3.7 0.9-6.9-0.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-0.2-6.9-0.2-10.6-0.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 13.2 5.8 23.5 9.2 31.5 11.8 13.3 4.2 25.4 3.6 35 2.2 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                        {{ t.btnVerifyWsp }}
                    </a>
                </div>
            </div>

            <button @click="resetForm" class="text-[9px] font-bold uppercase tracking-[0.4em] text-intimar-primary border-b border-intimar-primary/20 pb-1 transition-all hover:border-intimar-primary">{{ t.btnBackHome }}</button>
          </div>

          <footer class="mt-20 pb-10 border-t border-gray-50 pt-8 text-center space-y-2">
            <p class="text-gray-400 text-[10px] md:text-xs leading-relaxed font-medium">
              © {{ new Date().getFullYear() }} Inti-Mar Paracas. {{ lang === 'es' ? 'Todos los derechos reservados.' : 'All rights reserved.' }}
            </p>
            <p class="text-[9px] font-black uppercase tracking-[0.3em] text-gray-300">Desarrollado por NicoleXaviera y JackoTinoco</p>
          </footer>
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
      <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 448 512" fill="currentColor"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-5.5-2.8-23.2-8.5-44.2-27.1-16.4-14.6-27.4-32.7-30.6-38.2-3.2-5.6-.3-8.6 2.5-11.3 2.5-2.5 5.6-6.5 8.3-9.7 2.8-3.3 3.7-5.6 5.6-9.3 1.9-3.7 0.9-6.9-0.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-0.2-6.9-0.2-10.6-0.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 13.2 5.8 23.5 9.2 31.5 11.8 13.3 4.2 25.4 3.6 35 2.2 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
      <span class="absolute right-16 bg-white text-gray-900 text-[10px] font-bold px-3 py-2 rounded-xl shadow-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none uppercase tracking-widest border border-gray-100">{{ lang === 'es' ? '¿Consultas?' : 'Questions?' }}</span>
    </a>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { call } from 'frappe-ui'
import { VueTelInput } from 'vue-tel-input'
import 'vue-tel-input/vue-tel-input.css'

const step = ref(1); const submitting = ref(false); const lang = ref('es'); const showManualPax = ref(false); const currentMonthOffset = ref(0); const currentHeroIdx = ref(0); let heroTimer = null;
const radarData = ref([]); const loadingSlots = ref(false);
const reservationId = ref('');
const requiresAnticipo = ref(false);
const totalAnticipo = computed(() => {
  const pax = (Number(form.adultos) || 0) + (Number(form.ninos) || 0)
  return pax * 20
})
const showWaitlistModal = ref(false);
const apiError = ref('');
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
    labelManualPax: 'Especifique cantidad',
    labelDate: 'Selecciona una Fecha', btnSearch: 'Buscar Disponibilidad',
    title2: 'Horarios Disponibles', subtitle2: 'Sujeto a disponibilidad del día',
    policyTitle: 'Tolerancia', policyDesc: '15 minutos. Pasado este tiempo, su mesa podría ser reasignada.',
    assignmentNote: 'Las mesas se asignan según disponibilidad por orden de llegada.',
    title3: 'Confirma tus Datos', subtitle3: 'Solo falta un paso para registrar tu reserva',
    labelName: 'Nombre', labelLastname: 'Apellido', labelPhone: 'Teléfono',
    title4: 'Personalizar', subtitle4: 'Ayúdanos a que tu visita sea única',
    labelSpecialReq: '¿Algún requerimiento especial?', placeholderReq: 'Indícanos si tienes alguna petición especial...',
    labelNeeds: '¿Alguna necesidad especial?', placeholderNeeds: 'Voy con mi bebe canino...',
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
    btnChangeTime: 'Elegir otro horario',
    btnVerifyWsp: 'Verificar mi reserva',
    verifyText: '¿No te llegó el correo? Verifica aquí:',
    emailCheck1: 'Por favor, revisa tu correo electrónico',
    generalPolicy: 'Nuestro horario de atención es de 11:00 a.m. a 4:00 p.m, la asignación de mesas es por orden de llegada y la zona sujeta a disponibilidad. Para reservas grupales de 8 a más personas, se requiere un pago de consumo anticipado.',
    anticipoTitle: 'Pago de Anticipo Requerido',
    anticipoNotice: 'Debido al tamaño de tu grupo, nos contactaremos pronto vía WhatsApp para coordinar el pago del anticipo que sería:',
    anticipoConditions: 'Condiciones de Reserva',
    anticipoItem1: 'Para grupos de 8 o más personas, se requiere un anticipo de 20 soles por persona previo a la visita.',
    anticipoItem2: 'Este importe será deducido del total de su consumo en el restaurante.',
    anticipoItem3: 'Por favor, envíe el comprobante de pago vía WhatsApp para formalizar su confirmación.'
  },
  en: {
    welcomeQuote: 'Welcome to this place of respect for nature, taste for good food, and Passion for the sea.',
    summaryTitle: 'Booking Summary', summaryPax: 'People',
    title1: 'Experience', subtitle1: 'How many people will visit us?',
    labelManualPax: 'Specify amount',
    labelDate: 'Select a Date', btnSearch: 'Search Availability',
    title2: 'Available Slots', subtitle2: 'Times subject to availability',
    btnVerifyWsp: 'Verify my booking',
    verifyText: "Didn't get the email? Verify here:",
    emailCheck1: 'Please check your email',
    generalPolicy: 'Our service hours are from 11:00 a.m. to 4:00 p.m., table assignment is on a first-come, first-served basis, and area is subject to availability. For group bookings of 8 or more people, advance payment is required.',
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
    btnChangeTime: 'Choose another time',
    btnVerifyWsp: 'Verify via WhatsApp',
    verifyText: 'Didn\'t get the email? Verify here:',
    emailCheck1: 'Please, check your email inbox',
    emailCheck2: 'If you didn\'t receive the confirmation, contact reception:',
    generalPolicy: 'Our service hours are from 11:30 a.m. to 4:00 p.m. Table assignment is on a first-come, first-served basis. For groups of 8 or more, a pre-payment is required.'
  }
}

const t = computed(() => translations[lang.value])
const whatsappUrl = computed(() => {
  const phone = '51981318866' // Número de recepción
  
  // Formatear fecha a DD-MM-YYYY
  let fechaFormat = form.fecha
  if (form.fecha && form.fecha.includes('-')) {
    const [y, m, d] = form.fecha.split('-')
    fechaFormat = `${d}-${m}-${y}`
  }

  const msg = lang.value === 'es' 
    ? `¡Hola! Acabo de solicitar una reserva pero no me llegó el correo. Mi código es *${reservationId.value}* a nombre de *${form.nombre} ${form.apellido}* para el día *${fechaFormat}* a las *${form.hora}* para *${form.adultos}* personas.`
    : `Hi! I just requested a reservation but I didn't get the email. My code is *${reservationId.value}* for *${form.nombre} ${form.apellido}* on *${fechaFormat}* at *${form.hora}* for *${form.adultos}* people.`
  
  return `https://wa.me/${phone}?text=${encodeURIComponent(msg)}`
})
const formatDate = (dateStr) => { if (!dateStr) return ''; const date = new Date(dateStr + 'T12:00:00'); return date.toLocaleDateString(lang.value === 'es' ? 'es-ES' : 'en-US', { weekday: 'short', day: 'numeric', month: 'short' }).toUpperCase(); }
const calendarData = computed(() => { const months = []; let curr = new Date(); curr.setMonth(curr.getMonth() + currentMonthOffset.value); curr.setDate(1); for (let i = 0; i < 2; i++) { const month = curr.getMonth(); const year = curr.getFullYear(); let firstDay = new Date(year, month, 1).getDay(); let padding = firstDay === 0 ? 6 : firstDay - 1; const daysInMonth = new Date(year, month + 1, 0).getDate(); const days = []; for (let d = 1; d <= daysInMonth; d++) { const date = new Date(year, month, d); const dateStr = year + '-' + String(month + 1).padStart(2, '0') + '-' + String(d).padStart(2, '0'); const today = new Date(); today.setHours(0,0,0,0); days.push({ day: d, dateStr, disabled: date < today }) } months.push({ month, year, padding, days }); curr.setMonth(curr.getMonth() + 1); } return months })
const nextMonth = () => currentMonthOffset.value++; const prevMonth = () => { if (currentMonthOffset.value > 0) currentMonthOffset.value-- };
const getMonthName = (m) => { const names = lang.value === 'es' ? ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'] : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']; return names[m]; }
const selectDate = (dateStr) => { form.fecha = dateStr; fetchAvailability(); }; 
const availableSlots = ['11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '15:45'];

const fetchAvailability = async () => {
  if (!form.fecha) return;
  loadingSlots.value = true;
  try {
    const data = await call('intimar_erp.api.get_ocupacion_proyectada', { fecha: form.fecha });
    radarData.value = data || [];
  } catch (e) {
    console.error('Error fetching availability:', e);
  } finally {
    loadingSlots.value = false;
  }
};

const isSlotDisabled = (slotTime) => {
  if (!radarData.value || radarData.value.length === 0) return false;
  const pax = (Number(form.adultos) || 0) + (Number(form.ninos) || 0);
  const slot = radarData.value.find(s => s.hora === slotTime);
  if (!slot) return false;
  
  const salonLleno = (slot.ocupado + pax) > slot.limite;
  const cocinaLlena = (slot.llegando + pax) > slot.limite_cocina;
  
  return salonLleno || cocinaLlena;
};

const handleSlotClick = (slot) => {
  if (isSlotDisabled(slot)) return
  form.hora = slot
  nextStep()
}

const getSlotClass = (slot) => {
  if (isSlotDisabled(slot)) {
    return 'border-gray-100 bg-gray-50/50 text-gray-200 cursor-not-allowed opacity-50';
  }
  return 'border-gray-50 text-gray-300 hover:border-intimar-primary hover:text-intimar-primary active:scale-95';
};

watch(() => [form.adultos, form.ninos], () => {
  if (form.fecha) fetchAvailability();
});
const nextStep = () => { step.value++; window.scrollTo({ top: 0, behavior: 'smooth' }) }

const validateForm = () => {
    Object.keys(errors).forEach(key => delete errors[key])
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!form.nombre) errors.nombre = true
    if (!form.apellido) errors.apellido = true
    if (!form.email || !emailRegex.test(form.email)) errors.email = true
    if (!form.celular) errors.celular = true
    if (!form.adultos || form.adultos < 1) errors.adultos = true
    if (!form.acepta_legal3) errors.acepta_legal3 = true
    return Object.keys(errors).length === 0
}

const submitReserva = async () => {
  if (!validateForm()) { window.scrollTo({ top: 0, behavior: 'smooth' }); return }
  
  // Intentar obtener el token CSRF desde la cookie si no existe en window
  if (!window.csrf_token) {
    const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('frappe_csrftoken='));
    if (csrfCookie) window.csrf_token = csrfCookie.split('=')[1];
  }

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
        requiresAnticipo.value = !!res.requires_anticipo;
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
