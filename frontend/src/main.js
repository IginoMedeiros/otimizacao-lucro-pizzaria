/**
 * main.js
 * --------
 * Ponto de entrada da aplicação Vue 3.
 *
 * Responsabilidades:
 * - Instanciar o app Vue
 * - Registrar plugins globais: PrimeVue, Pinia, Vue Router
 * - Importar estilos globais (Tailwind + tokens)
 * - Montar o app no elemento #app do index.html
 *
 * Plugins registrados:
 * - PrimeVue   → componentes de UI (InputNumber, Button, Card, etc.)
 * - Pinia      → gerenciamento de estado global
 * - Vue Router → navegação entre views (preparado para expansão futura)
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import 'primeicons/primeicons.css'

import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

// Pinia — gerenciamento de estado
app.use(createPinia())

// Vue Router — navegação
app.use(router)

// PrimeVue — componentes UI com tema Aura (minimalista)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: 'html', // tema escuro aplicado globalmente
      cssLayer: false,
    },
  },
})

app.mount('#app')
