/**
 * router/index.js
 * ----------------
 * Configuração do Vue Router.
 *
 * Atualmente a aplicação possui uma única view (HomeView).
 * O router é incluído para facilitar expansões futuras
 * (ex: tela de histórico, configurações, relatórios).
 */

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Pizza Optimizer' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  document.title = to.meta?.title ?? 'Pizza Optimizer'
})

export default router
