/**
 * vite.config.js
 * ---------------
 * Configuração do Vite para o projeto Vue 3.
 *
 * - Plugin Vue: habilita suporte a Single File Components (.vue)
 * - Plugin Tailwind: integração nativa Tailwind v4 com Vite (sem postcss manual)
 * - Proxy /api: redireciona chamadas do frontend para o backend FastAPI
 *   em desenvolvimento — evita problemas de CORS durante o dev local
 * - Em produção (Docker), o Nginx cuida do proxy reverso
 */

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  server: {
    port: 5173,
    proxy: {
      // Redireciona /api/* → http://backend:8000/api/* em dev local
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
