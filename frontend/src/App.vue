<!--
  App.vue
  --------
  Componente raiz da aplicação Vue 3.

  Responsabilidade única: renderizar o <RouterView /> que carrega
  a view correspondente à rota atual (HomeView por padrão).

  A tag <html> recebe a classe 'dark' no carregamento para ativar
  o tema escuro do PrimeVue (configurado em main.js com darkModeSelector: 'html').
-->

<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'

// Ativa tema escuro no PrimeVue via seletor 'html'
document.documentElement.classList.add('dark')
</script>
