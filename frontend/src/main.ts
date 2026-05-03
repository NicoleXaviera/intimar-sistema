import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import './index.css'

import { Button, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'

let app = createApp(App)
setConfig('resourceFetcher', frappeRequest)

// Handle Vite chunk load errors
window.addEventListener('error', (e) => {
  if (e.message && (e.message.includes('Unable to preload CSS') || e.message.includes('Failed to fetch dynamically imported module'))) {
    window.location.reload()
  }
}, true)

app.use(router)
app.use(resourcesPlugin)

app.component('Button', Button)
app.mount('#app')
