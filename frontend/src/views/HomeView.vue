<!--
  [DOC-F07] views/HomeView.vue
  -----------------------------
  Tela principal e única da aplicação.

  Responsabilidades:
  - Compor todos os componentes em um layout responsivo
  - Header com nome da aplicação e descrição
  - Grid de duas colunas em desktop: formulário à esquerda, resultado à direita
  - Colapsa para coluna única em mobile (< 768px via Tailwind md:)
  - Gerenciar transições de entrada dos componentes

  Layout:
  ┌─────────────────────────────────────────────┐
  │  Header — Pizza Optimizer                   │
  ├─────────────────┬───────────────────────────┤
  │  StockForm      │  ResultCard               │
  │                 ├───────────────────────────┤
  │                 │  UsageChart               │
  │                 ├───────────────────────────┤
  │                 │  ExplainPanel             │
  └─────────────────┴───────────────────────────┘
-->

<template>
  <div class="min-h-screen" style="background: var(--color-surface);">

    <!-- Header -->
    <header
      class="border-b px-6 py-4"
      style="border-color: var(--color-surface-line); background: var(--color-surface-card);"
    >
      <div class="max-w-5xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div
            class="w-9 h-9 rounded-lg flex items-center justify-center text-lg"
            style="background: var(--color-brand);"
          >
            🍕
          </div>
          <div>
            <h1 class="text-base font-bold" style="color: var(--color-text-primary)">
              Pizza Optimizer
            </h1>
            <p class="text-xs" style="color: var(--color-text-muted)">
              Programação Linear Inteira
            </p>
          </div>
        </div>

        <!-- Badge de versão -->
        <span
          class="text-xs px-2 py-1 rounded-full font-medium"
          style="
            background: rgba(16,185,129,0.1);
            border: 1px solid rgba(16,185,129,0.2);
            color: var(--color-brand);
          "
        >
          v1.0.0
        </span>
      </div>
    </header>

    <!-- Conteúdo principal -->
    <main class="max-w-5xl mx-auto px-4 py-6">

      <!-- Subtítulo da seção -->
      <div class="mb-6">
        <h2 class="text-xl font-bold mb-1" style="color: var(--color-text-primary)">
          Otimização de Lucro: Muçarela vs Calabresa
        </h2>
        <p class="text-sm" style="color: var(--color-text-muted)">
          Informe o estoque disponível para calcular a combinação de pizzas
          que maximiza o lucro da pizzaria.
        </p>
      </div>

      <!-- Grid principal: 2 colunas no desktop, 1 no mobile -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

        <!-- Coluna esquerda: formulário -->
        <div class="flex flex-col gap-4">
          <StockForm />

          <!-- Resumo do modelo matemático -->
          <div class="card">
            <h3 class="text-xs font-semibold uppercase tracking-wider mb-3"
                style="color: var(--color-text-muted)">
              Modelo Matemático
            </h3>
            <div class="space-y-1.5">
              <p class="text-xs font-mono" style="color: var(--color-text-secondary)">
                <span style="color: var(--color-brand)">max</span>
                Z = 20x + 25y
              </p>
              <p class="text-xs font-mono" style="color: var(--color-text-muted)">
                s.a. 0.5x + 0.5y ≤ massa
              </p>
              <p class="text-xs font-mono" style="color: var(--color-text-muted)">
                &nbsp;&nbsp;&nbsp;&nbsp; 0.3x + 0.2y ≤ queijo
              </p>
              <p class="text-xs font-mono" style="color: var(--color-text-muted)">
                &nbsp;&nbsp;&nbsp;&nbsp; 0.2x + 0.2y ≤ molho
              </p>
              <p class="text-xs font-mono" style="color: var(--color-text-muted)">
                &nbsp;&nbsp;&nbsp;&nbsp; 0.15y ≤ calabresa
              </p>
              <p class="text-xs font-mono" style="color: var(--color-text-muted)">
                &nbsp;&nbsp;&nbsp;&nbsp; x, y ∈ ℤ⁺
              </p>
            </div>
          </div>
        </div>

        <!-- Coluna direita: resultados -->
        <div class="flex flex-col gap-4">
          <ResultCard />
          <Transition name="fade">
            <UsageChart v-if="store.hasResult" />
          </Transition>
          <Transition name="fade">
            <ExplainPanel v-if="store.hasResult" />
          </Transition>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer
      class="text-center py-4 text-xs border-t mt-8"
      style="
        color: var(--color-text-muted);
        border-color: var(--color-surface-line);
      "
    >
      Pizza Optimizer · PuLP + CBC · Vue 3 + FastAPI
    </footer>
  </div>
</template>

<script setup>
import StockForm from '../components/StockForm.vue'
import ResultCard from '../components/ResultCard.vue'
import UsageChart from '../components/UsageChart.vue'
import ExplainPanel from '../components/ExplainPanel.vue'
import { useOptimizerStore } from '../stores/optimizer'

const store = useOptimizerStore()
</script>
